# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/15 20:53
# @Author   : tangky
# @Site     : 
# @File     : osconfeed.py
# @Software : PyCharm

# 示例19-2 下载osconfeed.json

from urllib.request import urlopen
import warnings
import os
import json

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = './osconfeed.json'


def load():
    if not os.path.exists(JSON):
        msg = 'downloading {} to {}'.format(URL, JSON)
        warnings.warn(msg)  # 1.如果需要下载,就发出提醒
        with urlopen(URL) as remote, open(JSON, 'wb') as local:  # 2.在with语句中使用两个上下文管理器,分别用于读取和保存远程文件
            local.write(remote.read())

    with open(JSON) as fp:
        return json.load(fp)  # 3.json.load函数解析JSON文件,返回Python原生对象.


# 示例19-3 doctest
feed = load()  # 1.feed的值是一个字典,里面嵌套着字典和列表,存储着字符串和整数
print(sorted(feed['Schedule'].keys()))  # 2.
for key, value in sorted(feed['Schedule'].items()):
    print('{:3} {}'.format(len(value), key))  # 3.
print(feed['Schedule']['speakers'][-1]['name'])  # 4.
print(feed['Schedule']['speakers'][-1]['serial'])  # 5.
print(feed['Schedule']['events'][0]['name'])
print(feed['Schedule']['events'][0]['speakers'])  # 6.
