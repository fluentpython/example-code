"""
Paragraph: iterate over sentences and words with generator functions.
The ``.words()`` generator shows the use of ``yield from``.

::
    >>> p = Paragraph("The cat. The mat. Is the cat on the mat?"
    ...               " The cat is on the mat.")
    >>> for s in p:
    ...     print(s)
    ...
    Sentence('The cat.')
    Sentence('The mat.')
    Sentence('Is the cat on the mat?')
    Sentence('The cat is on the mat.')
    >>> list(p.words())  # doctest: +NORMALIZE_WHITESPACE
    ['The', 'cat', 'The', 'mat', 'Is', 'the', 'cat', 'on',
    'the', 'mat', 'The', 'cat', 'is', 'on', 'the', 'mat']


.. Note:: sample text from `McGuffey's First Eclectic Reader`__

__ http://www.gutenberg.org/cache/epub/14640/pg14640.txt
"""

import re
import reprlib

from sentence_gen import Sentence


RE_SENTENCE = re.compile('([^.!?]+[.!?]+)')


class Paragraph:

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Paragraph(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for match in RE_SENTENCE.finditer(self.text):
            yield Sentence(match.group().strip())

    def words(self):
        for sentence in self:
            yield from sentence
