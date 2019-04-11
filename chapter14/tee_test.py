# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 19:39
# @Author   : tangky
# @Site     : 
# @File     : tee_test.py
# @Software : PyCharm

from itertools import tee

# print(list(tee('ABC')))
g1, g2 = tee('ABC')
# print(g1, g2)
# print(next(g1))
# print(next(g2))
# print(next(g1))
# print(list(g1))
# print(list(g2))
print(list(zip(*tee('ABC'))))