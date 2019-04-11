# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 19:29
# @Author   : tangky
# @Site     : 
# @File     : groupby_test.py
# @Software : PyCharm


import itertools

# print(list(itertools.groupby('LLLLAAGGG'))) # 产出(key, group_generator)这种形式的元组
# for char, group in itertools.groupby('LLLLAAAGG'):
#     print(char, '->', list(group))
# 处理groupby函数返回的生成器要嵌套迭代:这里在外层使用for循环,内层使用列表推导
animals = ['duck', 'eagle', 'rat', 'giraffe', 'bear', 'bat', 'dolphin', 'shark', 'lion']
animals.sort(key=len)
# print(animals)
# for length, group in itertools.groupby(animals, len):
#     print(length, '->', list(group))
# for length, group in itertools.groupby(reversed(animals), len):
#     print(length, '->', list(group))