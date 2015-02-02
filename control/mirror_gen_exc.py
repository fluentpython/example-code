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

# BEGIN MIRROR_GEN_DEMO_3

    >>> from mirror_gen import looking_glass
    >>> with looking_glass():
    ...      print('Humpty Dumpty')
    ...      x = 1/0  # <1>
    ...      print('END')  # <2>
    ...
    ytpmuD ytpmuH
    Please DO NOT divide by zero!
    >>> with looking_glass():
    ...      print('Humpty Dumpty')
    ...      x = no_such_name  # <1>
    ...      print('END')  # <2>
    ...
    Traceback (most recent call last):
      ...
    NameError: name 'no_such_name' is not defined

# END MIRROR_GEN_DEMO_3

"""


# BEGIN MIRROR_GEN_EX

import contextlib


@contextlib.contextmanager  # <1>
def looking_glass():
    import sys
    original_write = sys.stdout.write  # <2>

    def reverse_write(text):  # <3>
        original_write(text[::-1])

    sys.stdout.write = reverse_write  # <4>
    msg = ''
    try:
        yield 'JABBERWOCKY'  # <5>
    except ZeroDivisionError:  # <6>
        msg = 'Please DO NOT divide by zero!'  # <7>
    except:
        raise  # <8>
    finally:
        sys.stdout.write = original_write  # <9>
        if msg:
            print(msg)  # <10>


# END MIRROR_GEN_EX
