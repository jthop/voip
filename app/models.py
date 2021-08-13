#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without technical
# support, and with no warranty, express or implied, as to its usefulness for
# any purpose.
#
#  Author: Jamie Hopper <jh@mode14.com>
# --------------------------------------------------------------------------
#
from __future__ import annotations

import os
import yaml
from pathlib import Path
from uuid import uuid4
from datetime import datetime
from flask import current_app as app
from flask import request

from pynamodb.models import Model
from pynamodb.attributes import BooleanAttribute
from pynamodb.attributes import DynamicMapAttribute
from pynamodb.attributes import JSONAttribute
from pynamodb.attributes import ListAttribute
from pynamodb.attributes import MapAttribute
from pynamodb.attributes import NumberAttribute
from pynamodb.attributes import UnicodeAttribute
from pynamodb.attributes import UTCDateTimeAttribute
from pynamodb_attributes import UUIDAttribute

import config


ALLOWED_SERVER_TYPES = {"Asterisk", "Broadsoft", 'SPA9000', 'RFC3265_4235', 'Sylantro'}
ALLOWED_KEM_TYPES = {'BEKEM', 'CP-8800-Audio', 'CP-8800-Video'}
ALLOWED_SECURITY_MODES = {'Auto', 'EAP-FAST', 'PEAP-GTC', 'PEAP-MSCHAPV2', 'PSK', 'WEP', 'None'}
EPOCH = datetime(1970, 1, 1, 0, 0)


"""
===================================
          KEM classes
===================================
"""

class KemButton(MapAttribute):
    button = NumberAttribute()
    func = UnicodeAttribute()


class KemUnit(MapAttribute):
    buttons = ListAttribute(of=KemButton)
    unit = NumberAttribute()

    @property
    def blanks(self):
        avail_nums = list(range(1, self._features['buttons']+1))
        button_nums = [x.button for x in self.buttons]
        return list(set(avail_nums).difference(button_nums))


class Kem(MapAttribute):
    model = UnicodeAttribute(null=True)
    server_type = UnicodeAttribute(default='Asterisk')
    units = ListAttribute(of=KemUnit)

    @property
    def number_of_units(self):
        return len(self.units)


"""
===================================
   Phone button and line classes
===================================
"""


class Line(MapAttribute):
    button = NumberAttribute()
    did = UnicodeAttribute(null=True)
    hide_missed = BooleanAttribute(null=True, default=False)
    label = UnicodeAttribute(null=True, default='$DID')
    ring = UnicodeAttribute(null=True, default='2')
    secret = UnicodeAttribute()
    server = UnicodeAttribute()


class Button(MapAttribute):
    button = NumberAttribute()
    func = UnicodeAttribute()


"""
===================================
         Wifi Attribute
===================================

Implemented per Phone.  Things could get messy if
an SSID changes... Would be better to reuse these.
"""


class WifiConfig(MapAttribute):
    _id = UnicodeAttribute()
    psk = UnicodeAttribute(null=True)
    password = UnicodeAttribute(null=True)
    security = UnicodeAttribute(default='PSK')
    ssid = UnicodeAttribute()
    user = UnicodeAttribute(null=True)


"""
===================================
       THE MAIN PHONE MODEL
===================================
"""


class Phone(Model):
    """
    Pynamodb model for phone records
    """

    class Meta:
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        region = os.environ.get('AWS_DEFAULT_REGION')
        table_name = 'phone'
        write_capacity_units = 5
        read_capacity_units = 5
        # All your metadata are belong to us - above belong to pynamodb 
        __version__ = '1.5'

    __version__ = UnicodeAttribute(null=True, default=Meta.__version__)
    __id__ = UUIDAttribute(default=uuid4())
    additional_template = UnicodeAttribute(null=True)
    alternate_template = UnicodeAttribute(null=True)
    dark_room = BooleanAttribute(null=True)
    extension = NumberAttribute()
    did = UnicodeAttribute(null=True)
    location = UnicodeAttribute(null=True)
    mac = UnicodeAttribute(hash_key=True)
    model = UnicodeAttribute(null=True, default='')
    remote = BooleanAttribute(default=False)
    serial = UnicodeAttribute(null=True)
    station_name = UnicodeAttribute(null=True)  # {extension} - {location}
    sys_id = NumberAttribute(default=1)

    buttons = ListAttribute(of=Button, null=True)
    lines = ListAttribute(of=Line, null=True)
    kem = Kem(null=True)
    wifi = WifiConfig(null=True)

    created_at = UTCDateTimeAttribute(default=datetime.now)
    ip = UnicodeAttribute(null=True)
    updated_at = UTCDateTimeAttribute(default=EPOCH)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.__id__ = uuid4()
        return super().save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().update(*args, **kwargs)

    @classmethod
    def get(cls, *args, **kwargs):
        phone = super().get(*args, **kwargs)
        if config.CONTAINER:
            phone._agent = request.headers.get('User-Agent')
            phone._ip =request.remote_addr
        return Phone.load_references(phone)

    @staticmethod
    def load_references(phone):
        """
        load all our external data besides what was pulled
        already from pynamodb
        """

        with open(config.PHONE_MODELS.absolute()) as f:
            models = yaml.load(f, Loader=yaml.SafeLoader)

        m = models.get(phone.model)
        if m is None:
            raise ValueError(f'no model: {phone.model}')

        """
        take the phoneModel.yml info and split it into two pieces
        phone._features and phone._template
        """
        phone._features = m.get('features')
        phone._template = m.get('template')

        """
        A subset of the features are for the kem and need to be available
        to the kem class
        """
        if hasattr(phone, 'kem') and (getattr(phone, 'kem') is not None):
            phone.kem._features = m.get('features', {}).get('kem')

        """
        Lookup and the system specific config.  This is everything specific
        to the local pbx.  IPs, domains, provisioning configs, etc.
        """
        with open(config.SYSTEMS.absolute()) as f:
            systems = yaml.load(f, Loader=yaml.SafeLoader)

        phone._sys = systems.get(phone.sys_id)
        
        return phone

    @property
    def sys(self):
        return self._sys

    @property
    def features(self):
        return self._features

    @property
    def template(self):
        return self._template

    @property
    def additional_template_file(self):
        filepath = (
            Path(config.ADDITIONAL_TEMPLATE) / self.additional_template)
        if filepath.is_file():
            """
            config.ADDITIONAL_TEMPLATE is not flask friendly as it's an
            absolute path.  All Flask needs is the one directory off the
            template directory, 'additional'
            """
            flask_friendly_path = Path('additional/' + self.additional_template)
            return  str(flask_friendly_path)

    @property
    def alternate_template_file(self):
        filepath = (
            Path(config.ALTERNATE_TEMPLATE) / self.alternate_template)
        if filepath.is_file():
            """
            config.ALTERNATE_TEMPLATE is not flask friendly as it's an
            absolute path.  All Flask needs is the one directory off the
            template directory, 'alternate'
            """
            flask_friendly_path = Path('alternate/' + self.alternate_template)
            return  str(flask_friendly_path)

    @property
    def blank_lines(self):
        """
        returns:

        List with all blank line #s.  This is every # between 1 and
        max_buttons with no line

        """

        line_nums = [x.button for x in self.lines]
        avail_nums = list(range(1, self._features['buttons']+1))

        return sorted(set(avail_nums).difference(line_nums))

    @property
    def blank_buttons(self):
        """
        returns:

        List with all blank func buttons #s.  This is every # between
        1 and max_buttons with no func button

        """

        button_nums = [x.button for x in self.buttons]
        avail_nums = list(range(1, self._features['buttons']+1))

        return sorted(set(avail_nums).difference(button_nums))

    @property
    def all_blanks(self):
        """
        returns:

        Intersection of blank_buttons and blank_lines

        """

        line_nums = [x.button for x in self.lines]
        button_nums = [x.button for x in self.buttons]
        all_nums = line_nums + button_nums
        avail_nums = list(range(1, self._features['buttons']+1))

        return sorted(set(avail_nums).difference(all_nums))

if not Phone.exists():
    Phone.create_table(wait=True)
