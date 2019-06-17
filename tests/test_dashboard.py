#!/usr/bin/env
# -*- coding: utf-8 -*-
"""Dashboard tests"""

from flask import Flask, Response
from unittest import mock

import flaskr.dashboard
import unittest

DASHBOARD = '/api/dashboard'
GET = 'requests.get'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SERVICE_REPORT'] = 'http://localhost:8080/mysql'
app.register_blueprint(flaskr.dashboard.blueprint)


class MockResponse:
    """Mock response"""
    def __init__(self, json_data, status_code) -> None:
        self.json_data = json_data
        self.status_code = status_code

    def json(self) -> str:
        """Json"""
        return self.json_data


class TestInit(unittest.TestCase):
    @mock.patch(GET, return_value=MockResponse({"sessions": []}, 200))
    def test_dashboard(self, _) -> None:
        client = app.test_client()
        self.__set_session_id(client)
        self.assertEqual(client.get(DASHBOARD).status_code, 200)

    @mock.patch(GET, return_value=Response(status=500))
    def test_dashboard_error(self, _) -> None:
        client = app.test_client()
        self.__set_session_id(client)
        self.assertEqual(client.get(DASHBOARD).status_code, 500)

    def test_dashboard_unauthorized(self) -> None:
        self.assertEqual(app.test_client().get(DASHBOARD).status_code, 401)

    @staticmethod
    def __set_session_id(client) -> None:
        with client.session_transaction() as session:
            session['firstName'] = 'test'
            session['id'] = 'test'
            session['lastName'] = 'test'


if __name__ == '__main__':
    unittest.main()
