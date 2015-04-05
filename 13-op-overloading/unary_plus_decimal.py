"""
# BEGIN UNARY_PLUS_DECIMAL

>>> import decimal
>>> ctx = decimal.getcontext()  # <1>
>>> ctx.prec = 40  # <2>
>>> one_third = decimal.Decimal('1') / decimal.Decimal('3')  # <3>
>>> one_third  # <4>
Decimal('0.3333333333333333333333333333333333333333')
>>> one_third == +one_third  # <5>
True
>>> ctx.prec = 28  # <6>
>>> one_third == +one_third  # <7>
False
>>> +one_third  # <8>
Decimal('0.3333333333333333333333333333')

# END UNARY_PLUS_DECIMAL

"""

import decimal

if __name__ == '__main__':

    with decimal.localcontext() as ctx:
        ctx.prec = 40
        print('precision:', ctx.prec)
        one_third = decimal.Decimal('1') / decimal.Decimal('3')
        print('    one_third:', one_third)
        print('   +one_third:', +one_third)

    print('precision:', decimal.getcontext().prec)
    print('    one_third:', one_third)
    print('   +one_third:', +one_third)
