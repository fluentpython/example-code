def corrotina():
    print('\t(corrotina) inciciando...')
    x = yield 1
    print('\t(corrotina) recebeu x: %r' % x)
    y = yield 2
    print('\t(corrotina) recebeu y: %r' % y)
    print('\t(corrotina) terminando.')


def principal():
    print('(principal) iniciando...')
    co = corrotina()
    print('(principal) invocando next(co)...')
    res = next(co)
    print('(principal) produzido por next(co): %r' % res)
    print('(principal) invocando co.send(88)...')
    res2 = co.send(88)
    print('(principal) produzido por co.send(88): %r' % res2)
    try:
        print('(principal) invocando co.send(99)...')
        res3 = co.send(99)
        # o print a seguir nunca vai acontecer
        print('(principal) produzido por co.send(99): %r' % res3)
    except StopIteration:
        print('(principal) a corotina nao tem mais valores a produzir')
principal()

