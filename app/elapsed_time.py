#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without technical
# support, and with no warranty, express or implied, as to its usefulness for
# any purpose.
#
#  Author: Jamie Hopper <jh@mode14.com>
# --------------------------------------------------------------------------

from functools import wraps
from time import process_time
from flask import current_app as app

__version__ = '1.3'

from functools import wraps

def print_elapsed_time(func):
    @wraps(func)
    def wrapper(**kwargs):
        tic = process_time()
        result = func(**kwargs) 
        app.logger.debug(f'\tElapsed time for function: {(process_time() - tic):.1f} sec.')
        return result
    return wrapper