# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api
from controllers import blueprints
from configs import config
from extensions import db
from application.controllers.api import Todo, TodoList


def create_app(config_name=None):
    if config_name is None:
        config_name = 'default'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # db
    db.init_app(app)

    # blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    # flask restful plugin

    api = Api(app)

    api.add_resource(TodoList, '/todos')
    api.add_resource(Todo, '/todos/<string:todo_id>')

    return app
