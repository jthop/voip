#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without technical
# support, and with no warranty, express or implied, as to its usefulness for
# any purpose.
#
#  Author: Jamie Hopper <jh@mode14.com>
# --------------------------------------------------------------------------

from os import environ
from pathlib import Path
import pkg_resources
from uuid import uuid4


__version__ = '1.3'

############################################

CONTAINER = environ.get('INSIDE_CONTAINER')
if CONTAINER:
    d = environ.get('HOSTNAME', None)
    docker_hostname = '-'.join([d[:4], d[4:8], d[8:]])
    
    PHONE_MODELS = Path('/app/yaml/phone_models.yml')
    SYSTEMS = Path('/app/yaml/systems.yml')
    ADDITIONAL_TEMPLATE = Path('/app/templates/additional/')
    ALTERNATE_TEMPLATE = Path('/app/templates/alternate/')
else:
    docker_hostname = 'a-b-c'
    
    PHONE_MODELS = Path('./app/yaml/phone_models.yml')
    SYSTEMS = Path('./app/yaml/systems.yml')    
    ADDITIONAL_TEMPLATE = Path('./app/templates/additional/')
    ALTERNATE_TEMPLATE = Path('./app/templates/alternate/')

LOG_FORMAT_DATE = '%m-%d %H:%M:%S'
LOG_FORMAT = '[%(asctime)-12s] %(levelname)-8s %(message)s'

REQUEST_ID_HEADER = 'x-request-id'
TIME_HEADER = 'x-request-time'
JWT_SECRET_KEY = 'kljsd319408rujksdf'
JSONIFY_PRETTYPRINT_REGULAR = True

INSTANCE_ID = uuid4().hex[0:7]
DOCKER_HOSTNAME = docker_hostname
PIP_VERSION = environ.get('PYTHON_PIP_VERSION', '1.0')
PYTHON_VERSION = environ.get('PYTHON_VERSION', '1.0')
SERVER_SOFTWARE = environ.get('SERVER_SOFTWARE', 'server/1.0')
FLASK_VERSION = pkg_resources.get_distribution("flask").version
PYNAMODB_VERSION = pkg_resources.get_distribution("pynamodb").version

############################################

class AppConfig(object):    
    SECRET_KEY = environ.get('FLASK_SECRET', 'is-this-even-necessary')
    APP_NAME = 'voip'
