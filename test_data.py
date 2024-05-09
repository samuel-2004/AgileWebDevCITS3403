from app import flaskApp, db
from app.models import *
flaskApp.app_context().push()
db.drop_all()
db.create_all()
u = User(username='matt', email='matt@example.com')
u.set_password('test')
db.session.add(u)
addr = Address(number="35",street="Stirling Hwy",city="Crawley",postcode="6009",state="WA",country="Australia", resident=u)
db.session.add(addr)
post = Post(post_type = "OFFER", item_name = "Test Item",desc = "Look at my really cool test item", author=u)
db.session.add(post)
image = Image(src = '/static/data/photos/03:01:02_AHDK1011.JPG', post = post)
db.session.add(image)
db.session.commit()
