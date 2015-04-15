"""
A "mirroring" ``stdout`` context manager.

While active, the context manager reverses text output to
``stdout``::

# BEGIN MIRROR_GEN_DEMO_1

    >>> from mirror_gen import looking_glass
    >>> with looking_glass() as what:  # <1>
    ...      print('Alice, Kitty and Snowdrop')
    ...      print(what)
    ...
    pordwonS dna yttiK ,ecilA
    YKCOWREBBAJ
    >>> what
    'JABBERWOCKY'

# END MIRROR_GEN_DEMO_1


This exposes the context manager operation::

# BEGIN MIRROR_GEN_DEMO_2

    >>> from mirror_gen import looking_glass
    >>> manager = looking_glass()  # <1>
    >>> manager  # doctest: +ELLIPSIS
    <contextlib._GeneratorContextManager object at 0x...>
    >>> monster = manager.__enter__()  # <2>
    >>> monster == 'JABBERWOCKY'  # <3>
    eurT
    >>> monster
    'YKCOWREBBAJ'
    >>> manager  # doctest: +ELLIPSIS
    >...x0 ta tcejbo reganaMtxetnoCrotareneG_.biltxetnoc<
    >>> manager.__exit__(None, None, None)  # <4>
    >>> monster
    'JABBERWOCKY'

# END MIRROR_GEN_DEMO_2

The context manager can handle and "swallow" exceptions.
The following test does not pass under doctest (a
ZeroDivisionError is reported by doctest) but passes
if executed by hand in the Python 3 console (the exception
is handled by the context manager):

# BEGIN MIRROR_GEN_DEMO_3

    >>> from mirror_gen import looking_glass
    >>> with looking_glass():
    ...      print('Humpty Dumpty')
    ...      x = 1/0  # <1>
    ...      print('END')  # <2>
    ...
    ytpmuD ytpmuH
    Please DO NOT divide by zero!

# END MIRROR_GEN_DEMO_3

    >>> with looking_glass():
    ...      print('Humpty Dumpty')
    ...      x = no_such_name  # <1>
    ...      print('END')  # <2>
    ...
    Traceback (most recent call last):
      ...
    NameError: name 'no_such_name' is not defined



"""


# BEGIN MIRROR_GEN_EXC

import contextlib


@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    msg = ''  # <1>
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:  # <2>
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write  # <3>
        if msg:
            print(msg)  # <4>


# END MIRROR_GEN_EXC
