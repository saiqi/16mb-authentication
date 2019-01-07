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

    MAIL_SERVER = os.getenv('SMTP_HOST')
    MAIL_USERNAME = os.getenv('SMTP_USER')
    MAIL_PASSWORD = os.getenv('SMTP_PASSWORD')
    MAIL_PORT = os.getenv('SMTP_PORT')
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = os.getenv('DEFAULT_SENDER')
    MAIL_SUPPRESS_SEND = os.getenv('MAIL_SUPPRESS_SEND', False)
