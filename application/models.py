from passlib.apps import custom_app_context as pwd_context
from flask_mongoengine import MongoEngine


db = MongoEngine()


class User(db.Document):
    first_name = db.StringField(max_length=255)
    last_name = db.StringField(max_length=255)
    id = db.StringField(max_length=255, required=True, unique=True)
    password_hash = db.StringField(max_length=255)
    email = db.EmailField(required=True, unique=True)
    role = db.StringField(required=True, default='read')
    is_active = db.BooleanField(required=True, default=True)
    
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
        
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
