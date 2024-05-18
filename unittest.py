# python -m unittest tests.unittest
import unittest
from app import create_app, db
from app.config import TestConfig
from app.models import Users, Post, Image
import time
import multiprocessing

class BasicTests(unittest.TestCase):
    def setUp(self):
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()

        #self.server_process = multiprocessing.Process(target=self, testApp, run)
        #self.server_process.start()
        # add_test_data_to_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = Users(username='susan', email='susan@example.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))



    