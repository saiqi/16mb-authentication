import json

from flask import jsonify
from flask_restful import Resource, abort, reqparse

from application.models import User


class UserList(Resource):
    
    def post(self):
    
        parser = reqparse.RequestParser()
        parser.add_argument('user', required=True, dest='id')
        parser.add_argument('password',required=True)
        parser.add_argument('role')
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        
        args = parser.parse_args()
        
        user = User(id=args['id'], role=args['role'], first_name=args['first_name'], last_name=args['last_name'])
        user.hash_password(args['password'])
        
        user.save()
        
        return "User {user_id} created".format(user_id=user.id), 201
        
    
class Users(Resource):
    
    def get(self, user_id):
    
        user = User.object.get_or_404(id = user_id)
        
        return jsonify(json.loads(user.to_json()))
        
    def put(self, user_id):
        
        user = User.object.get_or_404(id = user_id)
        
        parser = reqparse.RequestParser()
        parser.add_argument('password',required=True)
        parser.add_argument('role')
        parser.add_argument('is_active', type=bool)
        
        args = parser.parse_args()
        
        if 'role' in args and args['role'] is not None:
            user.role = args['role']
            
        if 'is_active' in args and args['is_active'] is not None:
            user.is_active = args['is_active']
            
        if 'password' in args and args['password'] is not None:
            user.password = args['password']
            
        user.save()
        
        return "User {user_id} updated".format(user_id=user.id), 201
        