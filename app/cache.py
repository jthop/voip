#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without technical
# support, and with no warranty, express or implied, as to its usefulness for
# any purpose.
#
#  Author: Jamie Hopper <jh@mode14.com>
# --------------------------------------------------------------------------

import yaml
import config

__version__ = '1.0'

models = systems = None

with open(config.PHONE_MODELS.absolute()) as f:
    models = yaml.load(f, Loader=yaml.SafeLoader)

with open(config.SYSTEMS.absolute()) as f:
    systems = yaml.load(f, Loader=yaml.SafeLoader)