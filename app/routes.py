from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
	user = {'username':'Jonathan'}
	posts = [
		{
			'author': {'username':'John'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'username': 'Susan'},
			'body': 'The Avengers moview as so cool!'
		}]
	return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()

		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))

		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('index'))

	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = [
		{'author': user, 'body': 'Test post #1'},
		{'author': user, 'body': 'Test post #2'}
	]
	return render_template('user.html', user=user, posts=posts)

# Routing page for editing the profile in an about_me field for each user. Users also
# have the ability to change their username in this page. This works in conjunction 
# with the edit_profile.html template and form
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()

	# validate_on_submit() returns true, copy the data from the form into the user
	# object and write the object to the database
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit_profile'))

	# If the page/form is being requested with GET, this will populate the form with 
	# any pre-existing text in the fields found in the database
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me

	# If the above two criteria does not fit this implies browser sent a POST request
	# with form data but something in the data is invalid
	return render_template('edit_profile.html', title='Edit Profile', form=form)

# Before Request decorator from Flask registers the decorated function to be exceuted
# right before the view function. This is useful for executing any code before the
# view function
@app.before_request
def before_request():
	# Update the last_seen time of a logged in user in the database
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()