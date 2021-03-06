# encoding: utf-8
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
from config import app,jwt
import flask.ext.restless
from models import db,User,Role
import io 
import sys
import datetime
import pymysql
from flask import Flask, request, jsonify
import flask_sqlalchemy 
import flask_restless
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from werkzeug.security import safe_str_cmp,generate_password_hash,check_password_hash 


# Create the Flask application and the Flask-SQLAlchemy object.
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
# 
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
        print(user.password.encode('utf-8'))
        ret = {
        'access_token': create_access_token(identity=username),
        'refresh_token': create_refresh_token(identity=username),
        'userID': user.id,
    }
        return jsonify(ret), 200
    else: 
        return jsonify({'error': '错误'}), 401
################################################################################################################

from flask_restless import ProcessingException
@jwt_required    
def get_single_preprocessor(resource_id=None, **kw):
    """Accepts a single argument, `instance_id`, the primary key of the
    instance of the model to get.
 
    """
    users = User.query.all()
    username_table = {u.username: u for u in users} 
    current_user = get_jwt_identity()
    print('hello, world',current_user)
    print(resource_id)
    user = username_table.get(current_user, None) 
    print(user.id)
    if not user.id == int(resource_id):
        raise ProcessingException(code='405', detail='Not Authorized', status=401)


@jwt_required
def pre_get_single(**kw): pass


@jwt_required
def auth_admin_func(instance_id=None, **kwargs):
    current_user = get_jwt_identity()
    if not current_user == "jim":

        raise ProcessingException(description='Only admins can access this view', code=401)


################################################################################################################
def post_processors_func_get_many(instance_id=None, **kwargs):
    print("GET_MANY后处理.....")
################################################################################################################
# manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
# manager.create_api(User, methods=['GET', 'POST', 'PUT', 'DELETE'],
#                    preprocessors=dict(GET_RESOURCE=[get_single_preprocessor],
#                                       GET_COLLECTION=[auth_admin_func],
#                                       PUT_SINGLE=[get_single_preprocessor],
#                                       POST=[auth_admin_func]),
#                    postprocessors=dict(GET_MANY=[post_processors_func_get_many]),)
#  nclude_columns=['id', 'username','password', 'role', 'userrole'] ##########################

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
preprocessors = {'GET_COLLECTION': [auth_admin_func], 'GET_RESOURCE': [get_single_preprocessor]}
manager.create_api(User, page_size=2,
                   exclude=['password'],
                   collection_name='users',
                   methods=['GET', 'POST', 'PUT', 'DELETE'],
                   preprocessors=preprocessors)
manager.create_api(Role, collection_name='rolessss', methods=['GET', 'POST', 'PUT', 'DELETE'])
if __name__ == '__main__':
    app.run(port=1000)
