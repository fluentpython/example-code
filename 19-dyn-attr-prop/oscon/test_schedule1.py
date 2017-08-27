import os
import shelve

import pytest

import schedule1 as schedule

DB_NAME = 'data/test_db'


@pytest.fixture(scope='module')
def db():
    with shelve.open(DB_NAME) as the_db:
        if schedule.CONFERENCE not in the_db:
            schedule.load_db(the_db)
        yield the_db
        os.remove(DB_NAME)


def test_record_class():
    rec = schedule.Record(spam=99, eggs=12)
    assert rec.spam == 99
    assert rec.eggs == 12


def test_conference_record(db):
    assert schedule.CONFERENCE in db


def test_speaker_record(db):
    speaker = db['speaker.3471']
    assert speaker.name == 'Anna Martelli Ravenscroft'


def test_event_record(db):
    event = db['event.33950']
    assert event.name == 'There *Will* Be Bugs'


def test_event_venue(db):
    event = db['event.33950']
    assert event.venue_serial == 1449
