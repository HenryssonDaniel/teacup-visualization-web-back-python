#!/usr/bin/env
# -*- coding: utf-8 -*-
"""Dashboard API"""

from flask import Blueprint, current_app as app, jsonify, Response, session
from flaskr.account import user_required

import requests

blueprint = Blueprint('dashboard', __name__, url_prefix='/api')


@blueprint.route('/dashboard', methods=['GET'])
@blueprint.route('/v1/dashboard', methods=['GET'])
@blueprint.route('/v1.0/dashboard', methods=['GET'])
@user_required
def dashboard() -> [Response, int]:
    """Dashboard"""
    response = requests.get(app.config['SERVICE_REPORT'] + '/api/session/summary')

    content = {"account": {'firstName': session["firstName"], "lastName": session["lastName"]}}

    status = response.status_code
    if status == 200:
        content["sessions"] = response.json()["sessions"]

    response = jsonify(content)
    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response, status
