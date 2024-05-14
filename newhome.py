"""
The main application module
"""
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import flaskApp, db
from app.models import User, Post, Image, Address

@flaskApp.shell_context_processor
def make_shell_context():
    """
    Provides command line context when executing `flask shell`
    """
    return {'sa': sa, 'so': so, 'db': db, \
        'User': User, 'Post': Post, 'Image': Image, 'Address': Address}
