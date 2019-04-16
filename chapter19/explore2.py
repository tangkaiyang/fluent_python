# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/16 14:06
# @Author   : tangky
# @Site     : 
# @File     : explore2.py
# @Software : PyCharm

# 示例19-7 使用__new__方法取代build方法,构建可能是也可能不是FrozenJSON实例的新对象
from collections import abc
from keyword import iskeyword


class FrozenJSON:
    """一个制度接口,使用属性表示访问JSON类对象"""

    def __new__(cls, arg):  # 1.__new__是类方法,第一个参数是类本身,余下的参数与__init__方法一样,只不过没有self
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)  # 2.默认的行为是委托给超类的__new__方法.这里调用的是object基类的__new__方法,把唯一的参数设为FrozenJSON
        elif isinstance(arg, abc.MutableSequence):  # 3.__new__方法中余下的代码与原先的build方法完全一样
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON(self.__data[name])# 4.之前,这里调用的是FrozenJSON.build方法,现在只需要调用FrozenJSON构造方法
