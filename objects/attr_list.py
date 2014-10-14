import sys

from collections import Counter

def fn():
    pass

class Class():
    pass

# int, str,
sample_types = [object, list, Class, type(Class), type(fn)]
if '-' in sys.argv:
    del sample_types[0]  # exlude `object`
sample_objs = [type_() for type_ in sample_types[:-2]] + [Class, fn]
sample_oids = [id(obj) for obj in sample_objs]

fmt = '{attr:17}' + '|{:8}' * len(sample_types)

headings = [t.__name__ for t in sample_types]
headings[headings.index('Class')] = 'instance'
headings[headings.index('type')] = 'class'

common_attrs = set()
for obj in sample_objs:
    for attr_name in dir(obj):
        common_attrs.add(attr_name)

print(fmt.format(*headings, attr=''))

counter = Counter()
for attr_name in sorted(common_attrs):
    if not attr_name.startswith('__'):
        continue
    flags = []
    found = 0
    for obj in sample_objs:
        try:
            attr = getattr(obj, attr_name)
            if type(attr) == type:
                flag = 'type'
            elif callable(attr):
                flag = 'method'
            else:
                flag = 'data'
            counter[id(obj)] += 1
            found += 1
        except AttributeError:
            flag = ''
        flags.append(flag)
    if '-' in sys.argv:
        include = found < len(sample_objs)
    else:
        include = found == len(sample_objs)
    if include:
        print(fmt.format(*flags, attr=attr_name))

counts = [counter[oid] for oid in sample_oids]
print(fmt.format(*counts, attr='TOTALS'))

print(sys.argv)
