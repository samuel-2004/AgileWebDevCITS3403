import selenium
from selenium import webdriver
import time
import unittest
from app import create_app, db
from app.config import TestConfig
from app.models import Users, Post, Image
import multiprocessing

localHost = "http://localhost:5000"
class SeleniumTests(selenium.TestCase):
    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        #add_test_data_to_db()

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

    def test_index_page(self):
        time.sleep(10)
        self.assertTrue(True)