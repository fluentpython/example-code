"""string concatenation demos"""

from time import perf_counter

def load_lines():
    with open('war-and-peace.txt') as fp:
        return fp.readlines() * 100  # replace with 200 or more for surprises!!!

def chrono(f):
    def inner(lines):
        t0 = perf_counter()
        text = f(lines)
        elapsed = perf_counter() - t0
        print('%15s: %fs' % (f.__name__, elapsed))
        return text
    return inner

@chrono
def iadd_joiner(lines):
    text = ''
    for line in lines:
        text += line
    return text

@chrono
def list_joiner(lines):
    parts = []
    for line in lines:
        parts.append(line)
    return ''.join(parts)

@chrono
def genexp_joiner(lines):
    return ''.join(line for line in lines)

if __name__=='__main__':
    lines = load_lines()
    print('joining %s lines' % len(lines))
    text0 = iadd_joiner(lines)
    text1 = list_joiner(lines)
    text2 = genexp_joiner(lines)
    assert len(text0) == len(text1) == len(text2), repr(
        (len(text0), len(text1), len(text2)))
