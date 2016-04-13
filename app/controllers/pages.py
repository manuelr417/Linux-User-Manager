# from app import login_manager

from flask.ext.login import login_user, login_required, logout_user, current_user
from app.forms import *
from app.models import User, db, Request, RequestStatus
from flask import (Blueprint, send_from_directory, abort, request,
                   render_template, current_app, render_template, redirect,
                   url_for)
from flask.ext.bcrypt import Bcrypt

blueprint = Blueprint('pages', __name__)

bcrypt = Bcrypt()


################
#### Pages ####
################

@blueprint.route('/')
def home():
    return render_template('pages/home.html')


@blueprint.route('/about')
def about():
    return render_template('pages/about.html')


@blueprint.route('/email/confirmed')
def email_confirmed():
    return render_template('pages/email_confirmed.html')


@blueprint.route('/request/list')
@login_required
def request_list():
    open_requests = db.session.query(Request)\
        .filter(Request.status == 1)\
        .filter(Request.email_confirmation == True)\
        .order_by(Request.status.asc())
    return render_template('pages/request_list.html', open_requests=open_requests)


@blueprint.route('/account/list')
@login_required
def account_list():
    open_requests = db.session.query(Request)\
        .filter(Request.status > 1)\
        .filter(Request.email_confirmation == True)\
        .order_by(
        Request.status.asc())
    return render_template('pages/account_list.html', open_requests=open_requests)


################
#### Forms ####
################
# @blueprint.route('/login')
# def login():
#     form = RegisterForm(request.form)
#     return render_template('forms/login.html', form=form)
#

@blueprint.route('/account/request')
def register():
    form = RequestForm(request.form)
    return render_template('forms/request_account.html', form=form)


@blueprint.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. For POSTS, login the current user
    by processing the form."""
    print db
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect('/request/list')
    return render_template("forms/login.html", form=form)


@blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect('/')


