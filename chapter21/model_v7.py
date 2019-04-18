# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/18 7:57
# @Author   : tangky
# @Site     : 
# @File     : model_v7.py
# @Software : PyCharm
# 示例21-15 Entity Meta元类以及它的一个实例Entity
from model_v5 import Validated, NonBlank, Quantity


class EntityMeta(type):
    """元类,用于创建带有验证字段的业务实体"""

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)  # 1.在超类(这里是type)上调用__init__方法
        for key, attr in attr_dict.items():  # 2.与示例21-4中的@entity装饰器的逻辑一样
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = '_{}#{}'.format(type_name, key)


class Entity(metaclass=EntityMeta):  # 3.这个类的存在是为了用起来便利:这个模块的用户直接继承Entity类即可,无需关心EntityMeta元类,甚至不用知道它的存在
    """带有验证字段的业务实体"""
