from app import flaskApp, db
from app.models import *
flaskApp.app_context().push()
db.session.remove()
db.drop_all()
db.create_all()
addr = Address(address_line1="69 house lane",address_line2="",suburb="Crawley",city="Crawley",postcode="6009",state="WA",country="Australia",latitude=-31.980,longitude=115.810)
db.session.add(addr)
u = User(username='qwerty', email='matt@example.com', address = addr)
u.set_password('qwerty')
db.session.add(u)
db.session.commit()
post = Post(post_type = "OFFER", item_name = "Test Item",desc = "Look at my really cool test item", author=u)
db.session.add(post)
u.points += 1
u.given += 1
image = Image(src = '/static/book.jpg', post = post)
db.session.add(image)
db.session.commit()
