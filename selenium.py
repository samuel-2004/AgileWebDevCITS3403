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

    def test_login_page(self):
        time.sleep(1)
        loginElement = self.driver.find_element(By.username, "username")
        loginElement.send_keys("Add username")

        loginElement = self.driver.find_element(By.username, "password")
        loginElement.send_keys("Add password")

        submitElement = self.driver.find_element(By.username, "submit")
        submitElement.click()

        errorMessage = self.driver.find_element(By.TAG_NAME, "message")
        self.assertEqual(self.driver.current_url, localHost = "login_page")
        self.assertEqual(message[0:], text, f"Write yours here")

        webDriverWait(driver=self.driver).until

    def test_signup_page(self):
        loginElement = self.driver.find_element(By.username, "username")
        loginElement.send_keys("Add username")

        loginElement = self.driver.find_element(By.password, "password")
        loginElement.send_keys("Add password")

        # continue with other parameters
    