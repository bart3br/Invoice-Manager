from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo, email_validator
from application.models import User

class RegistrationForm(FlaskForm):
    #creating a form for registration, defining the fields and validators
    #we need username, email, password, confirm password and submit button for user registration
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        #custom validator to check if the username already exists in the database
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already in use. Try a different one.')
    
    def validate_email(self, email):
        #custom validator to check if the email already exists in the database
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is already in use. Try a different one.')

class LoginForm(FlaskForm):
    #creating a form for user login, defining the fields and validators
    #here we only need email, password and submit button since we don't create a new user here
    #also added a remember me checkbox to remember the user with browser cookies
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')