"""
Mappings of ISO-3166-1 alpha-2 country codes to names, to GEC
(Geopolitical Entities and Codes used by the US government)
and utility functions for flag download examples
"""

DATA_FILE = 'country-codes.tab'

# original source
CIA_URL = ('https://www.cia.gov/library/publications/'
            'the-world-factbook/graphics/flags/large/{gec}-lgflag.gif')

# local nginx web server
NGINX_URL = 'http://localhost:8080/ciaflags/{gec}.gif'

# Vaurien
VAURIEN_URL = 'http://localhost:8000/ciaflags/{gec}.gif'

SOURCE_URLS = {
    'CIA' : CIA_URL,
    'NGINX' : NGINX_URL,
    'VAURIEN' : VAURIEN_URL,
}

DEST_PATH_NAME = 'img/{cc}.gif'

cc2name = {}  # ISO-3166-1 to name
cc2gec = {}   # ISO-3166-1 to GEC

def _load():
    with open(DATA_FILE, encoding='utf-8') as cc_txt:
        for line in cc_txt:
            line = line.rstrip()
            if line.startswith('#'):
                continue
            iso_cc, gec, name = line.split('\t')
            cc2name[iso_cc] = name
            cc2gec[iso_cc] = gec


def flag_url(iso_cc, source='CIA'):
    base_url = SOURCE_URLS[source.upper()]
    return base_url.format(gec=cc2gec[iso_cc].lower())

def iso_file_name(iso_cc):
    return DEST_PATH_NAME.format(cc=iso_cc.lower())

def gec_file_name(iso_cc):
    return DEST_PATH_NAME.format(cc=cc2gec[iso_cc].lower())

_load()
