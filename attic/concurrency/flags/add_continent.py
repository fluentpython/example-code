# Source for continent listings:
# United Nations Statistics Division
# http://unstats.un.org/unsd/cr/ctryreg/default.asp?Lg=1

CONTINENTS = dict(AF='Africa',
                  AS='Asia',
                  EU='Europe',
                  NA='North America',
                  SA='South America',
                  OC='Oceania')

COUNTRY_CONTINENT = {}

for cont_code, cont_name in CONTINENTS.items():
    cont_suffix = cont_name.lower().replace(' ', '_')
    with open('continent-' + cont_suffix + '.txt') as fp:
        for country in fp:
            COUNTRY_CONTINENT[country.strip()] = cont_code

with open('country-codes.tab') as fp:
    for lin in fp:
        if lin.startswith('#'):
            continue
        lin = lin.strip()
        cc, gec, name = lin.split('\t')
        cont = COUNTRY_CONTINENT.get(name, '??')
        print(cc, gec, cont, name, sep='\t')
