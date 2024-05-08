from flask import Flask
from config import Config
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


# Testing Purposes
db = SQLAlchemy()

def create_app(config):
    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config)

    db.init_app(flaskApp)
    # initialises routes

    from app.blueprints import main
    flaskApp.register_blueprint(main)
    return flaskApp
