"""
This module provides controllers and helper functions for the flask application
"""
from math import floor, radians, cos, sin, asin, sqrt
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

def haversine_distance(lat1,lng1,lat2,lng2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    Uses the haversine formula
    :param lat1, lng1: first coordinate pair
    :param lat2, lng2: second coordinate pair
    :return: The distance between the points in kilometers.
    See https://stackoverflow.com/a/4913653 for the implementation
    """
    # convert decimal degrees to radians
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    # haversine formula 
    dlon = lng2 - lng1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers.
    out = c * r
    return out
def is_within_max_distance(md,lat1,lng1,lat2,lng2):
    """
    Calculates if the distance between two coordinate pairs is less than the given maximum distance
    :param md: maximum distance the pairs can be
    :param lat1, lng1: first coordinate pair
    :param lat2, lng2: second coordinate pair
    :return: True if the distance is less than the max distance, False otherwise
    """
    return haversine_distance(lat1,lng1,lat2,lng2) <= md
def get_posts(q="", md=None, order="new", lat=None, lng=None, lim=100):
    db.session.connection().connection.create_function("is_within_max_distance", 5, is_within_max_distance)
    db.session.connection().connection.create_function("haversine_distance", 4, haversine_distance)
    query = db.session.query(Post).join(User).join(Address)
    # Check if any word in q is in the post name or description
    # This does not take into account the maximum distance
    # Maximum distance will require api calls etc
    if (len(q) > 0):
        q = q.split()
        name_conditions = [Post.item_name.like('%{}%'.format(word)) for word in q]
        desc_conditions = [Post.desc.like('%{}%'.format(word)) for word in q]
        query = query.filter(sa.or_(*name_conditions, * desc_conditions))

    if md is not None and lat is not None and lng is not None:
        # convert inputs to floats
        md, lng, lat = map(float, [md, lng, lat])
        query = query.filter(func.is_within_max_distance(md,lat,lng,Address.latitude,Address.longitude))

    if order == "new":
        query = query.order_by(sa.desc(Post.timestamp))
    elif order == "old":
        query = query.order_by(Post.timestamp)
    elif order == "rating":
        query = query.order_by(User.points)
    elif md is not None and lat is not None and lng is not None:
        if order == "close":
            query = query.order_by(func.haversine_distance(lat,lng,Address.latitude,Address.longitude))
    query = query.limit(lim)
    posts = db.session.scalars(query)
    return posts
