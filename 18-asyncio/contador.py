import time
from threading import Thread


def contar(nome, n):
    for i in range(n):
        # time.sleep(.001)
        print(nome, i)


def contar_depois(t1, t2):
    contar(2, 100)
    print('Aguardando t1')
    t1.join()
    print('Aguardando t2')
    t2.join()
    print('Depois do join')

    contar(2, 100)


threads = tuple(Thread(target=contar, args=(i, 10000)) for i in range(2))
depois_t = Thread(target=contar_depois, args=threads)

for t in threads:
    t.start()
depois_t.start()
