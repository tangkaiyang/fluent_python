# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 20:07
# @Author   : tangky
# @Site     : 
# @File     : iter_test.py
# @Software : PyCharm

from random import randint

def d6():
    return randint(1, 6)

d6_iter = iter(d6, 1)
print(d6_iter)
for roll in d6_iter:
    print(roll)