import os


class Config(object):
    SECRET_KEY = os.getenv('APP_SECRET_KEY')
    
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGODB_HOST'),
        'replicaset': os.getenv('MONGODB_REPLICASET')
    }

    ADMIN_USER = os.getenv('APP_ADMIN_USER')
    ADMIN_PASSWORD = os.getenv('APP_ADMIN_PASSWORD')
    ADMIN_EMAIL = os.getenv('APP_ADMIN_EMAIL')
