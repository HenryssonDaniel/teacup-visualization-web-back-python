#!/usr/bin/env
# -*- coding: utf-8 -*-
"""REST API"""

from flask import Flask
from flask import json
from flask import jsonify
from flask import request
from flask import Response
from flask import session
from flask_cors import CORS
from flask_session import Session

import requests

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'

cors = CORS(app)
Session(app)


@app.route('/api/dashboard', methods=['GET'])
@app.route('/api/v1/dashboard', methods=['GET'])
@app.route('/api/v1.0/dashboard', methods=['GET'])
def dashboard() -> Response:
    """Dashboard"""
    if 'id' in session:
        response = requests.get('http://localhost:8080/mysql/api/dashboard', data='{"id":"' + session["id"] + '"}',
                                headers={'content-type': 'application/json'})

        response = jsonify({'firstName': session["firstName"], "lastName": session["lastName"]})
    else:
        response = Response(status=401)

    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response


@app.route('/api/account/logIn', methods=['POST'])
@app.route('/api/v1/account/logIn', methods=['POST'])
@app.route('/api/v1.0/account/logIn', methods=['POST'])
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


@app.route('/api/account/logOut', methods=['POST'])
@app.route('/api/v1/account/logOut', methods=['POST'])
@app.route('/api/v1.0/account/logOut', methods=['POST'])
def log_out() -> Response:
    """Log out"""
    if 'id' in session:
        session.pop('id')

    response = Response()
    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response


@app.route('/api/account/recover', methods=['POST'])
@app.route('/api/v1/account/recover', methods=['POST'])
@app.route('/api/v1.0/account/recover', methods=['POST'])
def recover() -> Response:
    """Recover account"""
    if requests.post('http://localhost:8080/mysql/api/account/recover', data=json.dumps(json.loads(request.data)),
                     headers={'content-type': 'application/json'}).status_code == 200:
        response = jsonify({'some': 'data'})
    else:
        response = Response(status=401)

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/api/account/signUp', methods=['POST'])
@app.route('/api/v1/account/signUp', methods=['POST'])
@app.route('/api/v1.0/account/signUp', methods=['POST'])
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


if __name__ == '__main__':
    app.run()
