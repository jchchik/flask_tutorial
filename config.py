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
