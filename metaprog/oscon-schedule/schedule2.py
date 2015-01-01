import warnings
import inspect

from explore import load_json

DB_NAME = 'schedule2_db'
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, mapping):
        self.__dict__.update(mapping)

    def __eq__(self, other):
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

    def __repr__(self):
        if hasattr(self, 'name'):
            ident = repr(self.name)
        else:
            ident = 'object at ' + hex(id(self))
        cls_name = self.__class__.__name__
        return '<{} {}>'.format(cls_name, ident)


class Event(Record):

    @classmethod
    def set_db(cls, db):
        cls._db = db

    @property
    def venue(self):
        key = self.venue_serial
        return self._db['venue.{}'.format(key)]

    @property
    def speakers(self):
        spkr_serials = self.__dict__['speakers']
        if not hasattr(self, '_speaker_refs'):
            self._speaker_refs = [self._db['speaker.{}'.format(key)]
                                  for key in spkr_serials]
        return self._speaker_refs


def load_db(db):
    raw_data = load_json()
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        rec_type = collection[:-1]
        for fields in rec_list:
            cls_name = rec_type.capitalize()
            cls = globals().get(cls_name, Record)
            if inspect.isclass(cls) and issubclass(cls, Record):
                record = cls(fields)
            else:
                Record(fields)
            key = '{}.{}'.format(rec_type, fields['serial'])
            db[key] = record
