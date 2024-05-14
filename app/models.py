"""
a really really gooddocstring
"""
from datetime import datetime, timezone
from typing import Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login

class Address(db.Model):
    """
    A User's address
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    number:so.Mapped[str] = so.mapped_column(sa.String(8)) # Can have letters, eg. 47A
    street: so.Mapped[str] = so.mapped_column(sa.String(128))
    city: so.Mapped[str] = so.mapped_column(sa.String(32))
    postcode: so.Mapped[str] = so.mapped_column(sa.String(32))
    state: so.Mapped[str] = so.mapped_column(sa.String(32))
    country: so.Mapped[str] = so.mapped_column(sa.String(128))

    resident: so.Mapped['User'] = so.relationship(back_populates='address')

    def __repr__(self) -> str:
        return f'<Address: {self.number} {self.street}, {self.city}, ' + \
                f'{self.postcode}, {self.state}, {self.country}>'

class User(UserMixin, db.Model):
    """
    A User that would use the webpage
    """
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
    address_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Address.id,name="fk_address_id"), index=True)

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')

    address: so.Mapped[Address] = so.relationship(
        back_populates='resident')

    def __repr__(self) -> str:
        return f'<User {self.username} {self.email}>'

    def set_password(self, password):
        """
        Sets the user's password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks that the user's password is correct
        """
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    """
    Allows a user to log in
    """
    return db.session.get(User, int(id))

class Post(db.Model):
    """
    A post class which stores the image and data about the post
    """
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
    """
    :param q: the query that is to be checked against
        if empty, the function will not compare against q
    :param md: the maximum distance away the user should be from the posts
    :param order: how the response should be ordered
        accepts: 'new', 'old', 'close', 'rating'
            new: sorts by newest posts first
            old: sorts by oldest posts first
            close: sorts by closest (by distance) posts first
            rating: sorts by the rating of the poster
    :param lim: the maximum posts to be returned

    :return: a list of posts accessed from the Posts database

    This method should be in the controllers.py file
    """
    query = db.session.query(
            Post.id,Post.post_type,Post.item_name,Post.timestamp,User.username,Address.city,Address.postcode,Image.src
        ).join(User, Post.user_id==User.id).\
        join(Image, Post.id==Image.post_id).\
        join(Address, User.address_id==Address.id)


    # Check if any word in q is in the post name or description
    # This does not take into account the maximum distance
    # Maximum distance will require api calls etc
    if len(q) > 0:
        q = q.split()
        name_conditions = [Post.item_name.like(f'%{word}%') for word in q]
        desc_conditions = [Post.desc.like(f'%{word}%') for word in q]
        query = query.filter(sa.or_(*name_conditions, * desc_conditions))

    if order == "old":
        query = query.order_by(Post.timestamp)
    elif order == "close":
        # need to access distance
        pass
    elif order == "rating":
        # need to access users' points
        pass
    else: #including order == "new"
        query = query.order_by(sa.desc(Post.timestamp))


    #print("\n\n\n",query,"\n\n\n")
    query = query.limit(lim)
    posts = db.session.execute(query).fetchall()
    return posts

class Image(db.Model):
    """
    Stores the source of the image for each post
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    src: so.Mapped[str] = so.mapped_column(sa.String(256))
    post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Post.id), index=True)

    post: so.Mapped[Post] = so.relationship(back_populates='images')

    def __repr__(self) -> str:
        return f'<User {self.id} {self.src} {self.post_id} {self.post.item_name}>'
