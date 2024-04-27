from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login

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

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
      back_populates='author')

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
  item_name: so.Mapped[str] = so.mapped_column(sa.String(32))
  desc: so.Mapped[str] = so.mapped_column(sa.String(256))
  timestamp: so.Mapped[datetime] = so.mapped_column(
    index=True, default=lambda: datetime.now(timezone.utc))
  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

  author: so.Mapped[User] = so.relationship(back_populates='posts')

  # Post type still needs to be added
  def __repr__(self) -> str:
    return f'<Post {self.id} {self.item_name} {self.desc} {self.timestamp}>'