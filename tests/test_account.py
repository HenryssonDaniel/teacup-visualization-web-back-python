#!/usr/bin/env
# -*- coding: utf-8 -*-
"""Account tests"""

from flask import Flask, Response
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer
from unittest import mock
from unittest.mock import MagicMock

import flaskr.account
import unittest

ACCOUNT = {"email": "email", "firstName": "firstName", "id": "id", "lastName": "lastName"}
AUTHORIZED = '/api/account/authorized'
CHANGE_PASSWORD = '/api/account/changePassword'
EMAIL_DATA = '{"email": "email"}'
LOG_IN = '/api/account/logIn'
LOG_IN_DATA = '{"email": "email", "password": "password"}'
LOG_OUT = '/api/account/logOut'
PASSWORD_TOKEN = '{"password": "password", "token": "'
POST = 'requests.post'
RECOVER = '/api/account/recover'
SECRET_KEY = 'SECRET_KEY'
SIGN_UP = '/api/account/signUp'
SMTP = 'smtplib.SMTP'
TEST_EMAIL = 'test@teacup.com'
VERIFY = '/api/account/verify/'

app = Flask(__name__)
app.config[SECRET_KEY] = 'dev'
app.config['SERVICE_VISUALIZATION'] = 'http://localhost:8080/mysql'
app.config['SMTP_FROM'] = 'noreply@teacup.com'
app.config['SMTP_HOST'] = 'localhost'
app.config['SMTP_PORT'] = '1025'
app.register_blueprint(flaskr.account.blueprint)


class MockResponse:
    """Mock response"""
    def __init__(self, json_data, status_code) -> None:
        self.json_data = json_data
        self.status_code = status_code

    def json(self) -> str:
        """Json"""
        return self.json_data


class TestInit(unittest.TestCase):
    def __mocked_requests_post_log_in_error(*args, **_) -> MockResponse:
        arg = args[0]
        if CHANGE_PASSWORD in arg or SIGN_UP in arg:
            status_code = 200
        else:
            status_code = 400

        return MockResponse(None, status_code)

    def test_user_required(self) -> None:
        name = "name"

        view = MagicMock()
        view.__name__ = name

        self.assertEqual(flaskr.account.user_required(view).__name__, name)

    def test_authorized(self) -> None:
        client = app.test_client()
        self.__set_session_id(client)
        self.assertEqual(client.get(AUTHORIZED).status_code, 200)

    def test_authorized_false(self) -> None:
        self.assertEqual(app.test_client().get(AUTHORIZED).status_code, 401)

    @mock.patch(POST, return_value=MockResponse(ACCOUNT, 200))
    def test_change_password(self, _) -> None:
        self.assertEqual(app.test_client().post(CHANGE_PASSWORD,
                                                data=PASSWORD_TOKEN + self.__create_timed_token() + '"}').status_code,
                         200)

    @mock.patch(POST, side_effect=__mocked_requests_post_log_in_error)
    def test_change_password_log_in_error(self, _) -> None:
        self.assertEqual(app.test_client().post(CHANGE_PASSWORD,
                                                data=PASSWORD_TOKEN + self.__create_timed_token() + '"}').status_code,
                         400)

    @mock.patch(POST, return_value=Response(status=500))
    def test_change_password_request_error(self, _) -> None:
        self.assertEqual(app.test_client().post(CHANGE_PASSWORD,
                                                data=PASSWORD_TOKEN + self.__create_timed_token() + '"}').status_code,
                         500)

    def test_change_password_token_error(self) -> None:
        self.assertEqual(app.test_client().post(CHANGE_PASSWORD, data='{"token": "test"}').status_code, 403)

    def test_change_password_false(self) -> None:
        client = app.test_client()
        self.__set_session_id(client)
        self.assertEqual(client.post(CHANGE_PASSWORD).status_code, 403)

    @mock.patch(POST, return_value=MockResponse(ACCOUNT, 200))
    def test_log_in(self, _) -> None:
        self.assertEqual(app.test_client().post(LOG_IN, data=LOG_IN_DATA).status_code, 200)

    @mock.patch(POST, side_effect=__mocked_requests_post_log_in_error)
    def test_log_in_error(self, _) -> None:
        self.assertEqual(app.test_client().post(LOG_IN, data=LOG_IN_DATA).status_code, 400)

    def test_log_in_false(self) -> None:
        client = app.test_client()
        self.__set_session_id(client)
        self.assertEqual(client.post(LOG_IN).status_code, 403)

    def test_log_out(self) -> None:
        client = app.test_client()
        self.__set_session_id(client)
        self.assertEqual(client.post(LOG_OUT).status_code, 200)

    def test_log_out_false(self) -> None:
        self.assertEqual(app.test_client().post(LOG_OUT).status_code, 401)

    @mock.patch(POST, return_value=Response())
    @mock.patch(SMTP, return_value=MagicMock())
    def test_recover(self, _, __) -> None:
        self.assertEqual(app.test_client().post(RECOVER, data=EMAIL_DATA).status_code, 200)

    @mock.patch(POST, return_value=Response(status=500))
    def test_recover_error(self, _) -> None:
        self.assertEqual(app.test_client().post(RECOVER, data=EMAIL_DATA).status_code, 500)

    def test_recover_false(self) -> None:
        client = app.test_client()
        self.__set_session_id(client)
        self.assertEqual(client.post(RECOVER).status_code, 403)

    @mock.patch(POST, return_value=MockResponse(ACCOUNT, 200))
    @mock.patch(SMTP, return_value=MagicMock())
    def test_sign_up(self, _, __) -> None:
        self.assertEqual(app.test_client().post(SIGN_UP, data=LOG_IN_DATA).status_code, 200)

    @mock.patch(POST, side_effect=__mocked_requests_post_log_in_error)
    @mock.patch(SMTP, return_value=MagicMock())
    def test_sign_up_log_in_error(self, _, __) -> None:
        self.assertEqual(app.test_client().post(SIGN_UP, data=LOG_IN_DATA).status_code, 400)

    @mock.patch(POST, return_value=Response(status=500))
    def test_sign_up_error(self, _) -> None:
        self.assertEqual(app.test_client().post(SIGN_UP, data=EMAIL_DATA).status_code, 500)

    def test_sign_up_false(self) -> None:
        client = app.test_client()
        self.__set_session_id(client)
        self.assertEqual(client.post(SIGN_UP).status_code, 403)

    @mock.patch(POST, return_value=Response(status=200))
    def test_verify(self, _) -> None:
        self.assertEqual(app.test_client().get(VERIFY + self.__create_token()).data, b'The account have been verified')

    @mock.patch(POST, return_value=Response(status=500))
    def test_verify_error(self, _) -> None:
        self.assertEqual(app.test_client().get(VERIFY + self.__create_token()).data,
                         b'The account could not be verified, please try again later')

    def test_verify_bad_token(self) -> None:
        self.assertEqual(app.test_client().get('%stoken' % VERIFY).data, b'The token is not valid')

    @staticmethod
    def __create_timed_token() -> str:
        return URLSafeTimedSerializer(app.config[SECRET_KEY]).dumps(TEST_EMAIL)

    @staticmethod
    def __create_token() -> str:
        return URLSafeSerializer(app.config[SECRET_KEY]).dumps(TEST_EMAIL)

    @staticmethod
    def __set_session_id(client) -> None:
        with client.session_transaction() as session:
            session['id'] = 'test'


if __name__ == '__main__':
    unittest.main()
