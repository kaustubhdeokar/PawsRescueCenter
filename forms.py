from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password',
                             validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    submit = SubmitField('Sign Up')


class SignUpForm(FlaskForm):
    fullname = StringField('Fullname')
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password',
                             validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Sign Up')


class PetEditForm(FlaskForm):
    name = StringField('Pet\'s Name')
    age = StringField('Pet\'s Age')
    bio = StringField('Pet\'s Bio')
    delete = SubmitField('Delete')
    submit = SubmitField('Edit')