from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

# db object that represents the database
db = SQLAlchemy(app)
# Represents the migration ngine
migrate = Migrate(app, db)
login = LoginManager(app)

# Importing new modules
# routes is the routing of urls
# models defines the structure of the database
from app import routes, models