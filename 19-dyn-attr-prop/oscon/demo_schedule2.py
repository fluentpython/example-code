import shelve

from schedule2 import DB_NAME, CONFERENCE, load_db
from schedule2 import DbRecord, Event

with shelve.open(DB_NAME) as db:
    if CONFERENCE not in db:
        load_db(db)
    
    DbRecord.set_db(db)
    event = DbRecord.fetch('event.33950')
    print(event)
    print(event.venue)
    print(event.venue.name)
    for spkr in event.speakers:
        print('{0.serial}: {0.name}'.format(spkr))
        
    print(repr(Event.venue))
    
    event2 = DbRecord.fetch('event.33451')
    print(event2)
    print(event2.fetch)
    print(event2.venue)