"""
Build flags fixture
"""

import shutil
import os
import json

SRC = 'img/'
DEST = 'fixture/'
CONTINENTS = dict(AF='Africa',
                  AS='Asia',
                  EU='Europe',
                  NA='North America',
                  SA='South America',
                  OC='Oceania')

with open('countries-continents.tab') as cc_fp:
    for line in cc_fp:
        if line.startswith('#'):
            continue
        iso_cc, gec_cc, cont, name = line.strip().split('\t')
        print(iso_cc, name)
        cc = iso_cc.lower()
        img_name = cc + '.gif'
        from_file = os.path.join(SRC, img_name)
        to_path = os.path.join(DEST, cc)
        os.mkdir(to_path)
        to_file = os.path.join(to_path, img_name)
        shutil.copyfile(from_file, to_file)
        tld_cc = 'uk' if cc == 'gb' else cc
        metadata = {'country': name, 'continent':CONTINENTS[cont],
            'iso_cc': iso_cc, 'tld_cc': '.'+tld_cc, 'gec_cc': gec_cc}

        with open(os.path.join(to_path, 'metadata.json'), 'wt') as json_fp:
            json.dump(metadata, json_fp, ensure_ascii=True)
