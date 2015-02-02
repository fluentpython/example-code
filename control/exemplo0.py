def corrotina():
    print('\t(corrotina) inciciando...')
    x = yield
    print('\t(corrotina) recebeu x: %r' % x)
    y = yield
    print('\t(corrotina) recebeu y: %r' % y)
    print('\t(corrotina) terminando.')


def principal():
    print('(principal) iniciando...')
    co = corrotina()
    print('(principal) invocando next(co)...')
    next(co)
    print('(principal) invocando co.send(88)...')
    co.send(88)
    try:
        print('(principal) invocando co.send(99)...')
        co.send(99)
        # o print a seguir nunca vai acontecer
        print('(principal) invocado co.send(99)')
    except StopIteration:
        print('(principal) a corotina nao tem mais valores a produzir')

principal()
