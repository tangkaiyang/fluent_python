# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/17 9:57
# @Author   : tangky
# @Site     : 
# @File     : bulkfood_v4prop.py
# @Software : PyCharm

# 示例20-5 使用特性工厂函数实现与示例20-2中的描述符类相同的功能
def quantity():  # 1.没有storage_name参数
    try:
        quantity.counter += 1  # 2.不能依靠类属性在多次调用之间共享counter,因此把它定义为quantity函数自身的属性
    except AttributeError:
        quantity.counter = 0  # 3.如果quantity.counter属性未定义,把值设为0
    storage_name = '_{}:{}'.format('quantity',
                                   quantity.counter)  # 4.没有实例变量,因此创建一个局部变量storage_name,借助闭包保持它的值,供后面的qty_getter和qty_setter函数使用

    def qty_getter(instance):  # 5.这里可以使用内置的getattr和setattr函数,而不是处理instance.__dict__属性
        return getattr(instance, storage_name)

    def qty_setter(instance, value):
        if value > 0:
            setattr(instance, storage_name, value)
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)
