
src = """
café = 1
cafe\u0301 = 2
names = {(name, tuple(name)):value
         for name, value in globals().items()
         if not name.startswith('__')}
print(names)
"""

with open('identifier_norm.py', 'tw', encoding='utf8') as out:
    out.write(src)
