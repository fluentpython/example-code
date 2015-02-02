"""
Exemplo adaptado da mensagem do Guido van Rossum em:
https://groups.google.com/forum/#!msg/python-tulip/bmphRrryuFk/aB45sEJUomYJ
http://bit.ly/yieldfrom

    >>> principal(ger2())
    OK
    42

Visualização no PythonTutor: http://goo.gl/pWrlkm

"""

def ger1():
    val = yield 'OK'
    print(val)
    yield  # para evitar o StopIteration

def ger2():
    yield from ger1()

def principal(g):
    print(next(g))
    g.send(42)


# auto-teste
import doctest
doctest.testmod()
