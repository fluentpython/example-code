import pytest

from charfinder import UnicodeNameIndex, tokenize, sample_chars, query_type
from unicodedata import name


@pytest.fixture
def sample_index():
    return UnicodeNameIndex(sample_chars)


@pytest.fixture(scope="module")
def full_index():
    return UnicodeNameIndex()


def test_query_type():
    assert query_type('blue') == 'NAME'


def test_tokenize():
    assert list(tokenize('')) == []
    assert list(tokenize('a b')) == ['A', 'B']
    assert list(tokenize('a-b')) == ['A', 'B']
    assert list(tokenize('abc')) == ['ABC']
    assert list(tokenize('café')) == ['CAFÉ']


def test_index():
    sample_index = UnicodeNameIndex(sample_chars)
    assert len(sample_index.index) == 9


def test_find_word_no_match(sample_index):
    res = sample_index.find_chars('qwertyuiop')
    assert len(res.items) == 0


def test_find_word_1_match(sample_index):
    res = [(ord(char), name(char))
           for char in sample_index.find_chars('currency').items]
    assert res == [(8352, 'EURO-CURRENCY SIGN')]


def test_find_word_1_match_character_result(sample_index):
    res = [name(char) for char in
           sample_index.find_chars('currency').items]
    assert res == ['EURO-CURRENCY SIGN']


def test_find_word_2_matches(sample_index):
    res = [(ord(char), name(char))
           for char in sample_index.find_chars('Euro').items]
    assert res == [(8352, 'EURO-CURRENCY SIGN'),
                   (8364, 'EURO SIGN')]


def test_find_2_words_no_matches(sample_index):
    res = sample_index.find_chars('Euro letter')
    assert res.count == 0


def test_find_2_words_no_matches_because_one_not_found(sample_index):
    res = sample_index.find_chars('letter qwertyuiop')
    assert res.count == 0


def test_find_2_words_1_match(sample_index):
    res = sample_index.find_chars('sign dollar')
    assert res.count == 1


def test_find_2_words_2_matches(sample_index):
    res = sample_index.find_chars('latin letter')
    assert res.count == 2


def test_find_chars_many_matches_full(full_index):
    res = full_index.find_chars('letter')
    assert res.count > 7000


def test_find_1_word_1_match_full(full_index):
    res = [(ord(char), name(char))
           for char in full_index.find_chars('registered').items]
    assert res == [(174, 'REGISTERED SIGN')]


def test_find_1_word_2_matches_full(full_index):
    res = full_index.find_chars('rook')
    assert res.count == 2


def test_find_3_words_no_matches_full(full_index):
    res = full_index.find_chars('no such character')
    assert res.count == 0


def test_find_with_start(sample_index):
    res = [(ord(char), name(char))
           for char in sample_index.find_chars('sign', 1).items]
    assert res == [(8352, 'EURO-CURRENCY SIGN'), (8364, 'EURO SIGN')]


def test_find_with_stop(sample_index):
    res = [(ord(char), name(char))
           for char in sample_index.find_chars('sign', 0, 2).items]
    assert res == [(36, 'DOLLAR SIGN'), (8352, 'EURO-CURRENCY SIGN')]


def test_find_with_start_stop(sample_index):
    res = [(ord(char), name(char))
           for char in sample_index.find_chars('sign', 1, 2).items]
    assert res == [(8352, 'EURO-CURRENCY SIGN')]

