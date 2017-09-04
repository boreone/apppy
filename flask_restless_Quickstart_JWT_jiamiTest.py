# encoding: utf-8
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
from config import db,app,jwt
from models import User,Role

import io 
import sys
import datetime
import pymysql
from flask import Flask, request, jsonify
import flask_sqlalchemy 
#from flask.ext.sqlalchemy import SQLAlchemy
import flask_restless
 
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from werkzeug.security import safe_str_cmp,generate_password_hash,check_password_hash 


# Create the Flask application and the Flask-SQLAlchemy object.
'''
app = Flask(__name__)
app.secret_key = 'super-secret'
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = 'all'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=10)
jwt = JWTManager(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/restlessc?charset=utf8'
#最新版本已经移除？app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = flask_sqlalchemy.SQLAlchemy(app,use_native_unicode='utf8')

#db = SQLAlchemy(app)
# Create your Flask-SQLALchemy models as usual but with the following two
# (reasonable) restrictions:
#   1. They must have a primary key column of type sqlalchemy.Integer or
#      type sqlalchemy.Unicode.
#   2. They must have an __init__ method which accepts keyword arguments for
#      all columns (the constructor in flask.ext.sqlalchemy.SQLAlchemy.Model
#      supplies such a method, so you don't need to declare a new one).
'''
 

################################################################################################################
'''
db.drop_all()
db.create_all()
role_admin = Role(name=u'Admin')
user_tom = User(username=u'tom',password=generate_password_hash('abc'),role=role_admin,userrole=1)
db.session.add(user_tom )
user_jim = User(username=u'jim',password=generate_password_hash('abc'),role=role_admin,userrole=1)
user_tim = User(username=u'tim',password=u'abc',role=role_admin,userrole=1)
user_sam = User(username=u'sam',password=u'abc',role=role_admin,userrole=4)
user_gas = User(username=u'gas',password=u'打开',role=role_admin,userrole=5)
db.session.commit()
'''

'''
#这里是修改密码
users = User.query.all()
username_table = {u.username: u for u in users} 
user = username_table.get('gom', None) 

user.password = generate_password_hash('abcd')
db.session.add(user )
db.session.commit()
'''
################################################################################################################
@app.route('/login', methods=['POST'])
def login():
    users = User.query.all()
    username_table = {u.username: u for u in users} 
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = username_table.get(username, None) 
    print(user.password)
    if user and check_password_hash(user.password, password):
       # return jsonify({"msg": "Bad username or password"}), 401
        print(user.password.encode('utf-8'))
        ret = {
        'access_token': create_access_token(identity=username),
        'refresh_token': create_refresh_token(identity=username),
        'userID': user.id,
    }
        return jsonify(ret), 200
    else: 
        return jsonify({'error':'错误'}), 401
################################################################################################################

from flask_restless import ProcessingException
@jwt_required    
def get_single_preprocessor(instance_id=None, **kw):
    """Accepts a single argument, `instance_id`, the primary key of the
    instance of the model to get.
    只能同过API/1...来访问单个内容
    另：使用手机做用户名登录好处就是不用再来做不要的查询了。直接判断current_user == instance_id 即可。
    """
    users = User.query.all()
    username_table = {u.username: u for u in users} 
    current_user = get_jwt_identity()
    print('hello, world',current_user)
    print(instance_id)
    user = username_table.get(current_user, None) 
    print(user.id)
    if not user.id == int(instance_id):
#   if not is_authorized_to_modify(current_user, instance_id): 
       raise ProcessingException(description=u'qing zhu ce',code=401) 
        #response = {'access_token': '111111',}
        #return  False
        #return  {'message': 'ProgrammingError11111111111',}

#   pass
@jwt_required  
def pre_get_single(**kw): pass
 
"""
def is_authorized(user, instance):
    return int(user.id) == int(instance)
@jwt_required
def auth_user_func(instance_id=None, **kwargs):
    del kwargs
    if not is_authorized(get_jwt_identity(), instance_id):
        raise ProcessingException(description='Not Authorized', code=401)
    """
@jwt_required
def auth_admin_func(instance_id=None, **kwargs):
#    del instance_id
#    del kwargs
    current_user = get_jwt_identity()
    if not current_user == "tom":

        raise ProcessingException(description='Only admins can access this view', code=401)


################################################################################################################
def post_processors_func_get_many(instance_id=None, **kwargs):
    print("GET_MANY后处理.....")
#   user_tompsot = User(username=u'tompsot',password=u'abc',role=role_admin,userrole=10)
#   db.session.add(user_tompsot )
#   db.session.commit()
################################################################################################################
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(User, methods=['GET', 'POST','PUT', 'DELETE'],
                    preprocessors=dict(GET_SINGLE=[get_single_preprocessor],
                        GET_MANY=[auth_admin_func],
                        PUT_SINGLE=[get_single_preprocessor],
                        POST=[auth_admin_func]
                        ),
                    postprocessors=dict(GET_MANY=[post_processors_func_get_many]
                        ),
                    include_columns=['id', 'username','password', 'role', 'userrole']##########此处控制不返回用户密码#############################
                   )

'''
import asyncio, os, json, time
loop = asyncio.get_event_loop()
loop.run_until_complete(app.run())
loop.run_forever()
'''

if __name__ == '__main__':
    app.run()