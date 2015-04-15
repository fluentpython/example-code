
if 'raw_input' in dir(__builtins__):
    input = raw_input  # para funcionar com Python 2

def ler_num():
    num = input('+: ')
    try:
        num = float(num)
    except ValueError:
        return 0
    return num

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
    next(coro)
    while True:
        item = ler_num()
        if item:
            coro.send(item)
        else:
            print('Fechando corotina...')
            coro.close()
            break

if __name__=='__main__':
    main()
