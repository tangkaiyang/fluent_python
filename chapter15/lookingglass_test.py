# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 20:54
# @Author   : tangky
# @Site     : 
# @File     : lookingglass_test.py
# @Software : PyCharm

# 示例15-2 测试LookingGlass上下文管理器类
from mirror import LookingGlass
# import sys

# with LookingGlass() as what:
#     print('Alice, Kitty and Snowdrop')
#     print(what)
#
# print(what)
# print('Back to normal.')
# 示例15-4 在with块之外使用LookingGlass类
# manager = LookingGlass()
# print(manager)
# monster = manager.__enter__()  # 在上下文管理器上调用__enter__()方法,把结果存储在monster中
# print(monster == 'JABBERWOCKY') # 打印出的True标识符是反向的,因为stdout的所有输出都经过__enter__方法中打补丁的write方法处理
# print(monster)
# print(manager)
# manager.__exit__(None, None, None)  #调用manager.__exit__,还原成之前的stdout.write
# print(monster)


# 示例15-6 测试looking_glass上下文管理器函数

from mirror_gen import looking_glass
with looking_glass() as what:
    print('Alice, Kitty and Snowdrop')
    print(what)

print(what)