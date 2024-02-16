from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField
from flask_wtf.file import FileField, FileRequired
# from sqlalchemy_utils import PhoneNumber
# from wtforms.fields.html5 import EmailField
from wtforms import validators
from extensions import db
from wtforms.validators import InputRequired, Email
from models import User
from wtforms import ValidationError


class FileUploadForm(FlaskForm):
	title = StringField('Title')
	note = FileField('File', [InputRequired("Please import the file.")])

class  RegisterForm(FlaskForm):
	first_name = StringField('First Name', [InputRequired("Please enter your first name.")])
	last_name = StringField('Last Name')
	email = StringField("Email",  [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
	phone_number = StringField('Phone Number', [InputRequired("Please enter your phone number.")]) 
	password = PasswordField('Password', [InputRequired("Please enter your password."), validators.EqualTo('confirm_password', message='Passwords must match')])
	confirm_password = PasswordField('Confirm Password', [InputRequired("Please confirm your password.")])

	def validate_email(form, field):
		print(form.email.data)
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			raise ValidationError("Email already in use.")
    
class  LoginForm(FlaskForm):
	email = StringField("Email",  [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
	password = PasswordField('Password', [InputRequired("Please enter your password.")])
