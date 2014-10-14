FILENAME = 'metro_areas.txt'

class MetroArea:

    def __init__(self, name, country, pop, pop_change, area):
        self.name = name
        self.country = country
        self.pop = pop
        self.pop_change = pop_change
        self.area = area

    def __repr__(self):
        return '{0.name}, {0.country} ({0.pop})'.format(self)

    def density(self):
        return self.pop / self.area


def load():
    metro_areas = []
    with open(FILENAME, encoding='utf-8') as text:
        for line in text:
            if line.startswith('#'):
                continue
            # Country Name Rank Population Yr_change % Area(km2) Pop/km2
            country, name, _, pop, pop_change, _, area, _ = line.split('\t')
            pop = float(pop.replace(',', ''))
            pop_change = float(pop_change)
            area = float(area)
            metro_areas.append((name, country, pop, pop_change, area))
    return metro_areas


def list(metro_areas):
    print('{:^18} {:>6} {:>4} {:>6}'.format('name', 'cc', 'pop', 'chg', 'area'))
    for metro in metro_areas:
        print('{:18} {:2} {:6.0f} {:4.0f} {:6.0f}'.format(*metro))

def list_instances(metro_areas):
    metro_areas = [MetroArea(*fields) for fields in metro_areas]
    for metro in metro_areas:
        print(metro)


if __name__ == '__main__':
    #list(load())
    list_instances(load())


