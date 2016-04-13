import uuid
from fabric.context_managers import settings
from flask.ext.login import login_required
from werkzeug.local import LocalProxy
from app.models import db, User, Request, RequestStatus, UserRole
from flask import render_template, request, redirect, Blueprint
from sqlalchemy.exc import IntegrityError
from app.forms import *
from flask import current_app
from flask.ext.mail import Mail, Message
from fabric.api import local, env, run, execute

mail = Mail()

logger = LocalProxy(lambda: current_app.logger)

blueprint = Blueprint('api', __name__)

host = 'HOST URI'

env.hosts = [host]
env.user = 'USER AT HOST'
env.password = 'USER AT HOST PASSWORD'


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
        return redirect('/account/request')


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
            msg.html = '<p>Please Login to your HTCondor Dashboard. New account request is waiting for you. </p> <a href="' + request.url_root + '/login"> Condor Admin Login </a>'
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
    current_uuid = request.args.get('uuid')
    current_app.logger.info(current_uuid)
    current_request = Request.query.filter(Request.uuid == current_uuid).first()
    current_request.status = 2  # Change status to approved

    username = current_request.email.split("@")[0]
    execute(ssh_approve, username, current_uuid)

    msg = Message(
        'Your account is ready!',
        sender="htcondor@uprm.edu",
        recipients=[current_request.email])
    msg.html = '<p>Your HT Condor has been created. login string: <br> <br> ssh ' + username + '@' + host + '<br> Temporary password: ' + current_uuid + '</p>'
    mail.send(msg)

    # db.session.add(new_user)
    db.session.commit()
    return redirect("/request/list")


@blueprint.route("/request/delete", methods=['Get'])
def delete_request():
    current_uuid = request.args.get('uuid')

    current_app.logger.info(current_uuid)
    current_request = Request.query.filter(Request.uuid == current_uuid).first()

    username = current_request.email.split("@")[0]

    db.session.delete(current_request)
    db.session.commit()

    execute(ssh_delete, username)

    msg = Message(
        'Your account have been deleted.',
        sender="htcondor@uprm.edu",
        recipients=[current_request.email])
    msg.html = '<p>Your HT Condor account has been deleted. </p>'

    mail.send(msg)

    return redirect("/account/list")


@blueprint.route("/request/lock", methods=['Get'])
def lock_request():
    current_uuid = request.args.get('uuid')
    current_app.logger.info(current_uuid)
    current_request = Request.query.filter(Request.uuid == current_uuid).first()
    current_request.status = 3  # Change status to deleted
    db.session.commit()

    username = current_request.email.split("@")[0]
    execute(ssh_lock, username)

    msg = Message(
        'Your account have been locked.',
        sender="htcondor@uprm.edu",
        recipients=[current_request.email])
    msg.html = '<p>Your HT Condor account have been locked. Please contact an admin. </p>'

    mail.send(msg)

    return redirect("/account/list")


@blueprint.route("/request/unlock", methods=['Get'])
def unlock_request():
    current_uuid = request.args.get('uuid')
    current_app.logger.info(current_uuid)
    current_request = Request.query.filter(Request.uuid == current_uuid).first()
    current_request.status = 2  # Change status to deleted
    db.session.commit()

    username = current_request.email.split("@")[0]
    execute(ssh_unlock, username)

    msg = Message(
        'Your account have been unlocked.',
        sender="htcondor@uprm.edu",
        recipients=[current_request.email])
    msg.html = '<p>Your HT Condor account have been unlocked. Welcome Back</p>'

    mail.send(msg)

    return redirect("/account/list")


@blueprint.route("/request/resetpassword", methods=['Get'])
def reset_password():
    current_uuid = request.args.get('email')
    current_app.logger.info(current_uuid)
    current_request = Request.query.filter(Request.uuid == current_uuid).first()
    # current_request.status = 2  # Change status to deleted
    # db.session.commit()
    #

    new_pwd = str(uuid.uuid1())
    username = current_request.email.split("@")[0]

    execute(reset_password, username, new_pwd)
    #
    # msg = Message(
    #     'Your account have been unlocked.',
    #     sender="htcondor@uprm.edu",
    #     recipients=[current_request.email])
    # msg.html = '<p>Your HT Condor account have been unlocked. Welcome Back</p>'
    #
    # mail.send(msg)

    return redirect("/request/list")


@blueprint.route('/account/view')
@login_required
def account_list():
    current_uuid = request.args.get('uuid')
    current_request = Request.query.filter(Request.uuid == current_uuid).first()

    username = current_request.email.split("@")[0]

    output = execute(get_processes(username))

    data = {"req": current_request, "output": output}
    return render_template('pages/account_view.html', data=data)


def ssh_approve(username, current_uuid):
    run('sudo useradd -p $(openssl passwd -1 ' + current_uuid + ') ' + username)
    run("sudo chage -d 0 " + username)


def ssh_delete(username):
    with settings(warn_only=True):
        run('sudo pkill -9 -u ' + username)
    with settings(warn_only=True):
        run('sudo userdel ' + username)
        run("sudo rm -rf /home/" + username)


def ssh_lock(username):
    with settings(warn_only=True):
        run('sudo pkill -9 -u ' + username)
    run('sudo passwd -l ' + username)


def ssh_unlock(username):
    with settings(warn_only=True):
        run('sudo pkill -9 -u ' + username)
        run('sudo passwd -u ' + username)


def reset_password(username, password):
    with settings(warn_only=True):
        run('sudo pkill -9 -u ' + username)
        run('echo -e "' + password + '\n' + password + '" | (passwd ' + username + ' )')


def get_processes(username):
    with settings(warn_only=True):
        output = run('ps -u ' + username)
