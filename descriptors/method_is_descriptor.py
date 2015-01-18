"""
# BEGIN FUNC_DESCRIPTOR_DEMO

    >>> word = Text('forward')
    >>> word  # <1>
    Text('forward')
    >>> word.reverse()  # <2>
    Text('drawrof')
    >>> Text.reverse(Text('backward'))  # <3>
    Text('drawkcab')
    >>> type(Text.reverse), type(word.reverse)  # <4>
    (<class 'function'>, <class 'method'>)
    >>> list(map(Text.reverse, ['repaid', (10, 20, 30), Text('stressed')]))  # <5>
    ['diaper', (30, 20, 10), Text('desserts')]
    >>> Text.reverse.__get__(word)  # <6>
    <bound method Text.reverse of Text('forward')>
    >>> Text.reverse.__get__(None, Text)  # <7>
    <function Text.reverse at 0x101244e18>
    >>> word.reverse  # <8>
    <bound method Text.reverse of Text('forward')>
    >>> word.reverse.__self__  # <9>
    Text('forward')
    >>> word.reverse.__func__ is Text.reverse  # <10>
    True

# END FUNC_DESCRIPTOR_DEMO
"""

# BEGIN FUNC_DESCRIPTOR_EX
import collections


class Text(collections.UserString):

    def __repr__(self):
        return 'Text({!r})'.format(self.data)

    def reverse(self):
        return self[::-1]

# END FUNC_DESCRIPTOR_EX
