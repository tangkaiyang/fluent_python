# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 19:06
# @Author   : tangky
# @Site     : 
# @File     : count_repeat_cycle.py
# @Software : PyCharm


# 示例14-19 演示count,repeat和cycle的用法
import itertools
import operator

ct = itertools.count()
# print(next(ct))
# print(next(ct), next(ct), next(ct))
# print(list(itertools.islice(itertools.count(1, .3), 3))) # 不能使用ct构建列表,因为ct是无穷的
# cy = itertools.cycle('ABC')
# print(next(cy))
# print(list(itertools.islice(cy, 7))) # 如果使用islice或takewhile函数做了限制,可以从count生成器中构建列表
# rp = itertools.repeat(7)
# print(next(rp), next(rp))
# print(list(itertools.repeat(8, 4)))
print(list(map(operator.mul, range(11), itertools.repeat(5)))) # repeat函数的常见用途:为map函数提供固定参数,这里提供的是乘数5