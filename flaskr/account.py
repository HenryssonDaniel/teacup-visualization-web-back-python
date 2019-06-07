#!/usr/bin/env
# -*- coding: utf-8 -*-
"""Account API"""

from email.message import EmailMessage
from flask import Blueprint, current_app as app, json, request, Response, session
from itsdangerous import BadSignature
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer

import requests
import smtplib

blueprint = Blueprint('account', __name__, url_prefix='/api')


def user_required(view) -> Response:
    """User required"""
    def wrapped_user_view(**kwargs) -> Response:
        """Wrapper view"""
        if 'id' in session:
            return view(**kwargs)

        response = Response(status=401)
        response.headers.add('Access-Control-Allow-credentials', 'true')

        return response

    wrapped_user_view.__name__ = view.__name__
    return wrapped_user_view


def __no_user_required(view) -> Response:
    """No user required"""
    def wrapped_no_user_view(**kwargs) -> Response:
        """Wrapper view"""
        if 'id' in session:
            response = Response(status=403)
            response.headers.add('Access-Control-Allow-credentials', 'true')

            return response

        return view(**kwargs)

    wrapped_no_user_view.__name__ = view.__name__
    return wrapped_no_user_view


@blueprint.route('/account/authorized', methods=['GET'])
@blueprint.route('/v1/account/authorized', methods=['GET'])
@blueprint.route('/v1.0/account/authorized', methods=['GET'])
@user_required
def authorized() -> Response:
    """Log in"""
    response = Response()
    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response


@blueprint.route('/account/changePassword', methods=['POST'])
@blueprint.route('/v1/account/changePassword', methods=['POST'])
@blueprint.route('/v1.0/account/changePassword', methods=['POST'])
@__no_user_required
def change_password() -> Response:
    """Log in"""
    data = json.loads(request.data)

    try:
        email = URLSafeTimedSerializer(app.config['SECRET_KEY']).loads(data["token"], max_age=3600)
        password = data["password"]

        status = requests.post(app.config['SERVICE_VISUALIZATION'] + '/api/account/changePassword',
                               data=json.dumps({"authorized": False, "email": email, "password": password}),
                               headers={'content-type': 'application/json'}).status_code

        if status == 200:
            status = __log_in_data({"email": email, "password": password})
    except BadSignature:
        status = 403

    response = Response(status=status)
    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response


@blueprint.route('/account/logIn', methods=['POST'])
@blueprint.route('/v1/account/logIn', methods=['POST'])
@blueprint.route('/v1.0/account/logIn', methods=['POST'])
@__no_user_required
def log_in() -> Response:
    """Log in"""
    response = Response(status=__log_in_data(json.loads(request.data)))
    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response


@blueprint.route('/account/logOut', methods=['POST'])
@blueprint.route('/v1/account/logOut', methods=['POST'])
@blueprint.route('/v1.0/account/logOut', methods=['POST'])
@user_required
def log_out() -> Response:
    """Log out"""
    session.pop('id')

    response = Response()
    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response


@blueprint.route('/account/recover', methods=['POST'])
@blueprint.route('/v1/account/recover', methods=['POST'])
@blueprint.route('/v1.0/account/recover', methods=['POST'])
@__no_user_required
def recover() -> Response:
    """Recover account"""
    data = json.loads(request.data)

    status = requests.post(app.config['SERVICE_VISUALIZATION'] + '/api/account/recover', data=json.dumps(data),
                           headers={'content-type': 'application/json'}).status_code

    if status == 200:
        email = data["email"]
        __send_email("The recover code: " + URLSafeTimedSerializer(app.config['SECRET_KEY']).dumps(email),
                     'Recover', email)

    response = Response(status=status)
    response.headers.add('Access-Control-Allow-credentials', 'true')

    return response


@blueprint.route('/account/signUp', methods=['POST'])
@blueprint.route('/v1/account/signUp', methods=['POST'])
@blueprint.route('/v1.0/account/signUp', methods=['POST'])
@__no_user_required
def sign_up() -> Response:
    """Sign up"""
    data = json.loads(request.data)

    status = requests.post(app.config['SERVICE_VISUALIZATION'] + '/api/account/signUp', data=json.dumps(data),
                           headers={'content-type': 'application/json'}).status_code
    if status == 200:
        email = data["email"]

        __send_email("Please verify your account by clicking here: " + request.url_root + "api/account/verify/" +
                     URLSafeSerializer(app.config['SECRET_KEY']).dumps(email), 'Verify', email)

        status = __log_in_data({"email": email, "password": data["password"]})

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
        status = requests.post(app.config['SERVICE_VISUALIZATION'] + '/api/account/verify',
                               data=json.dumps({"email": email}),
                               headers={'content-type': 'application/json'}).status_code

        if status == 200:
            message = 'The account have been verified'
        else:
            message = 'The account could not be verified, please try again later'
    except BadSignature:
        message = 'The token is not valid'

    return message


def __log_in_data(data) -> int:
    """Log in with data"""
    response = requests.post(app.config['SERVICE_VISUALIZATION'] + '/api/account/logIn', data=json.dumps(data),
                             headers={'content-type': 'application/json'})

    status = response.status_code
    if status == 200:
        content = response.json()

        session['email'] = content["email"]
        session['firstName'] = content["firstName"]
        session['id'] = content["id"]
        session['lastName'] = content["lastName"]

    return status


def __send_email(content, subject, to) -> None:
    """Send email"""
    email_message = EmailMessage()
    email_message.set_content(content)

    email_message['Subject'] = subject + ' your Teacup account'
    email_message['From'] = app.config['SMTP_FROM']
    email_message['To'] = to

    smtp = smtplib.SMTP(app.config['SMTP_HOST'], app.config['SMTP_PORT'])
    smtp.send_message(email_message)
    smtp.quit()
