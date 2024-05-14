from app import flaskApp, db
import sqlalchemy as sa
from app.models import *
import sqlalchemy.orm as so
import sqlite3


@flaskApp.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post, 'Image': Image, 'Address': Address}


