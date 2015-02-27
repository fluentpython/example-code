from keyword import kwlist
from itertools import combinations

for combo in combinations(kwlist, 2):
	print(*combo)
