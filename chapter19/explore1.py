# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/16 13:39
# @Author   : tangky
# @Site     : 
# @File     : explore1.py
# @Software : PyCharm

# 示例19-6 explore1.py:在名称为Python关键字的属性后面加上_
from collections import abc
import keyword


class FrozenJSON:

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):  # 1.keyword.iskeyword(...):先导入keyword模块
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj
