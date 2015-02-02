"""
Exemplo adaptado da mensagem do Guido van Rossum em:
https://groups.google.com/forum/#!msg/python-tulip/bmphRrryuFk/aB45sEJUomYJ
http://bit.ly/yieldfrom

    >>> principal(ger2())
    OK
    None

Visualização no PythonTutor: http://goo.gl/61CUcA

"""

def ger1():
    val = yield 'OK'
    print(val)
    yield  # para evitar o StopIteration

def ger2():
    for i in ger1():
        yield i

def principal(g):
    print(next(g))
    g.send(42)


# auto-teste
import doctest
doctest.testmod()
