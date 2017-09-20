# app/__init__.py

import io
import sys
import datetime
import pymysql
from flask import Flask, request, jsonify
import flask_sqlalchemy
# from flask.ext.sqlalchemy import SQLAlchemy
import flask_restless

from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from instance.config import app_config


def create_app(config_name):

    app = Flask(__name__)
    app.secret_key = 'super_secret_xyzXYZ_xyzXYZ@xyzXYZ_123'
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = 'all'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=10)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=100)
    jwt = JWTManager(app)

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/app?charset=utf8'
    # 最新版本已经移除？app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    return app

db = flask_sqlalchemy.SQLAlchemy(create_app, use_native_unicode='utf8')
