# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/17 10:20
# @Author   : tangky
# @Site     : 
# @File     : model_v5.py
# @Software : PyCharm

# 示例20-6 重构后的描述符类
import abc


class AutoStorage:  # 1.AutoStorage类提供了之前Quantity描述符的大部分功能
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)  # 2.验证除外


class Validated(abc.ABC, AutoStorage):  # 3.Validated是抽象类,不过也继承自AutoStorage类
    def __set__(self, instance, value):
        value = self.validate(instance, value)  # 4.__set__方法把验证操作委托给validate方法...
        super().__set__(instance, value)  # 5.然后把返回的value传给超类的__set__方法,存储值

    @abc.abstractmethod
    def validate(self, instance, value):  # 6.这个类中,validate是抽象方法
        """return validated value or raise ValueError"""


class Quantity(Validated):  # 7.Quantity和NonBlank都继承自Validated类
    """a number greater than zero"""

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    """a string with at least one non-space character"""

    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value  # 8.要求具体的validate方法返回验证后的值,借机可以清理,转换或规范化接受的数据.
