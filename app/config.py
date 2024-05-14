"""
Config object
"""
from os import path, environ
basedir = path.abspath(path.dirname(__file__))

class Config(object):
    """
    Config object
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'app.db')
    SQLACLHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY SET MANUALLY, DEFAULT ONLY FOR TESTING
    SECRET_KEY = environ.get('SECRET_KEY') or 'you-will-never-guess'
