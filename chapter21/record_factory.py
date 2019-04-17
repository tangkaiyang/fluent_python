# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/17 19:28
# @Author   : tangky
# @Site     : 
# @File     : record_factory.py
# @Software : PyCharm

# 一个简单的类工厂函数


def record_factory(cls_name, field_names):
    try:
        field_names = field_names.replace(',', ' ').split()
        # 1.这里体现了鸭子类型:尝试在逗号或空格处拆分field_names;如果失败,那么假定field_names本就是可迭代的对象,一个元素对应一个属性名
    except AttributeError:  # 不能调用.replace或.split方法
        pass  # 假定field_names本就是标识符组成的序列
    field_names = tuple(field_names)  # 2.使用属性名构建元组,这将成为新建类的__slots__属性

    def __init__(self, *args, **kwargs):  # 3.这个函数将成为新建类的__init__方法.参数有位置参数和(或)关键字参数
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self):  # 4.实现__iter__函数,把类的实例变成可迭代的对象;按照__slots__设定的顺序产出字段值
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):  # 5.迭代__slots__和self,生成友好的字符串表示形式
        values = ', '.join('{}={!r}'.format(*i) for i in zip(self.__slots__, self))
        return '{}({})'.format(self.__class__.__name__, values)

    cls_attrs = dict(__slots__=field_names,  # 6.组建类属性字典
                     __init__=__init__,
                     __iter__=__iter__,
                     __repr__=__repr__)
    return type(cls_name, (object,), cls_attrs)  # 7.调用type构造方法,构建新类,然后将其返回


if __name__ == '__main__':
    Dog = record_factory('Dog', 'name weight owner') # 1.这个工厂函数签名于namedtuple类似
    rex = Dog('Rex', 30, 'Bob')
    print(rex) # 友好的字符串表示形式
    name, weight, owner = rex # 3.实例是可迭代的对象,因此赋值时可以便利地拆包
    print(name, weight)
    print("{2}'s dog weighs {1}kg".format(*rex)) # 4.传给format等函数时也可以拆包
    rex.weight = 32 # 5.记录实例是可变的对象
    print(rex)
    print(Dog.__mro__) # 新建的类继承自object,与我们的函数工厂没有关系
