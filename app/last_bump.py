#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without technical
# support, and with no warranty, express or implied, as to its usefulness for
# any purpose.
#
#  Author: Jamie Hopper <jh@mode14.com>
# --------------------------------------------------------------------------

import json

DEFAULT_FILE = '.bumped'
VERSION_KEY = 'version'
HASH_KEY = 'hexdigest'
ERROR_VERSION = '0.0.0-error.1'
ERROR_HASH = 'ffffffff'

version = ERROR_VERSION
hexdigest = ERROR_HASH

try:
    with open(DEFAULT_FILE) as f:
        js = json.load(f)
except FileNotFoundError:
    print(f'Sorry, {DEFAULT_FILE} not found.')

v = js.get(VERSION_KEY)
if v:
    version = v

h = js.get(HASH_KEY)
if h:
    hexdigest = h
