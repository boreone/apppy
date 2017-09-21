# encoding: utf-8
import flask_restless
from flask import request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from app.models import *

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
# from app import db,User,Role,tags

# config_name = "development"

jwt = JWTManager(app)
# Create the Flask application and the Flask-SQLAlchemy object.
################################################################################################################
#
# db.drop_all()
# db.create_all()
#
# role_admin = Role(name=u'Admin')
# user_tom = User(username=u'tom',password=generate_password_hash('abc'),role=role_admin,userrole=1)
# db.session.add(user_tom )
# user_jim = User(username=u'jim',password=generate_password_hash('abc'),role=role_admin,userrole=1)
# user_tim = User(username=u'tim',password=u'abc',role=role_admin,userrole=1)
# user_sam = User(username=u'sam',password=u'abc',role=role_admin,userrole=4)
# user_gas = User(username=u'gas',password=u'打开',role=role_admin,userrole=5)
# db.session.commit()
#######################################################################################################

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
    只能同过API/1...来访问单个内容
    另：使用手机做用户名登录好处就是不用再来做不要的查询了。直接判断current_user == instance_id 即可。
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
# 此处控制不返回用户密码### include_columns=['id', 'username','password', 'role', 'userrole'] ##########################






#config_name = os.getenv('APP_SETTINGS') # config_name = "development"

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
preprocessors = {'GET_COLLECTION': [auth_admin_func], 'GET_RESOURCE': [get_single_preprocessor]}
manager.create_api(User, page_size=2,
                   exclude=['password'],
                   preprocessors=preprocessors,
                   collection_name='users',
                   methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Role, collection_name='roles', methods=['GET', 'POST', 'PUT', 'DELETE'])
# http://127.0.0.1:1000/api/rolessss/1/users

if __name__ == '__main__':
    app.run(port=2020)