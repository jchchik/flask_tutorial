from flask import render_template
from app import app, db

# Error handler functions which work similar to the view functions in the
# routes.py file. These return a second value after the template which is
# the error code number. 404 for page not found
@app.errorhandler(404)
def not_found_error(error):
	return render_templaet('404.html'), 404

# Error handler functions which work similar to the view functions in the
# routes.py file. These return a second value after the template which is
# the error code number. 500 for a database error
@app.errorhandler(500)
def internal_error(error):
	# Ensure failed data base sessions do not interfere with any database
	# accesses trigerred by the template, issue a session rollback and 
	# reset to a clean state
	db.session.rollback()
	return render_template('500.html'), 500