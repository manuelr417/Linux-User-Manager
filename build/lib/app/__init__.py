import logging
from flask import Flask, request as req
from flask.ext.login import LoginManager
from flask.ext.mail import Mail, Message
from app.controllers import pages
from app.controllers import api
import configuration
from flask_wtf.csrf import CsrfProtect
from app.models import db, User, RequestStatus, Request, UserRole, PasswordRequest

csrf = CsrfProtect()
mail = Mail()
lm = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(configuration.base_config)
    
    with app.app_context():
        lm.init_app(app)
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
