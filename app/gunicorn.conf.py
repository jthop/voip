#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without technical
# support, and with no warranty, express or implied, as to its usefulness for
# any purpose.
#
#  Author: Jamie Hopper <jh@mode14.com>
# --------------------------------------------------------------------------
#
# to use config file: --config CONFIG

import multiprocessing
import os
from distutils.util import strtobool

#
# Server socket
#
#   bind - The socket to bind.
#
#       A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'.
#       An IP is a valid HOST.
#
#   backlog - The number of pending connections. This refers
#       to the number of clients that can be waiting to be
#       served. Exceeding this number results in the client
#       getting an error when attempting to connect. It should
#       only affect servers under significant load.
#
#       Must be a positive integer. Generally set in the 64-2048
#       range.
#

bind = os.getenv('BIND', '0.0.0.0:80')
backlog = int(os.getenv('BACKLOG', '2048'))

#
#   Logging
#
#   logfile - The path to a log file to write to.
#
#       A path string. "-" means log to stdout.
#
#   loglevel - The granularity of log output
#
#       A string of "debug", "info", "warning", "error", "critical"
#

accesslog = '-'
errorlog = '-'
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'debug')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" in or %(D)sµs'
#logconfig = '/app/gunicorn.log.conf'

#
# Worker processes
#
#   workers - The number of worker processes that this server
#       should keep alive for handling requests.
#
#       A positive integer generally in the 2-4 x $(NUM_CORES)
#       range. You'll want to vary this a bit to find the best
#       for your particular application's work load.
#
#   worker_class - The type of workers to use. The default
#       sync class should handle most 'normal' types of work
#       loads. You'll want to read
#       http://docs.gunicorn.org/en/latest/design.html#choosing-a-worker-type
#       for information on when you might want to choose one
#       of the other worker classes.
#
#       A string referring to a Python path to a subclass of
#       gunicorn.workers.base.Worker. The default provided values
#       can be seen at
#       http://docs.gunicorn.org/en/latest/settings.html#worker-class
#
#   worker_connections - For the eventlet and gevent worker classes
#       this limits the maximum number of simultaneous clients that
#       a single process can handle.
#
#       A positive integer generally set to around 1000.
#
#   timeout - If a worker does not notify the master process in this
#       number of seconds it is killed and a new worker is spawned
#       to replace it.
#
#       Generally set to thirty seconds. Only set this noticeably
#       higher if you're sure of the repercussions for sync workers.
#       For the non sync workers it just means that the worker
#       process is still communicating and is not tied to the length
#       of time required to handle a single request.
#
#   keepalive - The number of seconds to wait for the next request
#       on a Keep-Alive HTTP connection.
#
#       A positive integer. Generally set in the 1-5 seconds range.
#

workers = 1
#threads = int(os.getenv('PYTHON_MAX_THREADS', 1))
#workers = int(os.getenv('WEB_CONCURRENCY', multiprocessing.cpu_count() * 2))
worker_class = os.getenv('WORKER_CLASS', 'sync')
worker_connections = int(os.getenv('WORKER_CONNECTIONS', 1000))
timeout = int(os.getenv('TIMEOUT', 30))
keepalive = int(os.getenv('KEEPALIVE', 5))




# debug
reload = bool(strtobool(os.getenv('WEB_RELOAD', 'false')))