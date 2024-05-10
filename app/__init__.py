from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

flaskApp = Flask(__name__)
login = LoginManager(flaskApp)
login.login_view = 'login'
flaskApp.config.from_object(Config)
db = SQLAlchemy(flaskApp)
migrate = Migrate(flaskApp, db)
from app import routes, models
