"""Import necessary modules and classes from Flask, Flask-WTF, and other packages."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User  # Import the User model from your application's models


class RegistrationForm(FlaskForm):
    """Define a form for user registration."""

    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=999)])
    confirmpassword = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    """Define fields and their associated validators"""

    submit = SubmitField('Sign Up')
    """define a submit button"""
    
    """Custom validation to check if the username is already taken"""
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username has been taken. Please choose another username.')

    """Custom validation to check if the email is already registered"""
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email has been used. Please choose another email.')

class UpdateAccountForm(FlaskForm):
    """Define a form for updating user account information"""
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')  # Define a submit button

    """Custom validation to check if the updated username is already taken"""
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username has been taken. Please choose another username.')

    """Custom validation to check if the updated email is already registered"""
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email has been used. Please choose another email.')


class PostForm(FlaskForm):
    """Define a form for creating new posts."""

    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    """Define fields and their associated validators"""

    submit = SubmitField('Create Post')
    """Define a submit button"""
