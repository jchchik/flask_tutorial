import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

	# The Flask-SQLAlchemy extension takes the location of the application's 
	# database from the SQLALCHEMY_DATABASE_URI configuration variable. and
	# provides a fallback value when the environement does not define a variable
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')

	# This configuration option is to disable a feature in Flask-SQLAlchemy that
	# is not needed which is to signal the application every time a change is about
	# to be made in the database
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Server configuration variables for email and sourced from environment variable
	# counterparts
	#
	# Setting the email server
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	# Defining the email port, if not set the standard of 25 is used
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	# By default email server credentials are not used
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	# List of emails which will will receive error reports
	ADMINS = ['jonathanchik@gmail.com']

	# Determine the number of posts produced for each page in pagination
	POSTS_PER_PAGE = 3