# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 14:56
# @Author   : tangky
# @Site     : 
# @File     : Arithmetic.py
# @Software : PyCharm
"""
ArithmeticProgression(begin, step[, end])
公差step必须指定,末项end可选.
数字的类型与begin或step的类型一致
"""
class ArithmeticProgression:

    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end  # None --> 无穷数列

    def __iter__(self):
        result = type(self.begin + self.step)(self.begin) # 把self.begin赋值给result,先强制转换成前面的加法算式得到的类型
        forever = self.end is None
        index = 0
        while forever or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step * index #未使用result += self.step*index以此降低处理浮点数时累积效应致错的风险

