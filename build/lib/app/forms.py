from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField

from wtforms.validators import DataRequired, EqualTo, Length


class RequestForm(Form):
    name = TextField(
        'Name', validators=[DataRequired(), Length(min=2, max=25)]
    )
    lastname = TextField(
        'Last Name', validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=2, max=40)]
    )
    department = TextField(
        'Department', validators=[DataRequired(), Length(min=1, max=25)]
    )
    description = TextAreaField()

class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )




class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
