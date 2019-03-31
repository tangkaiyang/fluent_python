# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/3/31 10:36
# @Author   : tangky
# @Site     : 
# @File     : numpy_test.py
# @Software : PyCharm

# import numpy
# a = numpy.arange(12)
# print(a)
# print(type(a))
# print(a.shape)
# a.shape = 3, 4
# print(a)
# print(a[2])
# print(a[2, 1])
# print(a[:, 1])
# print(a.transpose())

# NumPy也可以对numpy.ndarray中的元素进行抽象的读取,保存和其他操作:
import numpy
floats = numpy.loadtxt('floats-10M-lines.txt')
print(floats[-3:])
floats *= .5
print(floats[-3:])
from time import perf_counter as pc
t0 = pc(); floats /= 3; pc() - t0   # 导入精度和性能都比较高的计时器
print(t0)
numpy.save('floats-10M', floats)
# 将上面的数据导入到另外一个数组里,这次load方法利用率一种叫做内存映射的机制,它让我们在内存不足的情况下仍然可以对数组做切片
floats2 = numpy.load('floats-10M.npy', 'r+')
floats2 *= 6
print(floats2[-3:])