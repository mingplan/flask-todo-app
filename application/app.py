# -*- coding: utf-8 -*-

from flask import Flask
from controllers import blueprints
from configs import config
from extensions import db, api
from application.controllers.api import api_v1

def create_app(config_name=None):
    if config_name is None:
        config_name = 'default'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # db
    db.init_app(app)

    # flask rest-plus

    api.init_app(app, version='1.0', title='Todo API',
                 description='A simple TODO API')

    # blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
