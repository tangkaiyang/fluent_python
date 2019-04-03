# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/3 7:24
# @Author   : tangky
# @Site     : 
# @File     : clip.py
# @Software : PyCharm
def clip(text, max_len=80):
    """
    在max_len前面或后面的第一个空格处截断文本
    """
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:
        end = len(text)
    return text[:end].rstrip()