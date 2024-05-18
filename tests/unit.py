# python -m unittest tests.unittest
from unittest import TestCase

from app import create_app, db
from app.config import TestConfig
from app.models import User, Post, Image, Address
from app.controllers import get_posts
from datetime import datetime
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
        u = User(id = 1234, username='susan', email='susan@example.com')
        a = User(id = 1235, username='Adan', email='adan@example.com')
        db.session.add(u)
        db.session.add(a)
        p = Post(id=1234, post_type="OFFER", item_name="test1", desc = "test description 1", timestamp = datetime(year=2024, month = 1, day = 1), user_id = u.id, author = u)
        db.session.add(p)
        self.assertTrue(p.id==1234)
        self.assertFalse(p.id==1235)

        self.assertTrue(p.post_type=="OFFER")
        self.assertFalse(p.post_type=="REQUEST")

        self.assertTrue(p.item_name=="test1")
        self.assertFalse(p.item_name=="test2")

        self.assertTrue(p.desc == "test description 1")
        self.assertFalse(p.desc == "not test description")

        self.assertTrue(p.timestamp == datetime(year=2024, month = 1, day = 1))
        self.assertFalse(p.timestamp == datetime(year=2023, month = 3, day = 3))

        self.assertTrue(p.user_id == 1234)
        self.assertFalse(p.user_id == 1235)

        self.assertTrue(p.author == u)
        self.assertFalse(p.author == a)

    def test_user(self):
        u = User(id = 1234, username = "testU", email = "testU@test.com", time_created = datetime(year=2024, month = 1, day = 1), bio = "testU bio", points = 0, given = 0, requested = 0)
        a = User(id = 1235, username = "testA", email = "testA@test.com", time_created = datetime(year=2023, month = 3, day = 3), bio = "testA bio", points = 3, given = 3, requested = 3)
        db.session.add(u)
        
        self.assertEqual(u.id, 1234)
        self.assertFalse(u.id == a.id)

        self.assertEqual(u.username, "testU")
        self.assertFalse(u.username == a.username)

        self.assertEqual(u.email, "testU@test.com")
        self.assertFalse(u.email == a.email)

        self.assertEqual(u.time_created, datetime(year=2024, month = 1, day = 1))
        self.assertFalse(u.time_created == a.time_created)

        self.assertEqual(u.bio, "testU bio")
        self.assertFalse(u.bio == a.bio)

        self.assertEqual(u.points, 0)
        self.assertFalse(u.points == a.points)

        self.assertEqual(u.given, 0)
        self.assertFalse(u.given == a.given)

        self.assertEqual(u.requested, 0)
        self.assertFalse(u.requested == a.requested)
        

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

    def test_get_posts(self):
        """
        This function tests the get_posts method in controllers.py
        """
        import warnings

        # Mute the DeprecationWarning
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # Initialise a user
        addr = Address(address_line1="35 wolfram st",address_line2="",suburb="Crawley", \
            city="Perth", postcode="6009",state="WA",country="Australia", \
            latitude="32",longitude="-100")
        u = User(username='susan', email='susan@example.com',address=addr)
        db.session.add(addr)
        db.session.add(u)
        
        ### Testing basic functionality
        # No posts added, should be 0
        self.assertEqual(0, len(list(get_posts())))

        posts = [
            Post(post_type="OFFER", item_name="Test Item", \
                desc="oldest", author=u, \
                timestamp = datetime(year=2022, month = 1, day = 1)),
            Post(post_type="OFFER", item_name="Test Item", \
                desc="middle", author=u, \
                timestamp = datetime(year=2023, month = 1, day = 1)),
            Post(post_type="OFFER", item_name="Test Item", \
                desc="newest", author=u, \
                timestamp = datetime(year=2024, month = 1, day = 1))
        ]
        for p in posts:
            db.session.add(p)
        
        # Three posts added, should be 3
        self.assertEqual(3, len(list(get_posts())))
        
        #get_posts(q="", md=None, order="new", lat=None, lng=None, lim=100):
        
        ### Testing limit
        # Three posts added, limit set to 1, should be 1
        self.assertEqual(1, len(list(get_posts(lim=1))))

        ### Testing distance parameters
        # Three posts added, should be 3
        self.assertEqual(3, len(list(get_posts(lat=10,lng=1))))

        # Three posts added, add max distance
        self.assertEqual(0, len(list(get_posts(md=10,lat=10,lng=1))))

        ### Testing the sort function
        # Oldest
        f = list(get_posts(order="old"))[0]
        self.assertEqual(f.desc, 'oldest', f)

        # Newest
        f = list(get_posts(order="new"))[0]
        self.assertEqual(f.desc, 'newest', f)

        del warnings

