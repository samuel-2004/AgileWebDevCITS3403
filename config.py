import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLACLHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' # SET MANUALLY, DEFAULT ONLY FOR TESTING

    # Testing Purposes
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"
    SQLACLHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'test.db')

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"
    TESTING = True;