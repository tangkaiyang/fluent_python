# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 19:17
# @Author   : tangky
# @Site     : 
# @File     : comb_gen.py
# @Software : PyCharm

# 示例14-20 组合学生成器函数会从输入的各个元素中产出多个值
import itertools

# print(list(itertools.combinations('ABC', 2)))
# print(list(itertools.combinations_with_replacement('ABC', 2)))
# print(list(itertools.permutations('ABC', 2)))
print(list(itertools.product('ABC', repeat=2))) #'ABC'和'ABC'(repeat=2的效果)的笛卡尔积
