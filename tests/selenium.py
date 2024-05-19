import multiprocessing
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from unittest import TestCase

from app import create_app, db
from app.config import TestConfig
from app.models import User, Address

localHost = "http://localhost:5000"
class SeleniumTests(TestCase):
    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.insert_dummy_data(db)

        self.server_thread = multiprocessing.Process(target = self.testApp.run)
        self.server_thread.start()

        # Make test run without rendering web page
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1920,1080')  
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
                    postcode="6009", state="WA", country="Australia", longitude="31.9789",latitude="115.8181")
        db.session.add(addr)

        # User
        user = User(username='matt', email='matt@example.com', address = addr)
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()

    def test_incorrect_login(self):

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
        
        loginElement = self.driver.find_element(By.ID, "username")
        loginElement.send_keys("matt")
        loginElement = self.driver.find_element(By.ID, "password")
        loginElement.send_keys("123456")
        submitElement = self.driver.find_element(By.ID, "submit")
        submitElement.click()

        self.assertEqual(self.driver.current_url,"http://localhost:5000/index")
        
    def test_successful_signup(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.LINK_TEXT, 'here').click()
        self.assertEqual(self.driver.current_url,"http://localhost:5000/signup", "Should be on signup page")
        signupElement = self.driver.find_element(By.ID, "username")
        signupElement.send_keys("johnsmith")
        signupElement = self.driver.find_element(By.ID, "email")
        signupElement.send_keys("john.smith@test.com")
        signupElement = self.driver.find_element(By.ID, "password")
        signupElement.send_keys("password")
        signupElement = self.driver.find_element(By.ID, "confirmed_password")
        signupElement.send_keys("password")
        signupElement = self.driver.find_element(By.ID, "address_line1")
        signupElement.send_keys("35 Stirling Highway")
        signupElement = self.driver.find_element(By.ID, "suburb")
        signupElement.send_keys("Crawley")
        signupElement = self.driver.find_element(By.ID, "postcode")
        signupElement.send_keys("6009")
        signupElement = Select(self.driver.find_element(By.ID,'state'))
        signupElement.select_by_value("WA")
        signupElement = self.driver.find_element(By.ID, "city")
        signupElement.send_keys("Perth")
        submitElement = self.driver.find_element(By.ID, "submit")
        submitElement.click()
        self.driver.implicitly_wait(5) # To allow for signup
        messages = self.driver.find_elements(By.CLASS_NAME, "message")
        self.assertEqual(len(messages), 1, f"Expected there to be a single confirmation message")
        self.assertEqual(messages[0].text, "Congratulations! Welcome to NewHome!")
        self.assertEqual(self.driver.current_url,f"http://localhost:5000/login", "Should've been redirected to login")
        
    def test_unsuccessful_signup(self):
        self.driver.get("http://localhost:5000/signup")
        signupElement = self.driver.find_element(By.ID, "username")
        signupElement.send_keys("matt")
        signupElement = self.driver.find_element(By.ID, "email")
        signupElement.send_keys("matt@example.com")
        signupElement = self.driver.find_element(By.ID, "password")
        signupElement.send_keys("password")
        signupElement = self.driver.find_element(By.ID, "confirmed_password")
        signupElement.send_keys("pasword")
        signupElement = self.driver.find_element(By.ID, "address_line1")
        signupElement.send_keys("35 Stirling Highway")
        signupElement = self.driver.find_element(By.ID, "suburb")
        signupElement.send_keys("Crawley")
        signupElement = self.driver.find_element(By.ID, "postcode")
        signupElement.send_keys("6009")
        signupElement = Select(self.driver.find_element(By.ID,'state'))
        signupElement.select_by_value("WA")
        signupElement = self.driver.find_element(By.ID, "city")
        signupElement.send_keys("Perth")
        submitElement = self.driver.find_element(By.ID, "submit")
        submitElement.click()
        errors = self.driver.find_elements('xpath','.//span')
        self.assertEqual(errors[1].text,"[Please use a different username]")
        self.assertEqual(errors[2].text,"[Please use a different email address]")
        self.assertEqual(errors[3].text,"[Passwords must match]")
    
    def test_make_and_delete_post(self):
        self.driver.get("http://localhost:5000/login")
        
        loginElement = self.driver.find_element(By.ID, "username")
        loginElement.send_keys("matt")
        loginElement = self.driver.find_element(By.ID, "password")
        loginElement.send_keys("123456")
        submitElement = self.driver.find_element(By.ID, "submit")
        submitElement.click()

        self.assertEqual(self.driver.current_url,"http://localhost:5000/index")
        
        self.driver.find_element(By.LINK_TEXT, 'Upload').click()
        self.assertEqual(self.driver.current_url,"http://localhost:5000/upload", "Should be on upload page")
        
        uploadElement = Select(self.driver.find_element(By.ID,'post_type'))
        uploadElement.select_by_value("REQUEST")
        
        uploadElement = self.driver.find_element(By.ID, "item_name")
        uploadElement.send_keys("I'd like a pen please!")
        
        uploadElement = self.driver.find_element(By.ID, "desc")
        uploadElement.send_keys("Preferably a blue one!")
        
        submitElement = self.driver.find_element(By.ID, "submit")
        submitElement.click()
        
        self.assertEqual(self.driver.current_url,"http://localhost:5000/index", "Should be on index page")
        
        postElement = self.driver.find_element(By.ID, "1")
        postElement.click()
        
        self.assertEqual(self.driver.current_url,"http://localhost:5000/post/1", "Should be on the post page")
        
        
        postElement = self.driver.find_element(By.ID, "delete")
        postElement.click()
        
        Alert(self.driver).dismiss()
        
        self.assertEqual(self.driver.current_url,"http://localhost:5000/post/1", "Should still be on the post page")
        
        postElement = self.driver.find_element(By.ID, "delete")
        postElement.click()
        
        Alert(self.driver).accept()
        
        messages = self.driver.find_elements(By.CLASS_NAME, "message")
        self.assertEqual(len(messages), 1, f"Expected there to be a single error message")
        self.assertEqual(messages[0].text, "Post I'd like a pen please! deleted")
        self.assertEqual(self.driver.current_url,f"http://localhost:5000/index", "Should've been redirected to index")
        
        self.driver.get("http://localhost:5000/post/1")
        self.assertEqual(self.driver.current_url,"http://localhost:5000/post/1", "Should be on the post page")
        
        headings = self.driver.find_elements('xpath','.//h3')
        self.assertEqual(headings[0].text,"Error in loading item")