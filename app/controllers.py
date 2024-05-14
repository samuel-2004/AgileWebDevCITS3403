"""
This module provides controllers and helper functions for the flask application
"""
from math import floor
from datetime import datetime, timezone

# Calculates the time since posting, and returns a formatted string
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
