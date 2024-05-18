import multiprocessing
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from unittest import TestCase

from app import create_app, db
from app.config import TestConfig
#from app.controllers import GroupCreationError, create_group
from app.models import User, Post, Image

localHost = "http://localhost:5000"
class SeleniumTests(TestCase):
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
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options = options)

        self.driver.get(localHost)
        
    def tearDown(self):
        self.server_thread.terminate()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_go_to_login_page(self):
        self.driver.find_element(By.LINK_TEXT, 'Login').click()
        self.assertEqual(self.driver.current_url,"http://localhost:5000/login")

"""     def test_login_page(self):
        loginElement = self.driver.find_element(By.ID, "username")
        loginElement.send_keys("jimmy")

        loginElement = self.driver.find_element(By.ID, "password")
        loginElement.send_keys("123456")

        submitElement = self.driver.find_element(By.ID, "submit")
        submitElement.click()

        errorMessage = self.driver.find_element(By.TAG_NAME, "message")
        self.assertEqual(self.driver.current_url, localHost = "login_page")
        self.assertEqual(errorMessage[0:].text, f"Write yours here")


    def test_signup_page(self):
        loginElement = self.driver.find_element(By.ID, "username")
        loginElement.send_keys("Add username")

        loginElement = self.driver.find_element(By.ID, "password")
        loginElement.send_keys("Add password")

        # continue with other parameters

    def test_upload_page(self):
        # continue with other parameters
        pass

    def test_search_page(self):
        # continue with other parameters
        pass

    def test_about_page(self):
        # continue with other parameters
        pass

    def test_displayitems_page(self):
        # continue with other parameters
        pass
     """