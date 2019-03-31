# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/3/31 9:54
# @Author   : tangky
# @Site     : 
# @File     : array_test.py.py
# @Software : PyCharm

# 实例2-20:展示了从一个有1000万个随机浮点数的数组开始,
# 到如何把这个数组存放到文件里,再到如何从文件读取这个数组

from array import array
from random import random

floats = array('d', (random() for i in range(10 ** 7)))
# floats = array('d', (random() for i in range(10)))
# print(floats)
# floats.byteswap()
# print(floats)
print(floats[-1])
fp = open('floats.bin', 'wb')
floats.tofile(fp)
fp.close()
floats2 = array('d')    # 双精度浮点数组(类型码是'd')
fp = open('floats.bin', 'rb')
floats2.fromfile(fp, 10 ** 7)   # 读取1000万个浮点数从二进制文件里
fp.close()
print(floats2[-1])
print(floats2 == floats)
