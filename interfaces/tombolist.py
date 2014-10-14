from random import randrange

from tombola import Tombola


class TomboList(list):  # <1>

    def pop(self):
        if self:  # <2>
            return super().pop(randrange(len(self)))  # <3>
        else:
            raise LookupError('pop from empty TomboList')

    def load(self, iterable): self.extend(iterable)  # <4>

    def loaded(self): return bool(self)  # <5>


Tombola.register(TomboList)  # <6>
