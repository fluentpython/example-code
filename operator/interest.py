"""
Compound interest function with ``decimal.Decimal``

"""

def compound_interest(principal, rate, periods):
    return principal * ((1 + rate) ** periods - 1)

def test(verbose=False):
    from decimal import Decimal, getcontext
    getcontext().prec = 8
    fixture = [(1000, Decimal('0.05'), 1, Decimal('50')),
               (1000, Decimal('0.10'), 5, Decimal('610.51')),
               (1000, Decimal('0.10'), 15, Decimal('3177.2482')),
               (1000, Decimal('0.06'), 5, Decimal('338.2256')),
              ]
    for principal, rate, periods, future_value in fixture:
        computed = compound_interest(principal, rate, periods)
        if verbose:
            print('{!r}, {!r}, {!r} -> {!r}'.format(
                  principal, rate, periods, computed))
        assert future_value == computed, '{!r} != {!r}'.format(future_value, computed)

if __name__ == '__main__':
    test(True)
