"""
Erik Meijer. 2014. The curse of the excluded middle.
Commun. ACM 57, 6 (June 2014), 50-55. DOI=10.1145/2605176
http://doi.acm.org/10.1145/2605176
"""

def ha():
    ha = 'Ha'
    print(ha)
    return ha

# prints 'Ha' twice before showing result
print('result ->', ha() + ha())

# prints 'Ha' only once before showing reult
ha_res = ha()  # common subexpression elimination
print('result ->', ha_res + ha_res)
