>>> metro_data = [
...     ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
...     ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
...     ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
...     ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
...     ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
... ]
# BEGIN ATTRGETTER_DEMO

>>> from collections import namedtuple
>>> LatLong = namedtuple('LatLong', 'lat long')  # <1>
>>> Metropolis = namedtuple('Metropolis', 'name cc pop coord')  # <2>
>>> metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long_))  # <3>
...     for name, cc, pop, (lat, long_) in metro_data]
>>> metro_areas[0]
Metropolis(name='Tokyo', cc='JP', pop=36.933, coord=LatLong(lat=35.689722, long=139.691667))
>>> metro_areas[0].coord.lat  # <4>
35.689722
>>> from operator import attrgetter  
>>> name_lat = attrgetter('name', 'coord.lat')  # <5>
>>>
>>> for city in sorted(metro_areas, key=attrgetter('coord.lat')):  # <6>
...     print(name_lat(city))  # <7>
...
('Sao Paulo', -23.547778)
('Mexico City', 19.433333)
('Delhi NCR', 28.613889)
('Tokyo', 35.689722)
('New York-Newark', 40.808611)

# END ATTRGETTER_DEMO
