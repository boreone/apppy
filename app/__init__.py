# app/__init__.py
import os
import io
import sys
import datetime
import pymysql
from flask import Flask, request, jsonify
import flask_sqlalchemy
from instance.config import app_config

app = Flask(__name__,instance_relative_config=True)
app.config.from_object(app_config['development'])
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = 'all'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=10)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=100)
db = flask_sqlalchemy.SQLAlchemy(app, use_native_unicode='utf8')
