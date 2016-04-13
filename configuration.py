import os

class base_config(object):
    DEBUG = True
    SECRET_KEY = 'B21A38EBAEA52759AB48B1DDE4319'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'postgres://user:password@host:port/database'
    HOST = 'localhost'
    PORT = int(os.environ.get('PORT', 5000))
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "GMAIL USER"
    MAIL_PASSWORD = "GMAIL PASSWORD"
