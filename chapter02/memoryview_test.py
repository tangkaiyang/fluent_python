# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/3/31 10:24
# @Author   : tangky
# @Site     : 
# @File     : memoryview_test.py
# @Software : PyCharm

"""
利用memoryview精准地修改了一个数组的某个字节,这个数组的元素是16位二进制整数
"""
import array
numbers = array.array('h', [-2, -1, 0, 1, 2])
# 利用含有5个短整型有符号整数的数组(类型码是'h')创建一个memoryview
memv = memoryview(numbers)
print(len(memv))
# memv里的5个元素跟数组里的没有区别
print(memv[0])
# 创建memv_oct,把memv里的内容转换成'B'类型,也就是无符号字符
memv_oct = memv.cast('B')
print(memv_oct.tolist())
memv_oct[5] = 4
print(numbers)