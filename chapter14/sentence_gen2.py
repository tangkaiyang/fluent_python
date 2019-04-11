# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 13:38
# @Author   : tangky
# @Site     : 
# @File     : sentence_gen2.py.py
# @Software : PyCharm


import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):  # finditer函数构建一个迭代器,包含self.text中匹配RE_WORD的单词,产出MatchObject实例
            yield match.group()  # match.group()方法从MatchObject实例中提取匹配正则表达式的具体文本
