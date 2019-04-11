# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 9:26
# @Author   : tangky
# @Site     : 
# @File     : 14-2.py
# @Software : PyCharm

from sentence import Sentence
# s = Sentence('"The time has come," the Walrus said.')
# print(s)
# for word in s:
#     print(word)
# print(list(s))

s3 = Sentence('Pig and Pepper')
it = iter(s3)
print(it)
print(next(it))
print(next(it))
print(list(it))
# print(next(it))
# try:
#     print(next(it))
# except StopIteration:
#     print(StopIteration.__dict__)
print(list(it))
print(list(iter(s3)))