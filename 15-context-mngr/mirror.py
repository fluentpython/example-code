"""
A "mirroring" ``stdout`` context.

While active, the context manager reverses text output to
``stdout``::

# BEGIN MIRROR_DEMO_1

    >>> from mirror import LookingGlass
    >>> with LookingGlass() as what:  # <1>
    ...      print('Alice, Kitty and Snowdrop')  # <2>
    ...      print(what)
    ...
    pordwonS dna yttiK ,ecilA  # <3>
    YKCOWREBBAJ
    >>> what  # <4>
    'JABBERWOCKY'
    >>> print('Back to normal.')  # <5>
    Back to normal.

# END MIRROR_DEMO_1


This exposes the context manager operation::

# BEGIN MIRROR_DEMO_2

    >>> from mirror import LookingGlass
    >>> manager = LookingGlass()  # <1>
    >>> manager
    <mirror.LookingGlass object at 0x2a578ac>
    >>> monster = manager.__enter__()  # <2>
    >>> monster == 'JABBERWOCKY'  # <3>
    eurT
    >>> monster
    'YKCOWREBBAJ'
    >>> manager
    >ca875a2x0 ta tcejbo ssalGgnikooL.rorrim<
    >>> manager.__exit__(None, None, None)  # <4>
    >>> monster
    'JABBERWOCKY'

# END MIRROR_DEMO_2

The context manager can handle and "swallow" exceptions.

# BEGIN MIRROR_DEMO_3

    >>> from mirror import LookingGlass
    >>> with LookingGlass():
    ...      print('Humpty Dumpty')
    ...      x = 1/0  # <1>
    ...      print('END')  # <2>
    ...
    ytpmuD ytpmuH
    Please DO NOT divide by zero!
    >>> with LookingGlass():
    ...      print('Humpty Dumpty')
    ...      x = no_such_name  # <1>
    ...      print('END')  # <2>
    ...
    Traceback (most recent call last):
      ...
    NameError: name 'no_such_name' is not defined

# END MIRROR_DEMO_3

"""


# BEGIN MIRROR_EX
class LookingGlass:

    def __enter__(self):  # <1>
        import sys
        self.original_write = sys.stdout.write  # <2>
        sys.stdout.write = self.reverse_write  # <3>
        return 'JABBERWOCKY'  # <4>

    def reverse_write(self, text):  # <5>
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_value, traceback):  # <6>
        import sys  # <7>
        sys.stdout.write = self.original_write  # <8>
        if exc_type is ZeroDivisionError:  # <9>
            print('Please DO NOT divide by zero!')
            return True  # <10>
        # <11>


# END MIRROR_EX
