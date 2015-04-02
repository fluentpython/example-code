from itertools import groupby

def bare_repr(codepoint):
    return repr(chr(codepoint))[1:-1]

def display(codepoint):
    repstr = repr(chr(codepoint))[1:-1]
    print('U+{:04x} {:{max_len}}'.format(
            codepoint, repstr, max_len=max(lengths)))

def repr_shape(codepoint):
    brepr = bare_repr(codepoint)
    if len(brepr) == 1:
        shape = 'GLYPH'
    else:
        shape = brepr[:2]
        escapes.add(shape)
    return len(brepr), shape

escapes = set()

group_gen = groupby((codepoint for codepoint in range(0x110000)), repr_shape)

for len_shape, group in group_gen:
    len_brepr, shape = len_shape
    group = list(group)
    cp_first = group[0]
    cp_last = group[-1]
    cp_mid = group[len(group)//2]
    if len(group) == 1:
        glyph_sample = bare_repr(cp_first) if shape == 'GLYPH' else ''
        print('{:6d} U+{:04X}          {:5} {}'.format(
            len(group), cp_first, shape, glyph_sample))
    else:
        if len(group) == 2:
            if shape == 'GLYPH':
                glyph_sample = bare_repr(cp_first) + ' ' + bare_repr(cp_last)
            else:
                glyph_sample = ''
            print('{:6d} U+{:04X} , U+{:04X} {:5} {}'.format(
                len(group), cp_first, cp_last, shape, glyph_sample))
        else:
            if shape == 'GLYPH':
                glyph_sample = ' '.join([bare_repr(cp_first),
                                    bare_repr(cp_mid), bare_repr(cp_last)])
            else:
                glyph_sample = ''
            print('{:6d} U+{:04X}...U+{:04X} {:5} {}'.format(
                len(group), cp_first, cp_last, shape, glyph_sample))
print('escapes:', ' '.join(sorted(escapes, key=str.upper)))
