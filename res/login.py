from flask_jwt import JWT,JWTError, jwt_required
from flask_restful import Resource, reqparse, Api
from model.user import User
from flask import app, jsonify, redirect
import model.user_token
from model.user_token import *
from werkzeug.security import safe_str_cmp
from collections import OrderedDict
# from res.user_res import UserRegister
import datetime


# parser = reqparse.RequestParser()
# parser.add_argument("username", type=str, help="Username")
# parser.add_argument("password", type=str, help="Password")
parser = reqparse.RequestParser()
# parser.add_argument(name="id_user", type=str, location="json")
parser.add_argument(name="name", type=str, location="json")
parser.add_argument(name="password", type=str, location="json")

class LoginCredentials(Resource):
    def __init__(self,id,username, password):
        self.id = id;
        self.username = username;
        self.password = password;

    def authenticate(username, password):
        for user in User.objects().filter(name=username):
            if user.password == password:
                return LoginCredentials(str(user.id),user.name,user.pass_word)

    def identity(payload):
        user_id = payload["identity"]
        user = User.objects().with_id(user_id)
        if (user_id is not None):
            return LoginCredentials(str(user.id),user.name, user.pass_word)

def handle_user_exception_again(e):
    if isinstance(e, JWTError):
        return jsonify(OrderedDict([
            ('status_code', e.status_code),
            ('error', e.error),
            ('description', e.description),
        ])), e.status_code, e.headers
    return e

class RegisterRes(Resource):
    def post(self):
        body = parser.parse_args()
        # id_user = body.id_user
        name = body.name
        password = body.password
        # old_user = User.objects(name=name).first()
        # print("REGISTER SAVE")
        # if old_user is not None:
        #     return {"code":0,"Message":"User already exists", "token":""}, 400
        print("REGISTER SAVE")
        user = User(name = name, pass_word = password, token = model.user_token.generate())
        print({"name": user.name+";password:"+user.pass_word+";token:"+user.token})
        user.save()
        return redirect('api/login', 307)

def authenticate(username, password):
    print("Authenticate register")
    for user in User.objects(name=username):
        if user.pass_word == password:
            if safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
                print("OK")
                return LoginCredentials(str(user.id), user.name, user.password)


def identity(payload):
    print("Identity register")
    user_id = payload['identity']
    user = User.objects.with_id(user_id)
    if user is not None:
        return LoginCredentials(str(user.id), user.name, user.pass_word)

def jwt_init(app):
    # print("JWT_Init app")
    # def print():
    #     user = User(name="khanhpham", pass_word="phamdinhkhanh")
    #     user.save()
    #     for user in User.objects():
    #         print(user.name + user.pass_word)
    app.config['SECRET_KEY'] = 'khanh'
    app.config["JWT_EXPIRATION_DELTA"] = datetime.timedelta(hours=24)
    app.config["JWT_AUTH_URL_RULE"] = "/api/login"
    # Catch exception and return it to users
    # https://github.com/mattupstate/flask-jwt/issues/32
    app.handle_user_exception = handle_user_exception_again
    jwt = JWT(app=app,
              authentication_handler=authenticate,
              identity_handler=identity)
    return jwt
