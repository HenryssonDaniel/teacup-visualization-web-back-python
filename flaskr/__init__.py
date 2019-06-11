#!/usr/bin/env
# -*- coding: utf-8 -*-
"""Initialize the application"""

from flask import Flask
from flask_cors import CORS
from flask_session import Session


def create_app(test_config=None) -> Flask:
    """Create the application"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SERVICE_REPORT='http://localhost:8080/mysql',
        SERVICE_VISUALIZATION='http://localhost:8080/mysql',
        SESSION_TYPE='filesystem',
        SMTP_FROM='noreply@teacup.com',
        SMTP_HOST='localhost',
        SMTP_PORT='1025'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    CORS(app)
    Session(app)

    from . import account, dashboard
    app.register_blueprint(account.blueprint)
    app.register_blueprint(dashboard.blueprint)

    return app
