# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 16:56
# @Author   : tangky
# @Site     : 
# @File     : prod_gen_test.py
# @Software : PyCharm

# 示例14-18 演示itertools.product生成器函数
import itertools

# print(list(itertools.product('ABC', range(2))))
suits = 'spades hearts diamonds clubs'.split()
# print(suits)
# print(list(itertools.product('AK', suits)))
# print(list(itertools.product('ABC')))
# print(list(itertools.product('ABC', repeat=2))) # repeat=N关键字告诉product函数重复N次处理输入的各个可迭代对象
# print(list(itertools.product(range(2), repeat=3)))
rows = itertools.product('AB', range(2), repeat=2)
for row in rows:print(row)