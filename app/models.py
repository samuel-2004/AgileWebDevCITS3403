from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
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