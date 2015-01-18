"""
schedule1.py: traversing OSCON schedule data

# BEGIN SCHEDULE1_DEMO
    >>> import shelve
    >>> db = shelve.open(DB_NAME)  # <1>
    >>> if CONFERENCE not in db:  # <2>
    ...     load_db(db)  # <3>
    ...
    >>> speaker = db['speaker.3471']  # <4>
    >>> type(speaker)  # <5>
    <class 'schedule1.Record'>
    >>> speaker.name, speaker.twitter  # <6>
    ('Anna Martelli Ravenscroft', 'annaraven')
    >>> db.close()  # <7>

# END SCHEDULE1_DEMO

"""

# BEGIN SCHEDULE1
import warnings

import osconfeed  # <1>

DB_NAME = 'data/schedule1_db'
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)  # <2>


def load_db(db):
    raw_data = osconfeed.load()  # <3>
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():  # <4>
        record_type = collection[:-1]  # <5>
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])  # <6>
            record['serial'] = key  # <7>
            db[key] = Record(**record)  # <8>

# END SCHEDULE1
