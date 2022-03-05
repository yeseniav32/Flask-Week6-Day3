from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo

class UserLoginForm(FlaskForm):
    #set up the email, password, confirm, and submitt button
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm', message = 'Your passwords do not match, please try again.')])
    confirm = PasswordField('Confirm Password')
    submit_button = SubmitField()