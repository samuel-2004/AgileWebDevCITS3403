"""
Defines the configuration settings for the app
"""
from os import path, environ
basedir = path.abspath(path.dirname(__file__))

class Config:
    '''
    Global config settings
    '''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get('SECRET_KEY')
    
class DeploymentConfig(Config):
    '''
    Deployment config settings
    '''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'app.db')
    
class TestConfig(Config):
    '''
    Test config settings
    '''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'
    TESTING = True
