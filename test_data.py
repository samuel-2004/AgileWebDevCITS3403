from app import flaskApp, db
from app.models import *
flaskApp.app_context().push()
db.session.remove()
db.drop_all()
db.create_all()
#addr = Address(address_line1="69 house lane",address_line2="",suburb="Crawley",city="Crawley",postcode="6009",state="WA",country="Australia",latitude=-31.980,longitude=115.810)
addr1 = Address(address_line1="456 water street",address_line2="",suburb="East Perth",city="Perth",postcode="6004",state="WA",country="Australia",latitude=-31.940,longitude=115.880)
addr2 = Address(address_line1="54 house road",address_line2="",suburb="Wembley",city="Wembley",postcode="6014",state="WA",country="Australia",latitude=-31.940,longitude=115.750)
addr3 = Address(address_line1="34 kensington circle",address_line2="",suburb="Warwick",city="Warwick",postcode="6024",state="WA",country="Australia",latitude=-31.780,longitude=115.770)
addr4 = Address(address_line1="68 chocolate road",address_line2="",suburb="Mundaring",city="Mundaring",postcode="6073",state="WA",country="Australia",latitude=-31.900,longitude=116.170)
addr5 = Address(address_line1="1230 unicorn drive",address_line2="",suburb="Donnybrook",city="Donnybrook",postcode="6239",state="WA",country="Australia",latitude=-33.550,longitude=115.770)
db.session.add(addr1)
db.session.add(addr2)
db.session.add(addr3)
db.session.add(addr4)
db.session.add(addr5)
users = [
    u1 = User(username='matt1', email='matt1@example.com', address = addr1)
    u2 = User(username='matt2', email='matt2@example.com', address = addr2)
    u3 = User(username='matt3', email='matt3@example.com', address = addr3)
    u4 = User(username='matt4', email='matt4@example.com', address = addr4)
    u5 = User(username='matt5', email='matt5@example.com', address = addr5)
]
for u in users:
    db.session.add(u)
db.session.commit()
from random import choice
p = ["OFFER","POST"]
i=["chocolate","chair","desk","nothing","computer","some books","idk","i'm bored of writing these","a mythical creature","sunscreen"]
for q in range(10):
    i_ = i[q]
    u_ = users[q%5]
    p_ = choice(p)
    po = Post(post_type = p_, item_name = i_,desc = "??", author=u_)
    db.session.add(po)
    u_.points += 1
    if p_ == "OFFER":
        u_.given += 1
    else:
        u_.requested += 1
    image = Image(src = '/static/book.jpg', post = po)
    db.session.add(image)
#post = Post(post_type = "OFFER", item_name = "Test Item",desc = "Look at my really cool test item", author=u)
#db.session.add(post)
#u.points += 1
#u.given += 1
#image = Image(src = '/static/book.jpg', post = post)
#db.session.add(image)
db.session.commit()
