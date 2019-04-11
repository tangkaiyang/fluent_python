# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 16:13
# @Author   : tangky
# @Site     : 
# @File     : accu_test.py
# @Software : PyCharm

# 示例14-15 演示了itertools.accumulate生成器函数
# sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
# import itertools
#
# print(list(itertools.accumulate(sample)))
# print(list(itertools.accumulate(sample, min)))
# print(list(itertools.accumulate(sample, max)))
# import operator
# print(list(itertools.accumulate(sample, operator.mul)))
# print(list(itertools.accumulate(range(1, 11), operator.mul)))

# 示例14-16 演示用于映射的生成器函数
# print(list(enumerate('albatroz', 1)))
import operator

# print(list(map(operator.mul, range(11), range(11))))
# print(list(map(lambda a, b: (a, b), range(11), [2, 4, 8])))
import itertools

# print(list(itertools.starmap(operator.mul, enumerate('albatroz', 1))))
sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
print(list(enumerate(itertools.accumulate(sample), 1)))
print(list(itertools.starmap(lambda a, b: b / a, enumerate(itertools.accumulate(sample), 1))))
