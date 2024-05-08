from app import create_app, db
from app.config import TestConfig
testApp = create_app(TestConfig)