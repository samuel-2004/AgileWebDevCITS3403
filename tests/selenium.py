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
from app.models import User, Address, Post

localHost = "http://localhost:5000"
class SeleniumTests(TestCase):
    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        self.insert_dummy_data(db)

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

    def insert_dummy_data(self, db):
        # Address
        addr = Address(address_line1="95 Pine St", address_line2="", suburb="Crawley", city="Perth", \
                    postcode="6009", state="WA", country="Australia", longitude="31.9789",lattitude="115.8181")
        db.session.add(addr)

        # User
        user = User(username='matt', email='matt@example.com', address = addr)
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()

    def test_incorrect_login_page(self):

        self.driver.find_element(By.LINK_TEXT, 'Login').click()
        self.assertEqual(self.driver.current_url,"http://localhost:5000/login", "Should be on login page")
        loginElement = self.driver.find_element(By.ID, "username")
        loginElement.send_keys("jimmy")
        
        loginElement = self.driver.find_element(By.ID, "password")
        loginElement.send_keys("123456")
        
        submitElement = self.driver.find_element(By.ID, "submit")
        submitElement.click()
        
        messages = self.driver.find_elements(By.CLASS_NAME, "message")
        self.assertEqual(len(messages), 1, "Expected there to be a single error message when trying to login as a non-existent user")
        self.assertEqual(messages[0].text, "Invalid username or password")
    
    def test_logged_out_redirects(self):
        pages = ["upload", "user"]
        for page in pages:
            self.driver.get(f"http://localhost:5000/{page}")
            messages = self.driver.find_elements(By.CLASS_NAME, "message")
            self.assertEqual(len(messages), 1, f"Expected there to be a single error message when redirected from {page}")
            self.assertEqual(messages[0].text, "Please log in to access this page.")
            self.assertEqual(self.driver.current_url,f"http://localhost:5000/login?next=%2F{page}", "Should've been redirected to login")

    def test_successful_login(self):
        self.driver.get("http://localhost:5000/login")
        self.assertEqual(self.driver.current_url,"http://localhost:5000/login")
        loginElement = self.driver.find_element(By.ID, "username")
        loginElement.send_keys("matt")
        loginElement = self.driver.find_element(By.ID, "password")
        loginElement.send_keys("123456")
        submitElement = self.driver.find_element(By.ID, "submit")
        submitElement.click()

        self.assertEqual(self.driver.current_url,"http://localhost:5000/")

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