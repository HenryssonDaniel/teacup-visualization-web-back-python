#!/usr/bin/env
# -*- coding: utf-8 -*-
"""REST API"""

from flask import Flask
from flask import json
from flask import jsonify
from flask import request
from flask import Response

app = Flask(__name__)


@app.route('/api/account/logIn', methods=['POST'])
@app.route('/api/v1/account/logIn', methods=['POST'])
@app.route('/api/v1.0/account/logIn', methods=['POST'])
def log_in() -> Response:
    """Log in"""
    data = json.loads(request.data)

    email = data['email']
    password = data['password']

    if email == 'admin@teacup.com' and password == 'password':
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
    return Response()


@app.route('/api/account/signUp')
@app.route('/api/v1/account/signUp')
@app.route('/api/v1.0/account/signUp')
def sign_up() -> Response:
    """Sign up"""
    return Response()


if __name__ == '__main__':
    app.run()
