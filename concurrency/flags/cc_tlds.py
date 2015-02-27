"""
Check country code TLDs
"""

import shutil
import os
import json

iso_cc_db = {}

with open('country-codes.tab') as cc_fp:
    for line in cc_fp:
        if line.startswith('#'):
            continue
        iso_cc, gec_cc, name = line.strip().split('\t')
        iso_cc_db[iso_cc.lower()] = name

tld_cc_db = {}

with open('tlds.tab') as cc_fp:
    for line in cc_fp:
        if line.startswith('#'):
            continue
        tld_cc, category, entity = line.strip().split('\t')
        if category.strip() != 'country-code':
            continue
        if ascii(tld_cc) != repr(tld_cc):
            continue
        tld_cc_db[tld_cc[1:].strip()] = entity

not_tld = iso_cc_db.keys() - tld_cc_db.keys()
print(sorted(not_tld))

for iso_cc, name in sorted(iso_cc_db.items()):
    entity = tld_cc_db[iso_cc]
    print('{}\t{}\t{}'.format(iso_cc, name, entity))
