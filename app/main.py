#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without technical
# support, and with no warranty, express or implied, as to its usefulness for
# any purpose.
#
#  Author: Jamie Hopper <jh@mode14.com>
# --------------------------------------------------------------------------

import logging
import time

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import redirect
from flask import Response
from flask import abort
from flask import request
from flask import make_response
from flask.logging import default_handler

import models
import config
from last_bump import version as __version__
from last_bump import hexdigest

###########################################

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config.AppConfig')


formatter = logging.Formatter(
    fmt=config.LOG_FORMAT,
    datefmt=config.LOG_FORMAT_DATE
)
default_handler.setFormatter(formatter)
app.logger.setLevel(logging.DEBUG)


###########################################


app.logger.info('====================================')
app.logger.info(f' nps v{__version__}')
app.logger.info(' by @jthop <jh@mode14.com>')
app.logger.info('------------------------------------')
app.logger.info(f' source hash: { hexdigest[0:7] }')
app.logger.info(f' config v{ config.__version__ }')
app.logger.info(f' dynamodb model v{ models.Phone.Meta.__version__ }')
app.logger.info('------------------------------------')
app.logger.info(f' instance { config.INSTANCE_ID }')
app.logger.info(f' docker: { config.DOCKER_HOSTNAME }')
app.logger.info(f' python v{ config.PYTHON_VERSION }')
app.logger.info(f' environment: pip v{ config.PIP_VERSION }')
app.logger.info(f' flask v{ config.FLASK_VERSION }')
app.logger.info(f' wsgi: { config.SERVER_SOFTWARE }')
app.logger.info('====================================')


# Cisco-CP-8841-3PCC/11.0 (00562b043615)
def render_xml(*args, **kwargs):
    xml = render_template(*args, **kwargs)

    r = make_response(xml)
    r.mimetype = 'application/xml'
    return r


###########################################


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/phones/all')
def all_phones():
    return render_template('all_phones.html',
            phones=models.Phone.scan()
        )


@app.route('/phones/<mac>')
def single_phone(mac):
    try:
        phone = models.Phone.get(mac)
    except models.Phone.DoesNotExist:
        app.logger.error(f'404 - mac: {mac}')
        abort(404)

    return render_template('single_phone.html',
            p=phone
        )


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
    except models.Phone.DoesNotExist:
        app.logger.error(f'404 - mac: {mac}')
        abort(404)

    app.logger.debug(f'record found for mac: {mac}')
    return render_xml(
        phone.template,
        phone=phone
    )


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
    return render_xml(
        '404.xml',
        full_path=request.full_path
    ), 404


@app.route('/_health/<patient>', methods=['GET'])
def healthcheck(patient='vagrant'):
    '''
    health checks for docker
    '''

    #app.logger.info(f'HEALTHCHECK for: <{patient}> returned 200')
    return jsonify({'success': True})


if __name__ == "__main__":
     app.run(host='0.0.0.0', port=7000, debug=False)
