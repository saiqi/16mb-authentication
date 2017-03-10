import os


class Config(object):
    SECRET_KEY = os.getenv('APP_SECRET_KEY')
    
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGODB_HOST'),
        'replicaset': os.getenv('MONGODB_REPLICASET')
    }
