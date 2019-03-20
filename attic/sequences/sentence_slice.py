"""
SentenceSlice: access words by index, sub-sentences by slices
"""

import re
import reprlib


RE_TOKEN = re.compile(r'\w+|\s+|[^\w\s]+')
RE_WORD = re.compile('\w+')
RE_PUNCTUATION = re.compile(r'[^\w\s]+')


class SentenceSlice:

    def __init__(self, text):
        self.text = text
        self.tokens = RE_TOKEN.findall(text)
        self.words = [t for t in self.tokens if RE_WORD.match(t)]
        self.word_index = [i for i, t in enumerate(self.tokens)
                           if RE_WORD.match(t)]

    def __repr__(self):
        return 'SentenceSlice(%s)' % reprlib.repr(self.text)

    def __getitem__(self, position):
        if isinstance(position, slice):
            if position.step is not None:
                raise LookupError('slice step is not supported')
            start, stop = self._handle_defaults(position)
            start, stop = self._widen(start, stop)
            tokens = self.tokens[start:stop]
            return SentenceSlice(''.join(tokens))
        else:
            return self.words[position]

    def __len__(self, index):
        return len(self.words)

    # helper functions -- implementation detail
    def _handle_defaults(self, position):
        """handle missing or overflow/underflow start/stop"""
        if position.start is None:  # missing
            start = 0
        elif position.start >= len(self.word_index):  # overflow
            start = len(self.tokens)
        else:
            start = self.word_index[position.start]
        if (position.stop is None  # missing
                or position.stop > len(self.word_index)):  # overflow
            stop = self.word_index[-1]
        else:
            stop = self.word_index[position.stop-1]
        return start, stop + 1  # stop after last word selected

    def _widen(self, start, stop):
        """widen range of tokens to get punctuation to the left of
           start and to the right of stop"""
        if start < len(self.tokens):
            while (start > 0 and
                    RE_PUNCTUATION.match(self.tokens[start-1])):
                start -= 1
        while (stop < len(self.tokens) and
                RE_PUNCTUATION.match(self.tokens[stop])):
            stop += 1
        return start, stop
