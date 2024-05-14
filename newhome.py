from app import create_app, db
from app.config import DeploymentConfig
import sqlalchemy as sa
from app.models import *
import sqlalchemy.orm as so
import sqlite3

from flask_migrate import Migrate

flaskApp = create_app(DeploymentConfig)
migrate = Migrate(db, flaskApp)


@flaskApp.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post, 'Image': Image, 'Address': Address}

#from app import flaskApp
#import sqlite3

