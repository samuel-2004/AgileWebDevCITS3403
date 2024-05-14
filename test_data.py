from app import flaskApp, db
from app.models import *
flaskApp.app_context().push()
db.session.remove()
db.drop_all()
db.create_all()
addr = Address(number="35",street="Stirling Hwy",city="Crawley",postcode="6009",state="WA",country="Australia")
db.session.add(addr)
u = User(username='matt', email='matt@example.com', address = addr)
u.set_password('test')
db.session.add(u)
db.session.commit()
post = Post(post_type = "OFFER", item_name = "Test Item",desc = "Look at my really cool test item", author=u)
db.session.add(post)
u.points += 1
u.given += 1
image = Image(src = '/static/book.jpg', post = post)
db.session.add(image)
db.session.commit()
