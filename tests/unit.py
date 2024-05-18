# python -m unittest tests.unittest
from unittest import TestCase

from app import create_app, db
from app.config import TestConfig
from app.models import User, Post, Image
#import time
#import multiprocessing

class BasicTests(TestCase):
    def setUp(self):
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan', email='susan@example.com')
        db.session.add(u)
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))
        self.assertTrue(True)
    
    def test_post(self):
        p = Post(id=1234, post_type="OFFER", item_name="test1", desc = "test description 1", timestamp = "12:00", user_id = 1234, author: "author1")
        db.session.add(p)
        self.assertTrue(p.id==1234)
        self.assertFalse(p.id==1235)

        self.assertTrue(p.post_type=="OFFER")
        self.assertFalse(p.post_type=="REQUEST")

        self.assertTrue(p.item_name=="test1")
        self.assertFalse(p.item_name=="test2")

        self.assertTrue(p.)
        self.assertFalse(p.)

        self.assertTrue(p.)
        self.assertFalse(p.)

        self.assertTrue(p.)
        self.assertFalse(p.)
        # add code
        pass

    def dummy1(self):
        pass

    def dummy2(self):
        pass

    def dummy3(self):
        pass

    def dummy4(self):
        pass

    def dummy5(self):
        pass

    def dummy6(self):
        pass

    def dummy7(self):
        pass

    def dummy8(self):
        pass

    def dummy9(self):
        pass

    def dummy10(self):
        pass


    