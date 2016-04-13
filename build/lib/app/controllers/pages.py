from flask import render_template, Blueprint, request
# from app import login_manager
from app.forms import *
from app.models import User, db, Request, RequestStatus

blueprint = Blueprint('pages', __name__)


################
#### Login ####
################
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

# @blueprint.route('/login', methods=['GET', 'POST'])
# def login():
#     # Here we use a class of some kind to represent and validate our
#     # client-side form data. For example, WTForms is a library that will
#     # handle this for us, and we use a custom LoginForm to validate.
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Login and validate the user.
#         # user should be an instance of your `User` class
#         login_user(user)
#
#         flask.flash('Logged in successfully.')
#
#         next = flask.request.args.get('next')
#         # next_is_valid should check if the user has valid
#         # permission to access the `next` url
#         if not next_is_valid(next):
#             return flask.abort(400)
#
#         return flask.redirect(next or flask.url_for('index'))
#     return flask.render_template('login.html', form=form)

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
def request_list():
    open_requests = db.session.query(Request).filter(Request.email_confirmation == True).order_by(Request.status.asc())
    return render_template('pages/request_list.html', open_requests=open_requests)


################
#### Forms ####
################
@blueprint.route('/login')
def login():
    form = RegisterForm(request.form)
    return render_template('forms/login.html', form=form)


@blueprint.route('/account/request')
def register():
    form = RequestForm(request.form)
    return render_template('forms/request_account.html', form=form)


@blueprint.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)
