from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from app import login
from hashlib import md5

# The model page defines the structure of the Model within the MVC framework
# These items define how the structure is formed within the Database
#
# To create the flask migration script run the following command:
# flask db migrate -m "new fields in the user model"
#
# To use the newly created flask migration script run the following command:
# flask db upgrade
#
# To backtrack on a previous change performed by a flask migration script run the
# following command:
# flask db downgrade

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def avatar(self, size):
		"""
		Return's URL of the user's avatar image scaled to the represented size in pixels
		If users do not have an avatar registered, an "indenticon" image will be generated
		"""

		# Convert user's email to lower case, as required by the Gravatar service and
		# since MD5 is suported in bytes and not strings, encode the string in bytes
		# before passing it to the hash function
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}'.format(self.body)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))