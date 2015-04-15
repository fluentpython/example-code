# Code below is the expansion of the statement:
#
# RESULT = yield from EXPR
#
# Copied verbatim from the Formal Semantics section of
# PEP 380 -- Syntax for Delegating to a Subgenerator
#
# https://www.python.org/dev/peps/pep-0380/#formal-semantics


# BEGIN YIELD_FROM_EXPANSION
_i = iter(EXPR)  # <1>
try:
    _y = next(_i)  # <2>
except StopIteration as _e:
    _r = _e.value  # <3>
else:
    while 1:  # <4>
        try:
            _s = yield _y  # <5>
        except GeneratorExit as _e:  # <6>
            try:
                _m = _i.close
            except AttributeError:
                pass
            else:
                _m()
            raise _e
        except BaseException as _e:  # <7>
            _x = sys.exc_info()
            try:
                _m = _i.throw
            except AttributeError:
                raise _e
            else:  # <8>
                try:
                    _y = _m(*_x)
                except StopIteration as _e:
                    _r = _e.value
                    break
        else:  # <9>
            try:  # <10>
                if _s is None:  # <11>
                    _y = next(_i)
                else:
                    _y = _i.send(_s)
            except StopIteration as _e:  # <12>
                _r = _e.value
                break

RESULT = _r  # <13>
# END YIELD_FROM_EXPANSION
