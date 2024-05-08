# python -m unittest tests.unittest
import os
import unittest
from app import create_app, db
from app.config import TestConfig
from app.models import Users, Post, Image


class BasicTests(unittest.TestCase):
    testApp = create_app(TestConfig)
    self.app_context = testApp.app_context()
    self.app_context.push()
    db.create_all()
    # add_test_data_to_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = Users(userId = "1", username = "user1")
        u.set_password("bubbles")
        self.assertTrue(u.check_password("bubbles"))
        self.assertFalse(u.check_password("rumbles"))

import selenium
from selenium import webdriver

localHost = "http://localhost:5000"
class SeleniumTests(selenium.TestCase):
    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        add_test_data_to_db()

        self.server_thread = multiprocessing.Process(target = self.testApp.run)
        self.server_thread.start()

        # Make test run without rendering web page
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options = options)

        self.driver.get(localHost)
        
    def tearDown(self):
        self.server_thread.terminate()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main(verbosity=2)