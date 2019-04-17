# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/17 13:38
# @Author   : tangky
# @Site     : 
# @File     : descriptor_sample.py
# @Software : PyCharm

# 描述符详解
class Desc(object):

    # def __get__(self, instance, owner):
    #     print("__get__...")
    #     print("self : \t\t", self)
    #     print("instance : \t", instance)
    #     print("owner : \t", owner)
    #     print('=' * 40, "\n")
    #
    # def __set__(self, instance, value):
    #     print("__set__...")
    #     print("self : \t\t", self)
    #     print("instance : \t", value)
    #     print('=' * 40, "\n")

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        print("__get__...")
        print("name = ", self.name)
        print('=' * 40, "\n")


# class TestDesc():
#     x = Desc()
class TestDesc(object):
    x = Desc('x')

    def __init__(self):
        self.y = Desc('y')

# t = TestDesc()
# t.x
# print(t)
t = TestDesc()
print(t.__dict__)
print(t.x)
print(t.y) # Desc()实现了描述符协议,Desc()是描述符,t.y因此会转换为TestDesc.__dict__['y'].__get__(t, TestDesc),而y不是类属性,所以忽略
# 当Python解释器发现实例对象的字典中,有与描述符同名的属性时,描述符优先,会覆盖掉实例属性
# 当描述符只设置__get__方法(没有设置__set__方法,)为非数据描述符,优先级低于实例属性
"""
属性查询优先级
1.__getattribute__(),无条件调用
2.数据描述符:由1.触发调用(若人为的重载了该__getattribute__()方法,可能会导致无法调用描述符)
3.实例对象的字典(若与描述符对象同名,会被覆盖)
4.类的字典
5.非数据描述符
6.父类的字典
7.__getattr__()方法
"""