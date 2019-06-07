#!/usr/bin/env
# -*- coding: utf-8 -*-
"""Dashboard API"""

from flask import Blueprint, current_app as app, json, jsonify, Response, session
from flaskr.account import user_required

import requests

blueprint = Blueprint('dashboard', __name__, url_prefix='/api')


@blueprint.route('/dashboard', methods=['GET'])
@blueprint.route('/v1/dashboard', methods=['GET'])
@blueprint.route('/v1.0/dashboard', methods=['GET'])
@user_required
def dashboard() -> Response:
    """Dashboard"""
    response = requests.get(app.config['SERVICE_VISUALIZATION'] + '/api/dashboard',
                            data=json.dumps({"id": session["id"]}), headers={'content-type': 'application/json'})

    response = jsonify({'firstName': session["firstName"], "lastName": session["lastName"]})
    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response
