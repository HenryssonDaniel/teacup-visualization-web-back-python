#!/usr/bin/env
# -*- coding: utf-8 -*-
"""Account tests"""

from flask import Flask, Response
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer
from unittest import mock
from unittest.mock import MagicMock

import flaskr.account
import unittest

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
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
        if '/api/account/changePassword' in arg or '/api/account/signUp' in arg:
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
        self.assertEqual(client.get('/api/account/authorized').status_code, 200)

    def test_authorized_false(self) -> None:
        self.assertEqual(app.test_client().get('/api/account/authorized').status_code, 401)

    @mock.patch('requests.post', return_value=MockResponse({"email": "email", "firstName": "firstName", "id": "id",
                                                            "lastName": "lastName"}, 200))
    def test_change_password(self, _) -> None:
        token = URLSafeTimedSerializer(app.config['SECRET_KEY']).dumps('test@teacup.com')
        self.assertEqual(app.test_client().post('/api/account/changePassword',
                                                data='{"password": "password", "token": "' + token + '"}').status_code,
                         200)

    @mock.patch('requests.post', side_effect=__mocked_requests_post_log_in_error)
    def test_change_password_log_in_error(self, _) -> None:
        token = URLSafeTimedSerializer(app.config['SECRET_KEY']).dumps('test@teacup.com')
        self.assertEqual(app.test_client().post('/api/account/changePassword',
                                                data='{"password": "password", "token": "' + token + '"}').status_code,
                         400)

    @mock.patch('requests.post', return_value=Response(status=500))
    def test_change_password_request_error(self, _) -> None:
        token = URLSafeTimedSerializer(app.config['SECRET_KEY']).dumps('test@teacup.com')
        self.assertEqual(app.test_client().post('/api/account/changePassword',
                                                data='{"password": "password", "token": "' + token + '"}').status_code,
                         500)

    def test_change_password_token_error(self) -> None:
        self.assertEqual(app.test_client().post('/api/account/changePassword', data='{"token": "test"}').status_code,
                         403)

    def test_change_password_false(self) -> None:
        client = app.test_client()
        self.__set_session_id(client)
        self.assertEqual(client.post('/api/account/changePassword').status_code, 403)

    @mock.patch('requests.post', return_value=MockResponse({"email": "email", "firstName": "firstName", "id": "id",
                                                            "lastName": "lastName"}, 200))
    def test_log_in(self, _) -> None:
        self.assertEqual(app.test_client().post('/api/account/logIn',
                                                data='{"email": "email", "password": "password"}').status_code,
                         200)

    @mock.patch('requests.post', side_effect=__mocked_requests_post_log_in_error)
    def test_log_in_error(self, _) -> None:
        self.assertEqual(app.test_client().post('/api/account/logIn',
                                                data='{"email": "email", "password": "password"}').status_code,
                         400)

    def test_log_in_false(self) -> None:
        client = app.test_client()
        self.__set_session_id(client)
        self.assertEqual(client.post('/api/account/logIn').status_code, 403)

    def test_log_out(self) -> None:
        client = app.test_client()
        self.__set_session_id(client)
        self.assertEqual(client.post('/api/account/logOut').status_code, 200)

    def test_log_out_false(self) -> None:
        self.assertEqual(app.test_client().post('/api/account/logOut').status_code, 401)

    @mock.patch('requests.post', return_value=Response())
    @mock.patch('smtplib.SMTP', return_value=MagicMock())
    def test_recover(self, _, __) -> None:
        self.assertEqual(app.test_client().post('/api/account/recover', data='{"email": "email"}').status_code, 200)

    @mock.patch('requests.post', return_value=Response(status=500))
    def test_recover_error(self, _) -> None:
        self.assertEqual(app.test_client().post('/api/account/recover', data='{"email": "email"}').status_code, 500)

    def test_recover_false(self) -> None:
        client = app.test_client()
        self.__set_session_id(client)
        self.assertEqual(client.post('/api/account/recover').status_code, 403)

    @mock.patch('requests.post', return_value=MockResponse({"email": "email", "firstName": "firstName", "id": "id",
                                                            "lastName": "lastName"}, 200))
    @mock.patch('smtplib.SMTP', return_value=MagicMock())
    def test_sign_up(self, _, __) -> None:
        self.assertEqual(app.test_client().post('/api/account/signUp',
                                                data='{"email": "email", "password": "password"}').status_code, 200)

    @mock.patch('requests.post', side_effect=__mocked_requests_post_log_in_error)
    @mock.patch('smtplib.SMTP', return_value=MagicMock())
    def test_sign_up_log_in_error(self, _, __) -> None:
        self.assertEqual(app.test_client().post('/api/account/signUp',
                                                data='{"email": "email", "password": "password"}').status_code, 400)

    @mock.patch('requests.post', return_value=Response(status=500))
    def test_sign_up_error(self, _) -> None:
        self.assertEqual(app.test_client().post('/api/account/signUp', data='{"email": "email"}').status_code, 500)

    def test_sign_up_false(self) -> None:
        client = app.test_client()
        self.__set_session_id(client)
        self.assertEqual(client.post('/api/account/signUp').status_code, 403)

    @mock.patch('requests.post', return_value=Response(status=200))
    def test_verify(self, _) -> None:
        token = URLSafeSerializer(app.config['SECRET_KEY']).dumps('test@teacup.com')
        self.assertEqual(app.test_client().get('/api/account/verify/' + token).data, b'The account have been verified')

    @mock.patch('requests.post', return_value=Response(status=500))
    def test_verify_error(self, _) -> None:
        token = URLSafeSerializer(app.config['SECRET_KEY']).dumps('test@teacup.com')
        self.assertEqual(app.test_client().get('/api/account/verify/' + token).data,
                         b'The account could not be verified, please try again later')

    def test_verify_bad_token(self) -> None:
        self.assertEqual(app.test_client().get('/api/account/verify/token').data, b'The token is not valid')

    @staticmethod
    def __set_session_id(client) -> None:
        with client.session_transaction() as session:
            session['id'] = 'test'


if __name__ == '__main__':
    unittest.main()
