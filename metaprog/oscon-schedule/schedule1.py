"""
schedule1.py: traversing OSCON schedule data

    >>> import shelve
    >>> db = shelve.open(DB_NAME)
    >>> if CONFERENCE not in db: load_db(db)
    >>> event = db['event.33950']
    >>> speaker = db['speaker.3471']
    >>> speaker.name
    'Anna Martelli Ravenscroft'
    >>> speaker.twitter
    'annaraven'
    >>> db.close()

"""

import warnings

import osconfeed

DB_NAME = 'data/schedule1_db'
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, mapping):
        self.__dict__.update(mapping)


def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        rec_type = collection[:-1]
        for fields in rec_list:
            key = '{}.{}'.format(rec_type, fields['serial'])
            db[key] = Record(fields)
