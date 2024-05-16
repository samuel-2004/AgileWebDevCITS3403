"""
This module provides controllers and helper functions for the flask application
"""
from math import floor
from datetime import datetime, timezone
import sqlalchemy as sa
from app.models import Post, User, Image, Address
from app import db

def calc_time_ago(timestamp):
    """
    This function converts a timestamp to a formatted string

    :param timestamp: a unix timestamp in UTC time
    
    :returns: a timestamp converted to a readable string

    Sample Usage
        timestamp = 1715670939
        (current time is 1715843839)
        Will return:
        '2 days ago'
    """
    timestamp = timestamp.astimezone(timezone.utc)
    time_difference = datetime.now(timezone.utc) - timestamp
    seconds_ago = int(time_difference.total_seconds())
    intervals = [
        { 'label': 'year',      'seconds': 31536000 },
        { 'label': 'month',     'seconds': 2592000 },
        { 'label': 'day',       'seconds': 86400 },
        { 'label': 'hour',      'seconds': 3600 },
        { 'label': 'minute',    'seconds': 60 }
    ]

    for interval in intervals:
        count = floor(seconds_ago / interval['seconds'])

        if count == 1:
            return f'1 {interval["label"]} ago'
        elif count > 1:
            return f'{count} {interval["label"]}s ago'

    return 'Just now'

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
