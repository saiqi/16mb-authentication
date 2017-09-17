from flask import Flask
from flask_restful import Api

from application.resources import Users, UserList, Authentications


def create_app():

    app = Flask(__name__)
    app.config.from_object('application.config.Config')

    api = Api()

    api.add_resource(Users, '/users/<string:user_id>')
    api.add_resource(UserList, '/users')

    api.add_resource(Authentications, '/auth')

    from application.models import db, User
    db.init_app(app)
    api.init_app(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        return response

    users = User.objects(role='admin')

    if not users:
        user = User(user_name=app.config['ADMIN_USER'], email=app.config['ADMIN_EMAIL'], role='admin')
        user.hash_password(app.config['ADMIN_PASSWORD'])

        user.save()
    
    return app
    

app = create_app()
