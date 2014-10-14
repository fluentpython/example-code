"""
Erik Meijer. 2014. The curse of the excluded middle.
Commun. ACM 57, 6 (June 2014), 50-55. DOI=10.1145/2605176
http://doi.acm.org/10.1145/2605176
"""

with open('citation.txt', encoding='ascii') as fp:
    get_contents = lambda: fp.read()

print(get_contents())
