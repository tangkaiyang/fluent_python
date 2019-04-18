# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/18 9:45
# @Author   : tangky
# @Site     : 
# @File     : model_v8.py
# @Software : PyCharm

from model_v5 import Validated, NonBlank, Quantity
import collections


# 示例21-16 EntityMeta元类用到了__prepare__方法,而且为Entity类定义了field_names类方法
class EntityMeta(type):
    """元类,用于创建带有验证字段的业务实体"""

    @classmethod
    def __prepare__(mcs, name, bases):
        return collections.OrderedDict()  # 1.返回一个空的OrderedDict实例,类属性将存储在里面

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        cls._field_names = []  # 2.在要构建的类中创建一个_field_names属性
        for key, attr in attr_dict.items():  # 3.这里的attr_dict是OrderedDict对象,由解释器在调用__init__方法之前调用__prepare__方法时获得.因此,这个for循环会按照添加属性的顺序迭代属性
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = '_{}#{}'.format(type_name, key)
                cls._field_names.append(key)  # 4.把找到的各个Validated字段添加到_field_names属性中


class Entity(metaclass=EntityMeta):
    """带有验证字段的业务实体"""

    @classmethod
    def field_names(cls):  # 5.field_names类方法的作用很简单:按照添加字段的顺序产出字段名称
        for name in cls._field_names:
            yield name


if __name__ == '__main__':
    # 示例21-17 展示field_names用法:无需修改LineItem类,field_names方法继承自model.Entity类
    from bulkfood_v7 import LineItem
    for name in LineItem.field_names():
        print(name)