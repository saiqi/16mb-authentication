import datetime
import json
from functools import wraps
import string
import random

from flask import jsonify, current_app, request
from flask_restful import Resource, abort, reqparse
import jwt

from application.models import User
from application.mail import send_mail


def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):

        if not request.headers.get('Authorization'):
            abort(401)

        token = request.headers.get('Authorization')

        try:
            payload = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms='HS256')
        except jwt.DecodeError:
            abort(401)
        except jwt.ExpiredSignatureError:
            abort(401)

        if payload['role'] != 'admin':
            abort(403)

        return f(*args, **kwargs)

    return decorated_func


def random_password():
    min_length = 8
    max_length = 12
    choices = string.ascii_letters + string.punctuation + string.digits
    return "".join(random.choice(choices) for x in range(random.randint(min_length, max_length)))


def message_body(user, password):
    return """Hi {user},
Please find your account details below:
USER: {user}
PASSWORD: {password}
    """.format(user=user, password=password)


class UserList(Resource):
    method_decorators = [login_required]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user', required=True, dest='user_name')
        parser.add_argument('role')
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('email', required=True)

        args = parser.parse_args()

        password = random_password()

        user = User(user_name=args['user_name'], role=args['role'], first_name=args['first_name'],
                    last_name=args['last_name'], email=args['email'])
        user.hash_password(password)

        user.save()

        send_mail(args['email'], "Your account has been created on dsas.io", message_body(
            args["user_name"], password))

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

        if args['role'] and args['password']:
            abort(400)

        if args['role']:
            user.role = args['role']
        else:
            password = random_password()
            user.hash_password(password)
            send_mail(user.email, "Your account has been updated on dsas.io", message_body(
                user_id, password))

        user.save()

        return "User {user_id} updated".format(user_id=user.user_name), 204


class Authentications(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args()

        qs = User.objects(user_name=args['user'])

        if not qs:
            current_app.logger.warning(
                'User {} not found'.format(args['user']))
            abort(403)

        user = qs[0]

        if user.verify_password(args['password']) is False:
            current_app.logger.warning(
                'User {} types wrong password !'.format(args['user']))
            abort(403)

        payload = {
            'sub': user.user_name,
            'exp': datetime.datetime.now() + datetime.timedelta(days=1),
            'role': user.role
        }

        token = jwt.encode(
            payload, current_app.config['SECRET_KEY'], algorithm='HS256')

        return token.decode('unicode_escape'), 201
