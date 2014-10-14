import random
import collections

SIZE = 15

random.seed(1729)

target_list = [random.randrange(SIZE*2) for i in range(SIZE)]
target_list.sort()

random.seed(1729)
display_list = ['    '] * SIZE
occurrences = collections.Counter()
for i in range(SIZE):
    new_item = random.randrange(SIZE*2)
    pos = target_list.index(new_item) + occurrences[new_item]
    occurrences[new_item] += 1
    display_list[pos] = '%2s, ' % new_item
    print('[' + ''.join(display_list) + ']')

