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

__version__ = '1.3'


"""
Now anywhere in the program that has imported config, we can
use config.CONTAINER to know if we are actually running
in a container or not.
"""
CONTAINER = environ.get('INSIDE_CONTAINER')
if CONTAINER:
    PHONE_MODELS = Path('/app/yaml/phone_models.yml')
    SYSTEMS = Path('/app/yaml/systems.yml')
    ADDITIONAL_TEMPLATE = Path('/app/templates/additional/')
    ALTERNATE_TEMPLATE = Path('/app/templates/alternate/')
else:
    PHONE_MODELS = Path('./yaml/phone_models.yml')
    SYSTEMS = Path('./yaml/systems.yml')    
    ADDITIONAL_TEMPLATE = Path('./templates/additional/')
    ALTERNATE_TEMPLATE = Path('./templates/alternate/')


APP_NAME = 'voip'
#LOG_FORMAT = '[%(asctime)s %(name)9s@%(lineno)-3d %(levelname)8s]  %(message)s'
LOG_FORMAT_DATE = '%m-%d %H:%M:%S'
LOG_FORMAT = '[%(asctime)-12s] %(levelname)-8s %(message)s'
JSONIFY_PRETTYPRINT_REGULAR = True

docker_host = 'a-b-c'
d = environ.get('HOSTNAME', None)
if d:
    docker_host = '-'.join([d[:4], d[4:8], d[8:]])
ver = {}
ver['docker_host'] = docker_host
ver['pip_version'] = environ.get('PYTHON_PIP_VERSION', '1.0')
ver['python_version'] = environ.get('PYTHON_VERSION', '1.0')
ver['server_software'] = environ.get('SERVER_SOFTWARE', 'server/1.0')
ver['flask_version'] = pkg_resources.get_distribution("flask").version

