#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without technical
# support, and with no warranty, express or implied, as to its usefulness for
# any purpose.
#
#  Author: Jamie Hopper <jh@mode14.com>
# --------------------------------------------------------------------------

from functools import wraps
import logging

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import redirect
from flask import Response
from flask import abort
from flask import request
from flask.logging import default_handler

import models
import config

from last_bump import version as __version__
from last_bump import hexdigest



###########################################


class XMLResponse(Response):
    default_mimetype = 'application/xml'

class XMLFlask(Flask):
    response_class = XMLResponse

app = XMLFlask(__name__, static_url_path='/static')


# creates a Flask application, named app
#app = Flask(__name__, static_url_path='/static')
app.config['APP_VERSION'] = __version__
app.config['CONFIG_VERSION'] = config.__version__


logging.basicConfig(
    format=config.LOG_FORMAT,
    datefmt=config.LOG_FORMAT_DATE,
    level=logging.DEBUG
)
pynamodb_logger = logging.getLogger("pynamodb")
pynamodb_logger.addHandler(default_handler)

app_logger = logging.getLogger(__name__)
app_logger.debug('next line main')
app_logger.debug(__name__)

###########################################


app.logger.info('======================================')
app.logger.info(f'nps v{__version__}')
app.logger.info('by @jthop <jh@mode14.com>')
app.logger.info('--------------------------------------')
app.logger.info(f'blake2b hash { hexdigest }')
app.logger.info(f'config v{ config.__version__ }')
app.logger.info('--------------------------------------')
app.logger.info(f'python v{ config.ver["python_version"] }')
app.logger.info(f'environment: pip v{ config.ver["pip_version"] }')
app.logger.info(f'flask v{ config.ver["flask_version"] }')
app.logger.info(f'wsgi: { config.ver["server_software"] }')
app.logger.info(f'docker host: { config.docker_host }')
app.logger.info('======================================')

# agent
# Cisco-CP-8841-3PCC/11.0 (00562b043615)

###########################################


@app.route('/CP-7821-3PCC.xml')
@app.route('/CP-7841-3PCC.xml')
@app.route('/CP-8841-3PCC.xml')
@app.route('/CP-8851-3PCC.xml')
@app.route('/CP-8845-3PCC.xml')
@app.route('/CP-8865-3PCC.xml')
def CP_PSN():
    # initial PSN.xml
    return redirect('/cp/conf/$MAU.xml', code=302)


@app.route('/cp/conf/<mac>.xml')
def MAU(mac):
    try:
        phone = models.Phone.get(mac)
        #phone.load_ext()
    except models.Phone.DoesNotExist:
        app.logger.error(f'404 - mac: {mac}')
        abort(404)

    app.logger.debug(f'record found for mac: {mac}')

    return render_template(
        phone.template,
        phone=phone
    )


@app.route('/cp/dir.xml')
def directory():
    return render_template('directory.xml')


"""
[--status]http://my_http_server/config-mpp-status.xml
[--delta]http://my_http_server/config-mpp-delta.xml
"""


@app.route('/config-mpp-status.xml', methods = ['POST', 'PUT'])
def status():
    data = request.form
    app.logger.info(data)
    return


@app.route('/config-mpp-delta.xml', methods = ['POST', 'PUT'])
def delta():
    data = request.form
    app.logger.info(data)
    return


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        '404.xml',
        full_path=request.full_path
    ), 404


@app.route('/_health/<patient>', methods=['GET'])
def healthcheck(patient='vagrant'):
    '''
    health checks for docker
    '''

    app.logger.info(f'HEALTHCHECK for: <{patient}> returned 200')
    return jsonify({'success': True})
