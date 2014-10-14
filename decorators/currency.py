# currency.py

"""
>>> convert(1, 'BRL', 'USD')
0.4591
>>> convert(1, 'USD', 'BRL')
2.1784
>>> convert(1, 'EUR', 'USD')
1.3482
>>> convert(1, 'USD', 'EUR')
0.7417
>>> convert(1, 'EUR', 'BRL')
2.9369
>>> convert(1, 'BRL', 'EUR')
0.3405

>>> from functools import partial
>>> eur = partial(convert, cur_to='EUR')
>>> eur(1, 'USD')
0.7417
>>> eur(1, 'BRL')
0.3405
>>> eur2brl = partial(convert, cur_from='EUR', cur_to='BRL')
>>> eur2brl(100)
293.6864
>>> type(eur2brl)
<class 'functools.partial'>
"""

DEMO = """
>>> eur2brl.func
<function convert at 0x1010c5560>
>>> eur2brl.args, eur2brl.keywords
((), {'cur_from': 'EUR', 'cur_to': 'BRL'})
"""

rates = {'BRL': 2.17836,
         'CAD': 1.03615,
         'CNY': 6.10562,
         'EUR': 0.74173,
         'GBP': 0.62814,
         'INR': 61.8685,
         'JPY': 98.6002,
         'USD': 1.0}

reference = rates['USD']

def convert(amount, cur_from, cur_to):
    ref_amount = reference / rates[cur_from] * amount
    return round(ref_amount * rates[cur_to], 4)
