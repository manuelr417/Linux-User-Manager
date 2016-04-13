from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context
import datetime

db = SQLAlchemy()


# Defining a new request for an account
class Request(db.Model):
    __tablename__ = 'Request'
    requestID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    department = db.Column(db.String(255))
    description = db.Column(db.String(255))
    date_requested = db.Column(db.DateTime, default=datetime.datetime.now)
    date_changed = db.Column(db.DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    email_confirmation = db.Column(db.Boolean, default=False)
    uuid = db.Column(db.String(255))
    status = db.Column(db.ForeignKey('RequestStatus.statusID'))


class User(db.Model):
    __tablename__ = 'User'
    userID = db.Column(db.Integer, primary_key=True)
    roleID = db.Column(db.Integer, db.ForeignKey('UserRole.roleID'))
    requestID = db.Column(db.Integer, db.ForeignKey('Request.requestID'))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    name = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    active = db.Column(db.Boolean, default=True)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=6000):
        s = Serializer("9B26798F18854ADD922D5475D85CB", expires_in=expiration)
        return s.dumps({'id': self.userID})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer("9B26798F18854ADD922D5475D85CB")
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['userID'])
        return user


class UserRole(db.Model):
    __tablename__ = 'UserRole'
    roleID = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(45))
#  Roles:
# 0 User
# 1 Manager
# 2 Admin

class RequestStatus(db.Model):
    __tablename__ = 'RequestStatus'
    statusID = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(45))

# Status Codes:
# 0 Pending Email Confirmation
# 1 Pending Review
# 2 Approved
# 3 Denied
# 4 Canceled

