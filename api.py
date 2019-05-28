#!/usr/bin/env
# -*- coding: utf-8 -*-
"""REST API"""

from flask import Flask
from flask import json
from flask import jsonify
from flask import request
import requests
from flask import Response

app = Flask(__name__)


@app.route('/api/account/logIn', methods=['POST'])
@app.route('/api/v1/account/logIn', methods=['POST'])
@app.route('/api/v1.0/account/logIn', methods=['POST'])
def log_in() -> Response:
    """Log in"""
    if requests.post('http://localhost:8080/mysql/api/account/logIn', data=json.dumps(json.loads(request.data)),
                         headers={'content-type': 'application/json'}).status_code == 200:
        response = jsonify({'some': 'data'})
    else:
        response = Response(status=401)

    response.headers.add('Access-Control-Allow-Origin', '*')

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

    return Response()


@app.route('/api/account/signUp')
@app.route('/api/v1/account/signUp')
@app.route('/api/v1.0/account/signUp')
def sign_up() -> Response:
    """Sign up"""
    return Response()


if __name__ == '__main__':
    app.run()
