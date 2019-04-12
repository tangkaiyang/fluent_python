# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/12 9:57
# @Author   : tangky
# @Site     : 
# @File     : context_test.py
# @Software : PyCharm

# 示例15-8 用于原地重写文件的上下文管理器

# import csv
#
# with inplace(csvfilename, 'r', newline='') as (infh, outfh):
#     reader = csv.reader(infh)
#     writer = csv.writer(outfh)
#
#     for row in reader:
#         row += ['new', 'columns']
#         writer.writerow(row)

"""
inplace函数是个上下文管理器,为同一个文件提供了两个句柄(infh和outfh),以便同时读写同一个文件.
比标准库中的fileinput.input函数(也提供了一个上下文管理器)易于使用
"""