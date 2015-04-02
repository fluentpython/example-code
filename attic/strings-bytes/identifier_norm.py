
café = 1
café = 2
names = {(name, tuple(name)):value
         for name, value in globals().items()
         if not name.startswith('__')}
print(names)
