from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login

class Address(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    address_line1: so.Mapped[str] = so.mapped_column(sa.String(64))
    address_line2: so.Mapped[str] = so.mapped_column(sa.String(64))
    suburb: so.Mapped[str] = so.mapped_column(sa.String(32))
    postcode: so.Mapped[str] = so.mapped_column(sa.String(32))
    city: so.Mapped[str] = so.mapped_column(sa.String(32))
    state: so.Mapped[str] = so.mapped_column(sa.String(32))
    country: so.Mapped[str] = so.mapped_column(sa.String(128))
    
    resident: so.Mapped['User'] = so.relationship(back_populates='address')
    
    def __repr__(self) -> str:
        return f'<Address: {self.number} {self.street}, {self.city}, {self.postcode}, {self.state}, {self.country}>'
    

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    time_created: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    bio: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    pic: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    points: so.Mapped[int] = so.mapped_column(default=0)
    given: so.Mapped[int] = so.mapped_column(default=0)
    requested: so.Mapped[int] = so.mapped_column(default=0)
    address_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Address.id,name="fk_address_id"), index=True)

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')
    
    address: so.Mapped[Address] = so.relationship(
        back_populates='resident')
    
    def increment_stats(self, post):
        self.points += 1
        if post.post_type == "OFFER":
            self.given += 1
        elif post.post_type == "REQUEST":
            self.requested += 1

    def __repr__(self) -> str:
        return f'<User {self.username} {self.email}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
        return db.session.get(User, int(id))

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    post_type: so.Mapped[str] = so.mapped_column(sa.String(8))
    item_name: so.Mapped[str] = so.mapped_column(sa.String(32))
    desc: so.Mapped[str] = so.mapped_column(sa.String(256))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')
    images: so.Mapped['Image'] = so.relationship(back_populates='post')



    def __repr__(self) -> str:
        return f'<Post {self.id} {self.item_name} {self.desc} {self.timestamp}>'

def get_posts(q="", md=None, order="new", lim=100):
    query = db.session.query(Post)

    # Check if any word in q is in the post name or description
    # This does not take into account the maximum distance
    # Maximum distance will require api calls etc
    if (len(q) > 0):
        q = q.split()
        name_conditions = [Post.item_name.like('%{}%'.format(word)) for word in q]
        desc_conditions = [Post.desc.like('%{}%'.format(word)) for word in q]
        query = query.filter(sa.or_(*name_conditions, * desc_conditions))
        
    if order == "new":
        query = query.order_by(sa.desc(Post.timestamp))
    elif order == "old":
        query = query.order_by(Post.timestamp)
    elif order == "close":
        # need to access distance
        pass
    elif order == "rating":
        # need to access users' points
        pass

    query = query.limit(lim)
    posts = db.session.scalars(query)
    return posts

  
class Image(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    src: so.Mapped[str] = so.mapped_column(sa.String(256))
    post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Post.id), index=True)
    
    post: so.Mapped[Post] = so.relationship(back_populates='images')
    
    def __repr__(self) -> str:
        return f'<User {self.id} {self.src} {self.post_id} {self.post.item_name}>'
