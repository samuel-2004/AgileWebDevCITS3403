import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'
    TESTING = True