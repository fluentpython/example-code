"""
Wikipedia Picture of the Day (POTD) download example
"""

import pytest

from daypicts import *


@pytest.mark.network
def test_get_picture_url_existing():
    url = get_picture_url('2012-01-01')
    expected = ('http://upload.wikimedia.org/wikipedia/commons/'
                'thumb/9/9d/MODIS_Map.jpg/550px-MODIS_Map.jpg')
    assert url == expected


@pytest.mark.network
def test_get_picture_url_not_existing():
    with pytest.raises(NoPictureForDate):
        get_picture_url('2013-09-12')


def test_validate_full_date():
    parts = validate_date('2015-1-2')
    assert parts == '2015-01-02'


def test_validate_date_too_early():
    with pytest.raises(NoPictureTemplateBefore):
        validate_date('2006-12-31')


def test_validate_month():
    parts = validate_date('2015-1')
    assert parts == '2015-01'


def test_validate_year():
    parts = validate_date('2015')
    assert parts == '2015'


def test_gen_month_dates():
    dates = list(gen_month_dates('2015-02'))
    assert len(dates) == 28
    assert dates[0] == '2015-02-01'
    assert dates[27] == '2015-02-28'


def test_gen_month_dates_leap():
    dates = list(gen_month_dates('2012-02'))
    assert len(dates) == 29
    assert dates[28] == '2012-02-29'


def test_gen_year_dates():
    dates = list(gen_year_dates('2015'))
    assert len(dates) == 365
    assert dates[0] == '2015-01-01'
    assert dates[364] == '2015-12-31'


def test_gen_year_dates_leap():
    dates = list(gen_year_dates('2012'))
    assert len(dates) == 366
    assert dates[365] == '2012-12-31'


GIF_MIN = (b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00'
           b'\x00\x00\x01\x00\x01\x00\x00\x02\x00;')
SVG_MIN = b'<svg xmlns="http://www.w3.org/2000/svg"></svg>'
SVG_XML_DECL = b'<?xml version="1.0" encoding="UTF-8"?>' + SVG_MIN
NOISE = b'\xb0\x0bU\xbe]L\n\x92\xbe\xc6\xf65"\xcc\xa3\xe3'

def test_picture_type_imghdr():
    assert picture_type(GIF_MIN) == 'gif'


def test_picture_type_svg():
    assert picture_type(SVG_MIN) == 'svg'
    assert picture_type(SVG_XML_DECL) == 'svg'


def test_picture_type_unknown():
    assert picture_type(NOISE) is None

