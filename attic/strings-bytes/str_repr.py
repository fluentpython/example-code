
last_len = 0
last_repr = ''
lengths = set()
for i in range(0x110000):
    r = repr(chr(i))[1:-1]
    if len(r) != last_len:
        lengths.add(len(r))
        last_len = len(r)
        if i > 0:
            prev_repr = repr(chr(i-1))[1:-1]
            print('{}'.format(prev_repr))
        print('U+{:04x} {:{max_len}} ...'.format(i, r, max_len=max(lengths)), end=' ')
        last_repr = r
