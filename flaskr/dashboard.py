#!/usr/bin/env
# -*- coding: utf-8 -*-
"""Dashboard API"""

from flask import Blueprint
from flask import jsonify
from flask import Response
from flask import session

from flaskr.account import user_required
import requests

blueprint = Blueprint('dashboard', __name__, url_prefix='/api')


@blueprint.route('/dashboard', methods=['GET'])
@blueprint.route('/v1/dashboard', methods=['GET'])
@blueprint.route('/v1.0/dashboard', methods=['GET'])
@user_required
def dashboard() -> Response:
    """Dashboard"""
    response = requests.get('http://localhost:8080/mysql/api/dashboard', data='{"id":"' + session["id"] + '"}',
                            headers={'content-type': 'application/json'})

    response = jsonify({'firstName': session["firstName"], "lastName": session["lastName"]})
    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response
