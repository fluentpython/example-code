
if 'raw_input' in dir(__builtins__):
    input = raw_input  # para funcionar com Python 2

def ler_parcela():
    parcela = input('+: ')
    try:
        parcela = float(parcela)
    except ValueError:
        return 0
    return parcela

# decorator
def coro(func):
    def start(*args, **kwargs):
        g = func(*args, **kwargs)
        next(g)
        return g
    return start

@coro
def somadora():
    qt_parcelas = 0
    total = 0
    try:
        while True:
            parcela = yield
            qt_parcelas += 1
            total += parcela

            print('parcelas: %d  total: %d' % (qt_parcelas, total))
    finally:
        print('parcelas: %d  total: %d  media: %d' % (qt_parcelas, total, total/qt_parcelas))

def main():
    coro = somadora()
    while True:
        parcela = ler_parcela()
        if parcela:
            coro.send(parcela)
        else:
            print('Fechando corotina...')
            coro.close()
            break

if __name__=='__main__':
    main()
