# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/12 8:00
# @Author   : tangky
# @Site     : 
# @File     : mirror_gen.py
# @Software : PyCharm

# 示例15-5 mirror_gen.py:使用生成器实现的上下文管理器
import contextlib

@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text): # 在闭包中访问original_write
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    yield 'JABBERWOCKY'
    sys.stdout.write = original_write