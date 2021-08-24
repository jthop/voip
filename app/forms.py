#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without technical
# support, and with no warranty, express or implied, as to its usefulness for
# any purpose.
#
#  Author: Jamie Hopper <jh@mode14.com>
# --------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import IntegerField
from wtforms import BooleanField
from wtforms import HiddenField
from wtforms import SelectField
from wtforms import FormField
from wtforms.fields.html5 import TelField

from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import MacAddress
from wtforms.validators import Optional
from wtforms.validators import AnyOf

import cache

class BasicConfig(FlaskForm):
    mac = StringField('Mac address', [DataRequired(), MacAddress()])
    serial = StringField('Serial number', [Optional()])
    extension = IntegerField('Extension number', [DataRequired()])
    did = TelField('DID number', [Optional()])
    location = StringField('Phone location', [Optional()])
    station_name = StringField('Upper left corner', [Length(min=1, max=16)])
    dark_room = BooleanField('Allow screen dim', [], default=False)
    model = SelectField('Phone model', [AnyOf(cache.models.keys())], choices=cache.models.keys())

