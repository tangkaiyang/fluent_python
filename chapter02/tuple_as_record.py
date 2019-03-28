# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/3/29 6:48
# @Author   : tangky
# @Site     : 
# @File     : tuple_as_record.py
# @Software : PyCharm

# lax_coordinates = (33.9425, -118.408056)
# city, year, pop, chg, area = ('Tokyo', 2003, 32450, 0.66, 8014)
# traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'), ('ESP', 'XDA205856')]
# for passport in sorted(traveler_ids):
#     print('%s/%s' % passport)
# for country, _ in traveler_ids:
#     print(country)

# for循环可以分别提取元组里的元素,也叫做拆包(unpacking).
# 因为元组中的第二个元素对我们没有什么用,所以赋值个_占位符

# metro_areas = [
#     ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
#     ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
#     ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
#     ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
#     ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
# ]
# print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
# fmt = '{:15} | {:9.4f} | {:9.4f}'
# for name, cc, pop, (latitude, longitude) in metro_areas:
#     if longitude <= 0:
#         print(fmt.format(name, latitude, longitude))
# import collections
# Card = collections.namedtuple('Card', ['rank', 'suit'])
# print(Card.__dict__)

from collections import namedtuple
City = namedtuple('City', 'name country population coordinates')
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
print(tokyo)
print(tokyo.population)
print(tokyo.coordinates)
print(tokyo[1])
print(City._fields)
LatLong = namedtuple('LatLong', 'lat long')
delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
delhi = City._make(delhi_data)
print(delhi._asdict)
for key, value in delhi._asdict().items():
    print(key + ':', value)