# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 11:37
# @Author   : tangky
# @Site     : 
# @File     : sentence_gen.py
# @Software : PyCharm

import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:
            yield word
        return  # 生成器函数都不会抛出StopIteration异常,而是在生成完全部值之后会直接退出
