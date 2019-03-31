# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/3/31 9:28
# @Author   : tangky
# @Site     : 
# @File     : insort_test.py
# @Software : PyCharm

# insort可以保持有序序列的顺序
import bisect
import random

SIZE = 7
random.seed(1729)
print(random.random())
random.seed(1729)   # 生成同一个随机数
print(random.random())

my_list = []
for i in range(SIZE):
    new_item = random.randrange(SIZE*2)   # randrange(start, stop, step)
    bisect.insort(my_list, new_item)
    print('%2d ->' % new_item, my_list)