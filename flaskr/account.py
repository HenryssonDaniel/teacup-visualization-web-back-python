#!/usr/bin/env
# -*- coding: utf-8 -*-
"""Account API"""

from flask import Blueprint
from flask import json
from flask import jsonify
from flask import request
from flask import Response
from flask import session

import requests

blueprint = Blueprint('account', __name__, url_prefix='/api')


@blueprint.route('/account/logIn', methods=['POST'])
@blueprint.route('/v1/account/logIn', methods=['POST'])
@blueprint.route('/v1.0/account/logIn', methods=['POST'])
def log_in() -> Response:
    """Log in"""
    response = log_in_data(json.loads(request.data))

    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response


def log_in_data(data) -> Response:
    """Log in with data"""
    response = requests.post('http://localhost:8080/mysql/api/account/logIn', data=json.dumps(data),
                             headers={'content-type': 'application/json'})

    status = response.status_code
    if status == 200:
        content = response.json()

        session['email'] = content["email"]
        session['firstName'] = content["firstName"]
        session['id'] = content["id"]
        session['lastName'] = content["lastName"]

        response = Response()
    else:
        response = Response(status=status)

    return response


@blueprint.route('/account/logOut', methods=['POST'])
@blueprint.route('/v1/account/logOut', methods=['POST'])
@blueprint.route('/v1.0/account/logOut', methods=['POST'])
def log_out() -> Response:
    """Log out"""
    if 'id' in session:
        session.pop('id')

    response = Response()
    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response


@blueprint.route('/account/recover', methods=['POST'])
@blueprint.route('/v1/account/recover', methods=['POST'])
@blueprint.route('/v1.0/account/recover', methods=['POST'])
def recover() -> Response:
    """Recover account"""
    if requests.post('http://localhost:8080/mysql/api/account/recover', data=json.dumps(json.loads(request.data)),
                     headers={'content-type': 'application/json'}).status_code == 200:
        response = jsonify({'some': 'data'})
    else:
        response = Response(status=401)

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@blueprint.route('/account/signUp', methods=['POST'])
@blueprint.route('/v1/account/signUp', methods=['POST'])
@blueprint.route('/v1.0/account/signUp', methods=['POST'])
def sign_up() -> Response:
    """Sign up"""
    data = json.loads(request.data)

    if requests.post('http://localhost:8080/mysql/api/account/signUp', data=json.dumps(data),
                     headers={'content-type': 'application/json'}).status_code == 200:
        response = log_in_data({"email": data["email"], "password": data["password"]})
    else:
        response = Response(status=401)

    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response


def user_required(view) -> Response:
    """User required"""
    def wrapped_view(**kwargs) -> Response:
        """Wrapper view"""
        if 'id' not in session:
            response = Response(status=401)
            response.headers.add('Access-Control-Allow-credentials', 'true')

            return response

        return view(**kwargs)

    return wrapped_view
