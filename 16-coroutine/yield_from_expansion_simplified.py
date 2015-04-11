# Code below is a very simplified expansion of the statement:
#
# RESULT = yield from EXPR
#
# This code assumes that the subgenerator will run to completion,
# without the client ever calling ``.throw()`` or ``.close()``.
# Also, this code makes no distinction between the client
# calling ``next(subgen)`` or ``subgen.send(...)``
#
# The full expansion is in:
# PEP 380 -- Syntax for Delegating to a Subgenerator
#
# https://www.python.org/dev/peps/pep-0380/#formal-semantics


# BEGIN YIELD_FROM_EXPANSION_SIMPLIFIED
_i = iter(EXPR)  # <1>
try:
    _y = next(_i)  # <2>
except StopIteration as _e:
    _r = _e.value  # <3>
else:
    while 1:  # <4>
        _s = yield _y  # <5>
        try:
            _y = _i.send(_s)  # <6>
        except StopIteration as _e:  # <7>
            _r = _e.value
            break

RESULT = _r  # <8>
# END YIELD_FROM_EXPANSION_SIMPLIFIED
