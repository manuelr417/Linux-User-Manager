import os

DEBUG = True
SECRET_KEY = 'B21A38EBAEA52759AB48B1DDE4319'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'postgres://rkqdxhfifvselg:9J6oTxFLM54wVhZGbK8Qzv7oEI@ec2-107-21-219-109.compute-1.amazonaws.com:5432/d9lgd4aus8u9r7'
HOST = 'localhost'
PORT = int(os.environ.get('PORT', 5000))
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = "uprm.htcondor"
MAIL_PASSWORD = "B21A38EBAEA52759AB48B1DDE4319"
