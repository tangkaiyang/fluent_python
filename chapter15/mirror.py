# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 20:57
# @Author   : tangky
# @Site     : 
# @File     : mirror.py.py
# @Software : PyCharm

# 示例15-3 mirror.py: LookingGlass上下文管理器类的代码

class LookingGlass:
    def __enter__(self):
        import sys
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'JABBERWOCKY'
    def reverse_write(self, text):
        self.original_write(text[::-1])
    def __exit__(self, exc_type, exc_value, traceback):
        import sys
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero!')
            return True