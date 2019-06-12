#!/usr/bin/env
# -*- coding: utf-8 -*-
"""Init tests"""

from unittest.mock import MagicMock
from flask import Flask

import flaskr.__init__
import flaskr.account
import flaskr.dashboard
import unittest


class TestInit(unittest.TestCase):
    def test_create_app(self) -> None:
        flask = flaskr.__init__.create_app()

        self.assertEqual(flask.config.get('SECRET_KEY'), 'dev')
        self.assertEqual(flask.config.get('SERVICE_REPORT'), 'http://localhost:8080/mysql')
        self.assertEqual(flask.config.get('SERVICE_VISUALIZATION'), 'http://localhost:8080/mysql')
        self.assertEqual(flask.config.get('SESSION_TYPE'), 'filesystem')
        self.assertEqual(flask.config.get('SMTP_FROM'), 'noreply@teacup.com')
        self.assertEqual(flask.config.get('SMTP_HOST'), 'localhost')
        self.assertEqual(flask.config.get('SMTP_PORT'), '1025')

        blueprints = flask.blueprints

        self.assertEqual(len(blueprints), 2)
        self.assertIsNotNone(blueprints.get('account'))
        self.assertIsNotNone(blueprints.get('dashboard'))

    def test_create_app_with_config(self) -> None:
        self.assertIsInstance(flaskr.__init__.create_app(MagicMock()), Flask)


if __name__ == '__main__':
    unittest.main()
