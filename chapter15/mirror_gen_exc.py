# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/12 9:33
# @Author   : tangky
# @Site     : 
# @File     : mirror_gen_exc.py
# @Software : PyCharm

# 示例15-7 mirror_gen_exc.py:基于生成器的上下文管理器,而且实现了异常处理

import contextlib

@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])
    sys.stdout.write = reverse_write
    msg = ''
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write  # 撤销对sys.stdout.write方法所作的猴子补丁
        if msg:
            print(msg)