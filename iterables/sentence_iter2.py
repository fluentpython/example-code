"""
Sentence: iterate over words using the Iterator Pattern, take #2

WARNING: the Iterator Pattern is much simpler in idiomatic Python;
see: sentence_gen*.py.
"""

import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        word_iter = RE_WORD.finditer(self.text)  # <1>
        return SentenceIter(word_iter)  # <2>


class SentenceIter():

    def __init__(self, word_iter):
        self.word_iter = word_iter  # <3>

    def __next__(self):
        match = next(self.word_iter)  # <4>
        return match.group()  # <5>

    def __iter__(self):
        return self
