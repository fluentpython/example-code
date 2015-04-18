# clockdeco_param.py

"""
>>> snooze(.1)  # doctest: +ELLIPSIS
[0.101...s] snooze(0.1) -> None
>>> clock('{name}: {elapsed}')(time.sleep)(.2)  # doctest: +ELLIPSIS
sleep: 0.20...
>>> clock('{name}({args}) dt={elapsed:0.3f}s')(time.sleep)(.2)
sleep(0.2) dt=0.201s
"""

# BEGIN CLOCKDECO_CLS
import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

class clock:

    def __init__(self, fmt=DEFAULT_FMT):
        self.fmt = fmt

    def __call__(self, func):
        def clocked(*_args):
            t0 = time.time()
            _result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(self.fmt.format(**locals()))
            return _result
        return clocked

if __name__ == '__main__':

    @clock()
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(.123)

# END CLOCKDECO_CLS
