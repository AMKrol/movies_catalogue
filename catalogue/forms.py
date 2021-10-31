from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={
                        "placeholder": "Title"})
    body = TextAreaField('Post content', validators=[DataRequired()], render_kw={
                         "placeholder": "Post content"})
    is_published = BooleanField('Published')


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
