import datetime
import json
from functools import wraps

from flask import jsonify, current_app, request
from flask_restful import Resource, abort, reqparse
import jwt

from application.models import User


def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):

        if not request.headers.get('Authorization'):
            abort(401)

        token = request.headers.get('Authorization')

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')
        except jwt.DecodeError:
            abort(401)
        except jwt.ExpiredSignatureError:
            abort(401)

        if payload['role'] != 'admin':
            abort(403)

        return f(*args, **kwargs)

    return decorated_func


class UserList(Resource):
    method_decorators = [login_required]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user', required=True, dest='user_name')
        parser.add_argument('password', required=True)
        parser.add_argument('role')
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('email', required=True)

        args = parser.parse_args()

        user = User(user_name=args['user_name'], role=args['role'], first_name=args['first_name'],
                    last_name=args['last_name'], email=args['email'])
        user.hash_password(args['password'])

        user.save()

        return "User {user_id} created".format(user_id=user.user_name), 201


class Users(Resource):
    method_decorators = [login_required]

    def get(self, user_id):

        user = User.objects.get_or_404(user_name=user_id)

        return jsonify(json.loads(user.to_json()))

    def put(self, user_id):

        user = User.objects.get_or_404(user_name=user_id)

        parser = reqparse.RequestParser()
        parser.add_argument('password')
        parser.add_argument('role')

        args = parser.parse_args()

        if 'role' in args and args['role'] is not None:
            user.role = args['role']

        if 'password' in args and args['password'] is not None:
            user.hash_password(args['password'])

        user.save()

        return "User {user_id} updated".format(user_id=user.user_name), 204


class Authentications(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args()

        user = User.objects.get_or_404(user_name=args['user'])

        if user.verify_password(args['password']) is False:
            abort(403)

        payload = {
            'sub': user.user_name,
            'exp': datetime.datetime.now() + datetime.timedelta(days=1),
            'role': user.role
        }

        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

        return token.decode('unicode_escape'), 201
