import json

from flask import jsonify
from flask_restful import Resource, abort, reqparse

from application.models import User


class UserList(Resource):
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
