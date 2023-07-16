from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BoleeanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .forms import RegistationForm








class RegistationForm(Flask):
    #creates a username which is a stringfield called Username, it has validators such as maximum 20 values and minimum values and that data is required
    username = StringField('Username', validators=[DataRequired(),Length(min-2, max=20)])
    #creates a username which is a stringfield called Username, it has to be an email input and that data is required
    emailed = StringField('Username', validators=[DataRequired(),Email()])
    #creates a username which is a stringfield called Username, it has validators such as maximum 20 values and minimum values and that data is required
    password = StringField('Username', validators=[DataRequired(),Length(min-2, max=20)])
    #
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired])
    #
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')
        
        def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')


    