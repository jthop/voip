#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without technical
# support, and with no warranty, express or implied, as to its usefulness for
# any purpose.
#
#  Author: Jamie Hopper <jh@mode14.com>
# --------------------------------------------------------------------------
#
#from __future__ import annotations

import os
from pathlib import Path
from uuid import uuid4
from datetime import datetime
from flask import current_app as app
from flask import request
from flask import current_app as app

from pynamodb.models import Model
from pynamodb.attributes import BooleanAttribute
from pynamodb.attributes import DynamicMapAttribute
from pynamodb.attributes import JSONAttribute
from pynamodb.attributes import ListAttribute
from pynamodb.attributes import MapAttribute
from pynamodb.attributes import NumberAttribute
from pynamodb.attributes import UnicodeAttribute
from pynamodb.attributes import UTCDateTimeAttribute
from pynamodb.attributes import VersionAttribute
from pynamodb_attributes import UUIDAttribute

import config
import cache

ALLOWED_SERVER_TYPES = {"Asterisk", "Broadsoft", 'SPA9000', 'RFC3265_4235', 'Sylantro'}
ALLOWED_KEM_TYPES = {'BEKEM', 'CP-8800-Audio', 'CP-8800-Video'}
ALLOWED_SECURITY_MODES = {'Auto', 'EAP-FAST', 'PEAP-GTC', 'PEAP-MSCHAPV2', 'PSK', 'WEP', 'None'}
EPOCH = datetime(1970, 1, 1, 0, 0)

__version__ = '1.8'

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
    __id__ = UUIDAttribute(default=uuid4())
    psk = UnicodeAttribute(null=True)
    password = UnicodeAttribute(null=True)
    security = UnicodeAttribute(default='PSK')
    ssid = UnicodeAttribute()
    user = UnicodeAttribute(null=True)


"""
===================================
      MAC ADDRESS PARSER
===================================
"""


class MacAddress(object):
    def __init__(self, mac):
        self.mac = mac
        self.default = 'cisco'
        self.caps = True

    def __str__(self):
        if self.default == 'cisco':
            return self.cisco
        else:
            return self.hp

    def _get_mac(self):
        if self.caps:
            return self.mac.upper()
        return self.mac.lower()

    @property
    def cisco(self):
        m = self._get_mac()
        c1 = self.mac.upper()[0:4]
        c2 = self.mac.upper()[4:8]
        c3 = self.mac.upper()[8:12]
        return f'{c1}.{c2}.{c3}'

    @property
    def hp(self):
        m = self._get_mac()
        h1 = self.m[0:2]
        h2 = self.m[2:4]
        h3 = self.m[4:6]
        h4 = self.m[6:8]
        h5 = self.m[8:10]
        h6 = self.m[10:12]
        return f'{h1}:{h2}:{h3}:{h4}:{h5}:{h6}'


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
        __version__ = '1.8'

    __id__ = UUIDAttribute(default=uuid4())
    __schema__ = UnicodeAttribute(null=True, default=Meta.__version__)
    __version__ = VersionAttribute()
    __created_at__ = UTCDateTimeAttribute(default=datetime.now)
    __updated_at__ = UTCDateTimeAttribute(default=EPOCH)
    __provisioned_at__ = UTCDateTimeAttribute(default=EPOCH)
    __reported_at__ = UTCDateTimeAttribute(default=EPOCH)
    
    ip = UnicodeAttribute(null=True)
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

    def __init__(self, *args, **kwargs):
        """
        unused - Override .__init__()
        """
        
        super().__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        """
        unused - overloaded .save()
        """
        
        self.__updated_at__ = datetime.now()
        return super().save(*args, **kwargs)

    def update(self, *args, **kwargs):
        """
        unused - overloaded .save()
        """

        self.__updated_at__ = datetime.now()
        return super().update(*args, **kwargs)

    @classmethod
    def get(cls, *args, **kwargs):
        """
        overloaded .get() - This is run each tiem a record is looked up.
        This is the perfect location to hook in our custom record
        altering code.

        returns:
        model instance with the requested record

        """
        
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

        m = cache.models.get(phone.model)
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

        phone._sys = cache.systems.get(phone.sys_id)

        return phone

    @property
    def sys(self):
        """
        Getter for private variable sys.  This includes the site specififc
        config.
        """
        
        return self._sys

    @property
    def features(self):
        """
        Getter for private variable features.  These include  all
        model-specific config.

        """
        
        return self._features      

    @property
    def template(self):
        """
        returns:

        Flask friendly file path that can be used to load the template.

        """
        
        return self._template

    @property
    def pretty_mac(self):
        """
        MacAddress parser has 2 attributes
        .cisco = xxxx.xxxx.xxxx format mac
        .hp = xx:xx:xx:xx:xx:xx format mac
        """
        
        return MacAddress(self.mac)
        
    @property
    def additional_template_file(self):
        """
        Additional_template_file is used when a user demands config
        beyond the standard template, but they do want the standard
        features as well.  When standard config is complete we will
        provide the config from their additional template.

        returns:

        The filepath to their required template.  The file is guaranteed
        to exist.
        """

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
        """
        alterenate_template_file is used in cases where the users requires
        a completely different template than the standard one for their
        phone.

        returns:

        The filepath to their required template.  The file is guaranteed
        to exist.
        """
        
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
