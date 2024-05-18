"""
The main application module
"""
from app import create_app, db
from app.config import DeploymentConfig
from app.models import User, Post, Image, Address, Reply
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_migrate import Migrate

flaskApp = create_app(DeploymentConfig)
migrate = Migrate(flaskApp, db)

@flaskApp.shell_context_processor
def make_shell_context():
    """
    Provides command line context when executing `flask shell`
    """
    return {'sa': sa, 'so': so, 'db': db, 'User': User, \
        'Post': Post, 'Image': Image, 'Address': Address, 'Reply': Reply}
