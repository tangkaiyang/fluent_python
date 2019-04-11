# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 15:06
# @Author   : tangky
# @Site     : 
# @File     : aritprog_test.py
# @Software : PyCharm

# from Arithmetic import ArithmeticProgression


# 示例14-12 aritprog_gen生成器函数
def ArithmeticProgression(begin, step, end=None):
    result = type(begin + step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index


ap = ArithmeticProgression(0, 1, 3)
print(list(ap))
ap = ArithmeticProgression(0, .5, 3)
print(list(ap))
ap = ArithmeticProgression(0, 1 / 3, 1)
print(list(ap))
from fractions import Fraction

ap = ArithmeticProgression(0, Fraction(1, 3), 1)
print(list(ap))
from decimal import Decimal

ap = ArithmeticProgression(0, Decimal('.1'), .3)
print(list(ap))
