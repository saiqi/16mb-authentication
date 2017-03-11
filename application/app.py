from flask import Flask
from flask_restful import Api
from application.resources import Users, UserList


def create_app():

    app = Flask(__name__)
    app.config.from_object('application.config.Config')

    api = Api()

    api.add_resource(Users, '/users/<string:user_id>')
    api.add_resource(UserList, '/users')

    from application.models import db
    db.init_app(app)
    api.init_app(app)
    
    return app
    

app = create_app()
