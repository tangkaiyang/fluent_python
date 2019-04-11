# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 20:54
# @Author   : tangky
# @Site     : 
# @File     : lookingglass_test.py
# @Software : PyCharm

# 示例15-2 测试LookingGlass上下文管理器类
from mirror import LookingGlass

with LookingGlass() as what:
    print('Alice, Kitty and Snowdrop')
    print(what)

print(what)
print('Back to normal.')