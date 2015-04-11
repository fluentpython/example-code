"""
Exemplo adaptado da mensagem do Guido van Rossum em:
https://groups.google.com/forum/#!msg/python-tulip/bmphRrryuFk/aB45sEJUomYJ
http://bit.ly/yieldfrom

    >>> principal_susto(ger2())
    OK
    Bu!

Visualização no PythonTutor: http://goo.gl/QXzQHS

"""

def ger1():
    try:
        val = yield 'OK'
    except RuntimeError as exc:
        print(exc)
    else:
        print(val)
    yield  # para evitar o StopIteration


def ger2():
    yield from ger1()


def principal_susto(g):
    print(next(g))
    g.throw(RuntimeError('Bu!'))


# auto-teste
import doctest
doctest.testmod()
