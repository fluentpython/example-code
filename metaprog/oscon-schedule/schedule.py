"""

>>> db = shelve.open(DB_NAME)
>>> if CONFERENCE not in db: load_db(db)
>>> event = db['event.33950']
>>> record = db['speaker.3471']
>>> record.name
'Anna Martelli Ravenscroft'
>>> record.twitter
'annaraven'
>>> db.close()

"""

import warnings
import shelve

from explore import load_json

DB_NAME = 'schedule_db'
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, mapping):
        self.__dict__.update(mapping)


def load_db(db):
    raw_data = load_json()
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        rec_type = collection[:-1]
        for fields in rec_list:
            key = '{}.{}'.format(rec_type, fields['serial'])
            db[key] = Record(fields)
