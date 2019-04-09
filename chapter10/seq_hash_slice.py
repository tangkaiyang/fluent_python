# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/9 14:41
# @Author   : tangky
# @Site     : 
# @File     : seq_hash_slice.py
# @Software : PyCharm

"""
第10章 序列的修改,散列和切片
Vector类
基本的序列协议--__len__和__getitem__
正确表述拥有很多元素的实例
适当的切片支持,用于生成新的Vector实例
综合各个元素的值计算散列值
自定义的格式语言扩展
通过__getattr__方法实现属性的动态存取,以及只读特性
把协议当做正式接口

10.1 Vector类:用户定义的序列类型
使用组合模式实现Vector类,而不使用继承
向量的分量存储在浮点数数组中,而且还将实现不可变扁平序列所需的方法
10.2 Vector类第1版:与Vector2d类兼容
为了编写Vector(3, 4)和Vector(3, 4, 5)这样的代码,我们可以让__init__方法接受任意个参数(通过*args);
但是,序列类型的构造方法最好接受可迭代的对象为参数,因为所有的内置的序列类型都是这样做的.
如果Vector实例的分量超过6个,repr()生成的字符串就会使用...省略一部分,
包含大量元素的集合类型一定要这么做,因为字符串表示形式是用于调试的(因此不想让大型对象在控制台或日志中输出几千行内容)
使用reprlib模块可以生成长度有限的表示形式
调用repr()函数的目的是调试,因此决不能抛出异常.
如果__repr__方法的实现有问题,那么必须处理,尽量输出有用的内容,让用户能够识别目标对象

10.3 协议和鸭子类型
在Python中创建功能完善的序列类型无需使用继承,只需实现符合序列协议的方法
在面向对象编程中,协议是非正式的接口,只在文档中定义,在代码中不定义.
"""
# 示例10-3
# import collections
#
# Card = collections.namedtuple('Card', ['rank', 'suit'])
#
#
# class FrenchDeck:
#     ranks = [str(n) for n in range(2, 11)] + list('JQKA')
#     suits = 'spades diamonds clubs hearts'.split()
#
#     def __init__(self):
#         self._cards = [Card(rank, suit) for suit in self.suits
#                        for rank in self.ranks]
#
#     def __len__(self):
#         return len(self._cards)
#
#     def __getitem__(self, position):
#         return self._cards[position]
"""
10.4 Vector类第二版:可切片的序列
实现__len__和__getitem__方法
需要切片得到的也是Vector实例,而不是数组
10.4.1 切片原理
"""
# 示例10-4 了解__getitem__和切片的行为
# class MySeq:
#     def __getitem__(self, index):
#         return index
#
# s = MySeq()
# print(s[1])
# # 1
# print(s[1:4])
# # slice(1, 4, None)
# print(s[1:4:2])
# # slice(1, 4, 2)
# print(s[1:4:2, 9])
# # (slice(1, 4, 2), 9)
# print(s[1:4:2, 7:9])
# # (slice(1, 4, 2), slice(7, 9, None))
"""
如果[]中有逗号,那么__getitem__收到的是元祖,元组甚至可以有多个切片对象
dir(slice)
slice是内置的类型
有start,stop和step数据属性,以及indices方法
help(slice.indices) -->
S.indices(len) -> (start, stop, stride)
给定长度为len的序列,计算S表示的扩展切片的起始(start)和结尾(stop)索引,
以及步幅(stride).超出边界的索引会被截掉,与常规切片的处理方式一样
indices方法开放了内置序列实现的棘手逻辑,用于优雅地处理缺失索引和负数索引,以及
长度超过目标序列的切片
slice(None, 10, 2).indices(5) --> (0, 5, 2)
slice(-3, None, None).indices(5) --> (2, 5, 1)
在Vector类中无需使用slice.indices()方法,因为受到切片参数,我们委托给_components数组处理
当没有底层序列类型作为依靠,可以使用这个方法
10.4.2 能处理切片的__getitem__方法
大量使用isinstance可能表明面向对象设计得不好,不过在__getitem__方法中使用它处理切片是合理的
numbers.Integral,这是一个抽象基类(Abstract Base Class,ABC).
在isinstance中使用抽象基类做测试能让API更灵活更容易更新
"""
# 示例10-7 测试改进的Vector.__getitem__方法
# from vector_v1 import Vector
# v7 = Vector(range(7))
# print(v7[-1])
# print(v7[1:4])
# print(v7[-1:])
# print(v7[1, 2]) # Vector不支持多维索引,因此索引元组或多个切片会抛出错误
"""
10.5 Vector类第3版:动态存取属性
通过单个字母访问前几个分量:用x,y和z代替v[0],v[1],v[2]
使用@property装饰器把x和y标记为只读特性,很麻烦
__getattr__提供了更好的方法
属性查找失败后,解释器会调用__getattr__方法.
属性查找失败后,解释器会调用__getattr__方法.
简单来说,对my_obj.x表达式,Python会检查my_obj实例有没有名为x的属性;
如果没有,到类(my_obj.__class__)中查找;
如果还没有,顺着继承树继续查找,
如果依旧找不到,调用my_obj所属类中定义的__getattr__方法,传入self和属性名称的字符串形式(如'x')
"""
# 示例10-9 不恰当的行为:为v.x赋值没有抛出错误,但是前后有矛盾
# from vector_v1 import Vector
# v = Vector(range(5))
# print(v)
# print(v.x)
# v.x = 10 # 此时为v赋予了新的属性x,调用v.x便不会调用__getattr__方法
# print(v.x)
# print(v)
# print(v.__dict__)
"""
为此需要实现__setattr__方法
super.__setattr__(name, value)
在超类上调用__setattr__方法,提供标准行为
super()函数用于动态访问超类的方法,对Python这样支持多重继承的动态语言来说,必须能这么做.
把子类方法的某些任务委托给超类中适当的方法
注意,我们没有禁止为全部属性赋值,只是禁止为单个小写字母属性赋值,以防与只读属性x,y,z和t混淆
在类中声明__slots__属性可以防止设置新实例属性;
因此,你可能想使用这个功能,而不想这里所实现的,实现__setattr__方法.
可是,不建议只为了避免创建实例属性而使用__slots__属性.
__slots__属性只应该用于节省内存,而且仅当内存严重不足时才应该这么做
多数时候,如果实现了__getattr__方法,那么也要定义__setattr__方法,以防对象的行为不一致

10.6 Vector类第4版:散列和快速等值测试
实现__hash__方法,加上现有的__eq__方法
reduce,计算向量所有分量的散列值非常适合使用这个函数
归约函数(reduce,sum,any,all)把序列或有限的可迭代对象变成一个聚合结果
"""
# 示例10-11 计算整数0~5的累计抑或的三种方式
# n = 0
# for i in range(1, 6):
#     n ^= i
# print(n)
# import functools
#
# print(functools.reduce(lambda a, b: a ^ b, range(6)))
# import operator
#
# print(functools.reduce(operator.xor, range(6)))
"""
使用reduce函数最好提供第三个参数,reduce(function, iterable, initializer),
这样能避免异常:TypeError: reduce() of empty sequence with no initial value
如果序列为空,initializer是返回的结果;否则,在归约中使用它作为第一参数,因此应该使用
恒等值.比如对+,|和^来说,initializer应该是0;而对*和&来说,应是1

映射归约:把函数应用到各个元素上,生成一个新序列(映射,map),然后计算聚合值(归约,reduce)
映射过程计算各个分量的散列值,归约过程则使用xor运算符聚合所有散列值.
在Python2中使用map函数效率低些,因为map函数要使用结果构建一个列表.
但是在Python3中,map函数是惰性的,它会创建一个生成器,按需产出结果,因此能节省内存
zip函数生成一个由元组构成的生成器,元组中的元素来自参数传入的各个可迭代对象.
用于计算聚合值的整个for循环可以替换成一行all函数调用:如果所有分量对的比较结果都是True,
那么结果就是True.只要有一次的结果是False,all函数就返回False

出色的zip函数
使用for循环迭代元素不用处理索引变量,还能避免很多缺陷,但是需要一些特殊的使用函数协助.
其中一个是内置的zip函数.
使用zip函数能轻松地并行迭代两个或更多可迭代对象,他返回的元组可以拆包成变量,分别
对应各个并行输入中的一个元素
zip函数的名字取自拉链系结物(zipper fastener)
zip函数与文件压缩没有关系
"""
# 示例10-15 zip内置函数的使用示例
# print(zip(range(3), 'ABC'))
# print(list(zip(range(3), 'ABC')))
# print(list(zip(range(3), 'ABC', [0.0, 1.1, 2.2, 3.3])))
# from itertools import zip_longest
#
# print(list(zip_longest(range(3), 'ABC', [0.0, 1.1, 2.2, 3.3], fillvalue=-1)))
"""
zip函数返回一个生成器,按需生成元组
zip:当有一个可迭代对象耗尽后,它不发出警告就停止
itertools.zip_longest函数的行为有所不同:使用可选的fillvalue(默认值为None)
填充缺失的值,因此可以继续产出,直到最长的可迭代对象耗尽
为了避免在for循环中手动处理索引变量,还经常使用内置的enumerate生成器函数

10.7 Vector类第5版:格式化
Vector类的__format__方法与Vector2d类的相似,但是不是使用
极坐标,而是使用球面坐标(也叫超球面坐标),因此Vector类支持n个维度,
而超过四维后,球体变成了超球体.
因此,我们会把自定义的格式后缀由'p'变成'h'
超球面坐标(hyperspherical coordinate)'h'是个不错的选择

10.8 本章小结
Vector的行为之所以想序列,是因为它实现了__getitem__和__len__方法;
这是鸭子类型语言使用的非正式接口

"""