from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler

app = Flask(__name__)
app.config.from_object(Config)

# db object that represents the database
db = SQLAlchemy(app)
# Represents the migration engine
migrate = Migrate(app, db)
login = LoginManager(app)
# Bootstrap Import (Flask)
bootstrap = Bootstrap(app)

# Run email/file logger when application is running without debug mode
if not app.debug:
	# Run email logger when the email server exists in the configuration
	if app.config['MAIL_SERVER']:
		auth = None
		if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
			auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
		secure = None
		if app.config['MAIL_USE_TLS']:
			secure = ()
		# Sets a SMTP handler and only reports errors not warnings
		mail_handler = SMTPHandler(
			mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
			fromaddr='no-reply@' + app.config['MAIL_SERVER'],
			toaddrs=app.config['ADMINS'], subject='Microblog Failure',
			credentials=auth, secure=secure)
		mail_handler.setLevel(logging.ERROR)
		# Attach to a app.logger object from Flask
		app.logger.addHandler(mail_handler)

	# File logging for errors
	if not os.path.exists('logs'):
		os.mkdir('logs')
	file_handler = RotatingFileHandler('logs/blog.log', maxBytes=10240,
									   backupCount=10)
	file_handler.setFormatter(logging.Formatter(
		'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)

	app.logger.setLevel(logging.INFO)
	app.logger.info('Microblog startup')

# Importing new modules
# routes is the routing of urls
# models defines the structure of the database
# errors is the error handling functions
from app import routes, models, errors