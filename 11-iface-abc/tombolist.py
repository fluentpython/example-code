from random import randrange

from tombola import Tombola

@Tombola.register  # <1>
class TomboList(list):  # <2>

    def pick(self):
        if self:  # <3>
            position = randrange(len(self))
            return self.pop(position)  # <4>
        else:
            raise LookupError('pop from empty TomboList')

    def load(self, iterable): self.extend(iterable)  # <5>

    def loaded(self): return bool(self)  # <6>

# Tombola.register(TomboList)  # <- Python 3.2 or earlier
