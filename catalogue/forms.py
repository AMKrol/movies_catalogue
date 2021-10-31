from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class SignupForm(FlaskForm):
    """User Sign-up Form."""
    username = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',
                            validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
