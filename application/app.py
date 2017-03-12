from flask import Flask, current_app
from flask_restful import Api

from application.resources import Users, UserList, Authentications


def create_app():

    app = Flask(__name__)
    app.config.from_object('application.config.Config')

    api = Api()

    api.add_resource(Users, '/users/<string:user_id>')
    api.add_resource(UserList, '/users')

    api.add_resource(Authentications, '/auth')

    from application.models import db
    db.init_app(app)
    api.init_app(app)
    
    return app
    

app = create_app()


@app.before_first_request
def create_admin():
    from application.models import User

    user = User(user_name=current_app.config['ADMIN_USER'], email=current_app.config['ADMIN_EMAIL'])
    user.hash_password(current_app.config['ADMIN_PASSWORD'])

    user.save()
