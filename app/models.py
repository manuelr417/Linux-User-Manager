from flask.ext.sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy()


# Defining a new request for an account
class Request(db.Model):
    __tablename__ = 'request'
    request_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    department = db.Column(db.String(255))
    description = db.Column(db.String(255))
    date_requested = db.Column(db.DateTime, default=datetime.datetime.now)
    date_changed = db.Column(db.DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    email_confirmation = db.Column(db.Boolean, default=False)
    uuid = db.Column(db.String(255))
    status = db.Column(db.ForeignKey('request_status.status_id'))


class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.ForeignKey('user_role.role_id'))

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


class UserRole(db.Model):
    __tablename__ = 'user_role'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(45))
#  Roles:
# 0 User
# 1 Manager
# 2 Admin

class RequestStatus(db.Model):
    __tablename__ = 'request_status'
    status_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(45))

# Status Codes:
# 0 Pending Email Confirmation
# 1 Pending Review
# 2 Approved
# 3 Denied
# 4 Deleted


#INSERT INTO user_role (role_id, role_name) VALUES (0, 'user');
#INSERT INTO user_role (role_id, role_name) VALUES (1, 'manager');
#INSERT INTO user_role (role_id, role_name) VALUES (2, 'admin');

# INSERT INTO request_status (status_id, status) VALUES (0, 'Pending Email Confirmation');
# INSERT INTO request_status (status_id, status) VALUES (1, 'Pending Review');
# INSERT INTO request_status (status_id, status) VALUES (2, 'Approved');
# INSERT INTO request_status (status_id, status) VALUES (3, 'Denied');
# INSERT INTO request_status (status_id, status) VALUES (4, 'Deleted');

