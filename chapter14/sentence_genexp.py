# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/11 14:03
# @Author   : tangky
# @Site     : 
# @File     : sentence_genexp.py
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
        return (match.group() for match in RE_WORD.finditer(self.text))