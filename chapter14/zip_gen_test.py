# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 16:49
# @Author   : tangky
# @Site     : 
# @File     : zip_gen_test.py
# @Software : PyCharm


# 示例14-17 演示用于合并的生成器函数
import itertools

print(list(itertools.chain('ABC', range(2))))
print(list(itertools.chain(enumerate('ABC'))))
print(list(itertools.chain.from_iterable(enumerate('ABC')))) # chain.from_iterable函数从可迭代的对象中获取每个元素,然后按顺序把元素连接起来,前提是各个元素本身也是可迭代的对象
print(list(zip('ABC', range(5))))
print(list(zip('ABC', range(5), [10, 20, 30, 40])))
print(list(itertools.zip_longest('ABC', range(5))))
print(list(itertools.zip_longest('ABC', range(5), fillvalue='?')))
