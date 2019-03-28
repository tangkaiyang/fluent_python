# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/3/28 20:23
# @Author   : tangky
# @Site     : 
# @File     : my_vector.py
# @Software : PyCharm

"""
模拟数值类型:
利用特殊方法,可以让自定义对象通过+进行运算
Python内置的complex类可以用来表示二维向量
用到的特殊方法:__repr__, __abs__, __add__和__mul__
"""
# 一个简单的二维向量类
from math import hypot


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr(self):
        return 'Vecotr(%r, %r)' % (self.x, self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

"""
1.2.2字符串表示形式
内置函数repr,把一个对象用字符串的形式表达出来以便辨认,这就是"字符串表示形式"
repr通过__repr__得到一个对象的字符串表示形式.
如果没有实现__repr__,打印会得到<Vector object at ....>
交互式控制台和调试程序(debugger)用repr函数来获取字符串表示形式
%符号,返回结果用来代替%r所代表的的对象
str.format函数所用到的新式字符串格式化语法,也是利用了repr,把!r字段变成字符串
__repr__和__str__的区别在于,后者是在str()函数被使用,
或是在用print函数打印一个对象的时候才被调用的,并且他返回的字符串对终端用户更友好
如果一个对象没有__str__函数,Python需要调用它的时候,解释器会用__repr__作为代替
1.2.3算术运算符
通过__add__和__mul__带来了+和*两个算术运算符.
值的注意的是,这两个方法的返回值都是新创建的向量对象,
被操作的两个向量(self或other)还是原封不动,代码里只是读取了它们的值而已,
中缀运算符的基本元组就是不改变操作对象,而是产出一个新的值
1.2.4自定义的布尔值
尽管Python中有bool类型,但实际上任何对象都可用于需要布尔值的上下文中,
if或while,或者and,or和not运算符.
为了判定一个值x为真还是为假,Python会调用bool(x),这个函数只能返回True或False
默认情况下,我们自己定义的类的实例总被认为是真的,除非这个类对__bool__或
__len__函数有自己的实现.
bool(x)是调用x.__bool__()的结果,如果不存在__bool__,
那么会尝试调用__len__,如果为0返回False,否则返回True

"""