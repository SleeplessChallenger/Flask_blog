from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email,\
							   EqualTo, ValidationError, Regexp
from flask_login import current_user
from blog.models import User


class RegistrationForm(FlaskForm):

	username = StringField('Username', 
							validators=[DataRequired(), \
							Length(min=5, max=15), \
							Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               				'''Usernames must have only letters, 
               					numbers, dots or 
               					underscores''')])
	email = StringField('Email',
						 validators=[DataRequired(), Email()])

	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm your password',
									  validators=[DataRequired(), \
									  EqualTo('password', message='Passwords must match')])
	country = StringField('Current location')

	submit = SubmitField('Sign up!')

	def validate_username(self, username): # check if user already in db or not
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Such username has been already taken')

	def validate_email(self, email): # check if email already in db or not
		email = User.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError('This email is already registered')

	# 'validate_' after should be name of the field


class LoginForm(FlaskForm):

	email = StringField('Email',
						 validators=[DataRequired(), Email()])

	password = PasswordField('Password',
							  validators=[DataRequired()])
	check = BooleanField('Tick to stay logged')
	submit = SubmitField('login!')


class UpdateAccountForm(FlaskForm):

	username = StringField('Username',
							validators=[DataRequired(), Length(min=2, max=25)])
	email = StringField('Email',
						 validators=[DataRequired(), Email()])

	country = StringField('Current location')
	
	pic = FileField('Update Profile image',
					 validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update now!')

	def validate_username(self, username):
		if username.data != current_user.username: # if new data differs from current else no need
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Such username is already taken. Opt for another variant')

	def validate_email(self, email):
		if email.data != current_user.email: # if new data differs from current else no need
			user = User.query.filer_by(email=email.data).first()
			if user:
				raise ValidationError('This email is already taken. Consider another one')


class RequestResetForm(FlaskForm):

	email = StringField('Email',
						 validators=[DataRequired(), Email()])
	submit = SubmitField('Request password reset')

	def validate_email(self, email):
		user_email = User.query.filter_by(email=email.data).first()
		if not user_email:
			raise ValidationError('No account with this email. Please, register first')


class ResetPasswordForm(FlaskForm):

	password = PasswordField('Password',
							  validators=[DataRequired()])
	confirm_password = PasswordField('Confirm your new password',
									  validators=[EqualTo('password', message='Passwords must match'), 
									  			  DataRequired()])
	submit = SubmitField('Place new password!')