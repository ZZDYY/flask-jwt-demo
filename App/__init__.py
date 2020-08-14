# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 10:39
# @Author  : CMJ
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Flask as _Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restplus import Api
from .config import config_by_name
import json
db = SQLAlchemy()
flask_bcrypt = Bcrypt()
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(title='FLASK RESTPLUS API WITH JWT',
          version='1.0',
          description='a flask restplus web service',
          authorizations=authorizations
          )




def register_blueprint(app):
    from App.controller import main
    app.register_blueprint(main, url_prefix="")


# 返回结果序列化
from datetime import date
from flask.json import JSONEncoder as _JSONEncoder
class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, o)


class Flask(_Flask):
    json_encoder = JSONEncoder

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    api.init_app(app)
    flask_bcrypt.init_app(app)
    register_blueprint(app)

    return app