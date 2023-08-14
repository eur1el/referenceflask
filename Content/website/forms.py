from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User



#creates a registration form
class RegistrationForm(FlaskForm):
    #creates a username which is a stringfield called "Username", it has validators such as maximum 20 values and minimum values and that data is required
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=20)])
    #creates an email which is a stringfield called "Email", it has to be an email input and that data is required
    email = StringField('Email', validators=[DataRequired(),Email()])
    #creates a password which is a stringfield called "Password", it has validators such as maximum 20 values and minimum values and that data is required
    password = StringField('Password', validators=[DataRequired(),Length(min=2, max=20)])
     #creates a confirm password which is a stringfield called "Confirm Password", it has validators such as maximum 20 values and minimum values and that data is required
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    #creates a field which is called "Sign Up" which allows users to sign up
    submit = SubmitField('Sign Up')

    #defines validate_username
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        #if user enters a taken username proceed and prompt user with a message that tells them to enter a new message
        if user:
            raise ValidationError('That username is taken. Please choose a different one')
    
    #defines validate email
    def validate_email(self, email):
        email = User.query.filter_by(Email=Email.data).first()
        #if user enters a taken email proceed and prompt user with a message that tells them to enter a new email address
        if email:
            raise ValidationError('That email is taken. Please choose a different one')


    