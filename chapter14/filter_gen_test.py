# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 15:56
# @Author   : tangky
# @Site     : 
# @File     : filter_gen_test.py
# @Software : PyCharm


# 实例14-14 演示用于过滤的生成器函数
def vowel(c):
    return c.lower() in 'aeiou'


print(list(filter(vowel, 'Aardvark')))
import itertools

print(list(itertools.filterfalse(vowel, 'Aardvark')))
print(list(itertools.dropwhile(vowel, 'Aardvark')))
print(list(itertools.takewhile(vowel, 'Aardvark')))
print(list(itertools.compress('Aardvark', (1, 0, 1, 1, 0, 1))))
print(list(itertools.islice('Aardvark', 4)))
print(list(itertools.islice('Aardvark', 4, 7)))
print(list(itertools.islice('Aardvark', 1, 7, 2)))