#!/usr/bin/env
# -*- coding: utf-8 -*-
"""Account API"""

from email.message import EmailMessage
from flask import Blueprint, current_app as app, json, jsonify, request, Response, session
from itsdangerous import BadSignature
from itsdangerous import URLSafeSerializer

import requests
import smtplib

blueprint = Blueprint('account', __name__, url_prefix='/api')


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


@blueprint.route('/account/authorized', methods=['GET'])
@blueprint.route('/v1/account/authorized', methods=['GET'])
@blueprint.route('/v1.0/account/authorized', methods=['GET'])
@user_required
def authorized() -> Response:
    """Log in"""
    response = Response()
    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response


@blueprint.route('/account/logIn', methods=['POST'])
@blueprint.route('/v1/account/logIn', methods=['POST'])
@blueprint.route('/v1.0/account/logIn', methods=['POST'])
def log_in() -> Response:
    """Log in"""
    response = Response(status=log_in_data(json.loads(request.data)))
    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response


def log_in_data(data) -> int:
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

    return status


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

    status = requests.post('http://localhost:8080/mysql/api/account/signUp', data=json.dumps(data),
                           headers={'content-type': 'application/json'}).status_code
    if status == 200:
        email = data["email"]

        email_message = EmailMessage()
        email_message.set_content("Please verify your account by clicking here: " + request.url_root +
                                  "api/account/verify/" + URLSafeSerializer(app.config['SECRET_KEY']).dumps(email))

        email_message['Subject'] = 'Verify your Teacup account'
        email_message['From'] = 'noreply@teacup.com'
        email_message['To'] = email

        smtp = smtplib.SMTP('localhost', 1025)
        smtp.send_message(email_message)
        smtp.quit()

        status = log_in_data({"email": email, "password": data["password"]})

    response = Response(status=status)
    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response


@blueprint.route('/account/verify/<token>', methods=['GET'])
@blueprint.route('/v1/account/verify/<token>', methods=['GET'])
@blueprint.route('/v1.0/account/verify/<token>', methods=['GET'])
def verify(token) -> str:
    """Verify"""
    try:
        email = URLSafeSerializer(app.config['SECRET_KEY']).loads(token)
        status = requests.post('http://localhost:8080/mysql/api/account/verify', data=json.dumps({"email": email}),
                               headers={'content-type': 'application/json'}).status_code

        if status == 200:
            message = 'The account have been verified'
        else:
            message = 'The account could not be verified, please try again later'
    except BadSignature:
        message = 'The token is not valid'

    return message
