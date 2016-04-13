import os

class base_config(object):
    DEBUG = True
    SECRET_KEY = 'GENERATE SECRET KEY'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'postgres://user:password@host:port/database'
    HOST = 'localhost'
    PORT = int(os.environ.get('PORT', 5000))
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "GMAIL USER"
    MAIL_PASSWORD = "GMAIL PASSWORD"
