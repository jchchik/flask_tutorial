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

followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	
	# 'User' is the right side entity of the relationship, the left side is the parent
	# class. This is a self-referential relatinoship, use same class on both sides
	# 'secondary' configures the association table that is used for the relationship
	# 'primaryjoin' indicates the condition that links the left side entity (follower
	# user) with the association table. In this case the parent class
	# 'secondaryjoin' indicates the condition that links the right side entity
	# 'backref' defines how the relationship will be accessed 
	followed = db.relationship(
		'User', secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

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

	# Check if a link between the two users exist
	# Looks for items in the association table that have the left side foreign key
	# set to the self user and the right side set to the user argument
	# Result query will be 0 or 1
	def is_following(self,user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	# Query to return posts by users followed by current user
	# as well as user's own posts
	def followed_posts(self):
		followed = Post.query.join(
			followers, (followers.c.followed_id == Post.user_id)).filter(
			followers.c.follower_id == self.id)
		own = Post.query.filter_by(user_id=self.id)
		return followed.union(own).order_by(Post.timestamp.desc())

	def own_posts(self):
		return Post.query.filter_by(user_id=self.id).order_by(Post.timestamp.desc())


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))