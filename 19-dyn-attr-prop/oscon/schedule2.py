"""
schedule2.py: traversing OSCON schedule data

    >>> import shelve
    >>> db = shelve.open(DB_NAME)
    >>> if CONFERENCE not in db: load_db(db)

# BEGIN SCHEDULE2_DEMO

    >>> DbRecord.set_db(db)  # <1>
    >>> event = DbRecord.fetch('event.33950')  # <2>
    >>> event  # <3>
    <Event 'There *Will* Be Bugs'>
    >>> event.venue  # <4>
    <DbRecord serial='venue.1449'>
    >>> event.venue.name  # <5>
    'Portland 251'
    >>> for spkr in event.speakers:  # <6>
    ...     print('{0.serial}: {0.name}'.format(spkr))
    ...
    speaker.3471: Anna Martelli Ravenscroft
    speaker.5199: Alex Martelli

# END SCHEDULE2_DEMO

    >>> db.close()

"""

# BEGIN SCHEDULE2_RECORD
import warnings
import inspect  # <1>

import osconfeed

DB_NAME = 'data/schedule2_db'  # <2>
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):  # <3>
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented
# END SCHEDULE2_RECORD


# BEGIN SCHEDULE2_DBRECORD
class MissingDatabaseError(RuntimeError):
    """Raised when a database is required but was not set."""  # <1>


class DbRecord(Record):  # <2>

    __db = None  # <3>

    @staticmethod  # <4>
    def set_db(db):
        DbRecord.__db = db  # <5>

    @staticmethod  # <6>
    def get_db():
        return DbRecord.__db

    @classmethod  # <7>
    def fetch(cls, ident):
        db = cls.get_db()
        try:
            return db[ident]  # <8>
        except TypeError:
            if db is None:  # <9>
                msg = "database not set; call '{}.set_db(my_db)'"
                raise MissingDatabaseError(msg.format(cls.__name__))
            else:  # <10>
                raise

    def __repr__(self):
        if hasattr(self, 'serial'):  # <11>
            cls_name = self.__class__.__name__
            return '<{} serial={!r}>'.format(cls_name, self.serial)
        else:
            return super().__repr__()  # <12>
# END SCHEDULE2_DBRECORD


# BEGIN SCHEDULE2_EVENT
class Event(DbRecord):  # <1>

    @property
    def venue(self):
        key = 'venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key)  # <2>

    @property
    def speakers(self):
        if not hasattr(self, '_speaker_objs'):  # <3>
            spkr_serials = self.__dict__['speakers']  # <4>
            fetch = self.__class__.fetch  # <5>
            self._speaker_objs = [fetch('speaker.{}'.format(key))
                                  for key in spkr_serials]  # <6>
        return self._speaker_objs  # <7>

    def __repr__(self):
        if hasattr(self, 'name'):  # <8>
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)
        else:
            return super().__repr__()  # <9>
# END SCHEDULE2_EVENT


# BEGIN SCHEDULE2_LOAD
def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        record_type = collection[:-1]  # <1>
        cls_name = record_type.capitalize()  # <2>
        cls = globals().get(cls_name, DbRecord)  # <3>
        if inspect.isclass(cls) and issubclass(cls, DbRecord):  # <4>
            factory = cls  # <5>
        else:
            factory = DbRecord  # <6>
        for record in rec_list:  # <7>
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = factory(**record)  # <8>
# END SCHEDULE2_LOAD
