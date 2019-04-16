# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/16 7:35
# @Author   : tangky
# @Site     : 
# @File     : explore0.py
# @Software : PyCharm

# 示例19-5 explore0.py:把一个JSON数据集转换成一个嵌套这FrozenJSON对象,列表和简单类型的FrozenJSON对象
from collections import abc


class FrozenJSON:
    """一个只读接口,使用属性表示法访问JSON类对象"""

    def __init__(self, mapping):
        self.__data = dict(mapping)  # 1.使用mapping参数构建一个字典:确保传入的是字典(或者是能转换成字典的对象);安全起见,创建一个副本

    def __getattr__(self, name):  # 2.仅当没有指定名称(name)的属性时才调用__getattr__方法
        if hasattr(self.__data, name):
            return getattr(self.__data, name)  # 3.如果name是实例属性__data的属性,返回那个属性.调用keys等方法就是通过这种方式处理的
        else:
            return FrozenJSON.build(self.__data[name])  # 4.否则,从self.__data中获取name键对应的元素,返回调用FrozenJSON.build()方法得到的结果

    @classmethod
    def build(cls, obj):  # 5.这是一个备选构造方法,@classmethod装饰器经常这么用
        if isinstance(obj, abc.Mapping):  # 6.如果obj是映射,那就构建一个FrozenJSON对象
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):  # 7.如果是MutableSequence对象,必然是列表,因此,我们把偶不进中的每个元素递归地传给.build()方法,构建一个列表
            # 数据源是JSON格式,而在JSON中,只有字典和列表是集合类型
            return [cls.build(item) for item in obj]
        else:  # 8.如果既不是字典也不是列表,原封不动地返回元素
            return obj


# 示例19-4 FrozenJSON类能读取属性,如name,还能调用方法,如.keys()和.items()
from osconfeed import load

raw_feed = load()
feed = FrozenJSON(raw_feed)  # 1.传入嵌套的字典和列表组成的raw_feed,创建一个FrozenJSON示例
print(len(feed.Schedule.speakers))  # 2.FrozenJSON实例能使用属性表示法遍历嵌套的字典
print(sorted(feed.Schedule.keys()))  # 3.也可以使用底层字典的方法,例如.keys(),获取记录集合的名称
for key, value in sorted(feed.Schedule.items()):  # 4.使用items()方法获取各个记录集合及其内容,然后显示各个记录集合中元素的数量
    print('{:3} {}'.format(len(value), key))
print(feed.Schedule.speakers[-1].name)  # 5.列表,例如feed.Schedule.speakers,仍是列表;但是,如果里面的元素是映射,会转换成FrozenJSON对象
talk = feed.Schedule.events[0]
print(type(talk))  # 6.
print(talk.name)
print(talk.speakers)  # 7.
# print(talk.flavor) # 8.读取不存在的属性会抛出KeyError异常,而不是抛出通常的AttributeError异常
