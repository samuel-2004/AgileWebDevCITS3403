from math import floor
import time

# Calculates the time since posting, and returns a formatted string
def calcTimeAgo(timestamp):
    secondsAgo = floor(time.time() - timestamp)
    intervals = [
        { 'label': 'year',      'seconds': 31536000 },
        { 'label': 'month',     'seconds': 2592000 },
        { 'label': 'day',       'seconds': 86400 },
        { 'label': 'hour',      'seconds': 3600 },
        { 'label': 'minute',    'seconds': 60 }
    ]

    for i in range(len(intervals)):
        interval = intervals[i]
        count = floor(secondsAgo / interval['seconds'])

        if count > 0:
            return f'1 {interval["label"]} ago' if count == 1 else f'{count} {interval["label"]}s ago'
        
        
    return 'Just now'