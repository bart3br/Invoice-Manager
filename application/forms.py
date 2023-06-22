from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
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
    
class UpdateAccountForm(FlaskForm):
    #creating a form for updating user account
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            #custom validator to check if the username already exists in the database
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already in use. Try a different one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            #custom validator to check if the email already exists in the database
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is already in use. Try a different one.')
            
class InvoiceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    entries = TextAreaField('Entries', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    submit = SubmitField('Upload')
    
class UploadInvoiceForm(FlaskForm):
    invoice_file = FileField('Upload Invoice From PDF File', validators=[FileAllowed(['pdf'])])
    submit = SubmitField('Upload')
    
    def validate_file(self, invoice):
        if not invoice.data:
            raise ValidationError('Please choose a PDF file to upload new invoice.')