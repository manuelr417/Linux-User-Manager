import uuid

from werkzeug.local import LocalProxy
from app.models import db, User, Request, RequestStatus, UserRole, PasswordRequest
from flask import render_template, request, redirect, Blueprint
from sqlalchemy.exc import IntegrityError
from app.forms import *
from flask import current_app
from flask.ext.mail import Mail, Message
from fabric.api import local, env, run, execute

mail = Mail()

logger = LocalProxy(lambda: current_app.logger)

blueprint = Blueprint('api', __name__)


host = '136.145.59.124'

env.hosts = [host]
env.user = 'root'


@blueprint.route('/request', methods=['POST'])
def new_request():
    form = RequestForm()

    if form.validate_on_submit():
        exists = db.session.query(Request).filter(Request.email == form.email.data).first()

        if exists:
            return render_template('pages/email_conflict.html', data=exists)
        else:
            new_uuid = str(uuid.uuid1())
            create_request = Request(
                name=form.name.data,
                lastname=form.lastname.data,
                email=form.email.data,
                department=form.department.data,
                description=form.description.data,
                uuid=new_uuid,
                status=0
            )
            try:
                db.session.add(create_request)
                msg = Message(
                    'Please Confirm your email',
                    sender="htcondor@uprm.edu",
                    recipients=[create_request.email])
                msg.html = '<p> Dear ' + create_request.name + ', </p>' + '<p> Please go to the following link and confirm you request:</p>' + '<a href="' + request.url_root + 'request/confirm?uuid=' + create_request.uuid + '" >Confirm Email</a>' + '<p>Shortly it will be review by one of our administrators.</p>'
                mail.send(msg)
                db.session.commit()
                return render_template('pages/request_created.html', data=create_request)

            except IntegrityError:
                db.session.rollback()
                return "Database Error"

            finally:
                db.session.close()

    else:
        return "Everything Failed"


# This method confirm email of a request
@blueprint.route("/request/confirm", methods=['Get'])
def email_confirmation():
    try:
        current_uuid = request.args.get('uuid')
        current_app.logger.info(current_uuid)
        current_request = Request.query.filter(Request.uuid == current_uuid).first()

        if current_request:
            current_request.email_confirmation = True
            current_request.status = 1
            msg = Message(
                'New Account Request',
                sender="htcondor@uprm.edu",
                recipients=["david.bartolomei@upr.edu"])
            msg.html = '<p>Please Login to your HTCondor Dashboard. New account request is waiting for you. </p> <a href="' + request.url_root + '"> Condor Admin Login </a>'
            mail.send(msg)

            db.session.commit()

            return redirect("/email/confirmed")

        else:
            current_app.logger.error("error updating DB")
            return "Error. Please try later."

    except:
        return "error"


@blueprint.route("/request/approve", methods=['Get'])
def approve_request():
    print env.hosts
    execute(ssh)
    # current_uuid = request.args.get('uuid')
    # current_app.logger.info(current_uuid)
    # current_request = Request.query.filter(Request.uuid == current_uuid).first()
    # current_request.status = 2  # Change status to approved
    #
    # new_user = User(
    #     roleID=1,  # Default to regular User
    #     requestID=current_request.requestID,
    #     password=current_request.requestID,
    #     email=current_request.email,
    #     name=current_request.name,
    #     lastname=current_request.lastname
    # )
    #
    # db.session.add(new_user)
    # db.session.commit()
    # return redirect("/request/list")

    # run("ls /var/www/")
    # run("ls /home/myuser", shell=False)


def ssh():
    output = run('ls /var/ --password=%s' % "ieriMee0")
    run("take_a_long_time", timeout=5)
    print output