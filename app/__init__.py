import logging
import flask
from flask import Flask, request as req
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from app.controllers import pages
from app.controllers import api
import configuration
from flask_wtf.csrf import CsrfProtect
from app.models import db, User, RequestStatus, Request, UserRole
from app.forms import *
from flask.ext.bcrypt import Bcrypt
from flask import redirect

csrf = CsrfProtect()
mail = Mail()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(configuration.base_config)

    with app.app_context():
        login_manager.init_app(app)
        db.init_app(app)
        db.create_all()
        mail.init_app(app)
        csrf.init_app(app)

    app.register_blueprint(pages.blueprint)
    app.register_blueprint(api.blueprint)

    app.logger.setLevel(logging.NOTSET)

    @app.after_request
    def log_response(resp):
        app.logger.info("{} {} {}\n{}".format(
            req.method, req.url, req.data, resp)
        )
        return resp

    return app


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect('/login')
