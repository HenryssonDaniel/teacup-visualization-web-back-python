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


@app.route('/api/account/logIn', methods=['POST'])
@app.route('/api/v1/account/logIn', methods=['POST'])
@app.route('/api/v1.0/account/logIn', methods=['POST'])
def log_in() -> Response:
    """Log in"""
    if 'logged_in' not in session:
        if requests.post('http://localhost:8080/mysql/api/account/logIn', data=json.dumps(json.loads(request.data)),
                         headers={'content-type': 'application/json'}).status_code == 200:
            response = jsonify({'some': 'data'})
            session['logged_in'] = True
        else:
            response = Response(status=401)
    else:
        response = Response(status=406)

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
    if requests.post('http://localhost:8080/mysql/api/account/signUp', data=json.dumps(json.loads(request.data)),
                     headers={'content-type': 'application/json'}).status_code == 200:
        response = jsonify({'some': 'data'})
    else:
        response = Response(status=401)

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == '__main__':
    app.run()
