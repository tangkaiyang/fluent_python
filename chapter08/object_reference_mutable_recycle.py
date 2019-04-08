# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/8 19:25
# @Author   : tangky
# @Site     : 
# @File     : object_reference_mutable_recycle.py
# @Software : PyCharm
"""
第四部分 面向对象惯用法

第8章 对象引用,可变性和垃圾回收
对象与对象名称:名称不是对象,而是单独的东西
对象标识,值和别名;元组不可变,但是其中的值是可变的,浅复制和深复制;
引用和函数参数:可变的参数默认值导致的问题,安全地处理函数的调用者传入的可变参数;
垃圾回收,del命令,使用弱引用"记住"对象,而无需对象本身存在

8.1 变量不是盒子
Python的变量不是盒子而是便利贴
"""
# 示例 8-1 变量a和b引用同一列表,而不是那个表的副本
# a = [1, 2, 3]
# b = a
# a.append(4)
# print(b)
# 对引用式变量来说,说把变量分配给对象更合理,反过来说就有问题
# 对象在赋值之前就创建了
# 示例8-2 证明赋值语句的右边先执行
# 示例8-2 创建对象之后才把变量分配给对象
# class Gizmo:
#     def __init__(self):
#         print('Gizmo id: %d' % id(self))
# x = Gizmo()
# # y = Gizmo() * 10
# print(dir()) # 不会创建变量y,因为在对赋值语句的右边进行求值时抛出了异常
"""
8.2 标识,相等性和别名
is和==的区别
每个变量都有标识,类型和值.对象一旦创建,它的标识绝不会变;
你可以把标识理解为对象在内存中的地址.
is运算符比较两个对象的标识;
id()函数返回对象表示的整数表示
8.2.1 在==和is之间选择
==运算符比较两个对象的值(对象中保存的数据),而is比较对象的标识.
通常我们关注的是值而不是标识.
然而在变量和单例值之间比较时,应该使用is.
推荐的写法:
x is None
x is not None
is运算符比==速度快,因为它不能重载,
而a==b是语法糖,等同于a.__eq__(b).
继承自object的__eq__方法比较两个对象的ID,结果与is一样.
但多数内置类型使用更有意义的方式覆盖了__eq__方法,
会考虑对象属性的值.
8.2.2 元组的相对不可变性
元组与多数Python集合(列表,字典,集,等等)一样,保存的是对象的引用.
如果引用的元素是可变的,即使元组本身不可变,元素依然可变,
也就是说,元组的不可变性其实是指tuple数据结构的物理内容(即保存的引用)不可变,
与引用的对象无关
而str,bytes和array.array等单一类型序列是扁平的,他们保存的不是引用,
而是在连续内存中保存数据本身(字符,字节和数字)
元组的值会随着引用的变量的可变对象的变化而变.元组中不可变的是元素的标识
"""
# 示例8-5
# t1 = (1, 2, [30, 40])
# t2 = (1, 2, [30, 40])
# print(t1 == t2)
# print(id(t1[-1]))
# t1[-1].append(99)
# print(id(t1[-1]))
# print(t1 == t2)
"""
8.3 默认做浅复制
复制列表(或多数内置的可变集合)最简单的方式是使用内置的类型构造方法
l1 = [3, [55, 44], (7, 8, 9)]
l2 = list(l1) # list(l1)创建l1的副本
l2 --> [3, [55, 44], (7, 8, 9)]
l2 == l1 --> True # 副本与源列表相等
l2 is l1 --> False # 二者指代不同的对象.对列表和其他可变序列来说,
还能使用简洁的l2 = l1[:]语句创建副本
然而,构造方法或[:]做的是浅复制
(即赋值了最外层容器,副本中的元素是源容器中元素的引用).
如果所有元素都是不可变的,那么这样没有问题,还能节省内存.
但是,如果有可变的元素,可能就导致意想不到的问题
"""
# 示例8-6 为一个包含另一列表的列表做浅复制;
# l1 = [3, [66, 55, 44], (7, 8, 9)]
# l2 = list(l1)
# l1.append(100)
# l1[1].remove(55)
# print('l1:', l1)
# print('l2:', l2)
# l2[1] += [33, 22]
# l2[2] += (10, 11)
# print('l1:', l1)
# print('l2:', l2)
"""
为任意对象做深复制和浅复制
深复制(即副本不共享内部对象的引用)
copy模块提供的deepcopy和copy函数能为任意对象做深复制和浅复制
"""


# 示例8-8 校车乘客在途中上车和下车
# class Bus:
#     def __init__(self, passengers=None):
#         if passengers is None:
#             self.passengers = []
#         else:
#             self.passengers = list(passengers)
#
#     def pick(self, name):
#         self.passengers.append(name)
#
#     def drop(self, name):
#         self.passengers.remove(name)
# # 示例8-9 使用copy和deepcopy产生的影响
# import copy
# bus1 = Bus(['ALice', 'Bill', 'Claire', 'David'])
# bus2 = copy.copy(bus1)
# bus3 = copy.deepcopy(bus1)
# print(id(bus1), id(bus2), id(bus3))
# bus1.drop('Bill')
# print(bus2.passengers)
# print(id(bus1.passengers), id(bus2.passengers), id(bus3.passengers))
# print(bus3.passengers)

# 注意,一般来说,深复制不是件简单的事.如果对象有循环引用,那么这个朴素的算法会进入无限循环.deepcopy函数会记住已经赋值的对象,因此能优雅的处理循环引用
# 示例8-10 循环引用:b引用a,然后追加到a中;deepcopy会想办法复制a
# a = [10, 20]
# b = [a, 30]
# a.append(b)
# print(a)
# from copy import deepcopy
# c = deepcopy(a)
# print(c)
# 此外,深复制有时可能太深了.例如,对象可能引用不该复制的外部资源或单例值.
# 我们可以实现特殊方法__copy__()和__deepcopy__(),控制copy和deepcopy的行为
"""
8.4 函数的参数作为引用时
Python唯一支持的参数传递模式是共享传参(call by sharing)
共享传参指函数的各个形式参数获得实参中各个引用的副本.
也就是说,函数内部的形参是实参的别名
这种方案的结果是,函数可能会修改作为参数传入的可变对象,但是无法修改那些对象的标识
(即不能把一个对象替换成另一个对象).
"""
# 示例8-11 函数可能会修改接收到的任何可变对象
# def f(a, b):
#     a += b
#     return a
# x = 1
# y = 2
# print(f(x, y))
# print(x, y)
# a = [1, 2]
# b = [3, 4]
# print(f(a, b))
# print(a, b) # a--> [1, 2, 3, 4]变了
# t = (10, 20)
# u = (30, 40)
# print(f(t, u))
# print(t, u)
"""
8.4.1 不要使用可变类型作为参数的默认值
通常使用None作为接收可变值的参数的默认值
8.4.2 防御可变参数
除非这个方法确实想修改通过参数传入的对象,否则在类中直接把参数赋值给实例变量
之前一定要三思,因为这样会为参数对象创建别名 .如果不确定,那就创建副本

8.5 del和垃圾回收
对象绝不会自行销毁;然而,无法得到对象时,可能会被当做垃圾回收
del语句删除名称,而不是对象.del命令可能会导致对象被当做垃圾回收,
但是仅当删除的变量保存的是对象的最后一个引用,或者无法得到对象时.重新绑定也可能会导致
对象的引用数量归零,导致对象被销毁
如果两个对象相互引用,当他们的引用只存在二者之间时,垃圾回收程序会判定他们都无法获取,进而把他们销毁
有个__del__特殊方法,但是它不会销毁实例,不应该在代码中调用.
即将销毁实例时,Python解释器会调用__del__方法,给实例最后的机会,释放外部资源.
"""
# 示例8-16 没有指向对象的引用时,监视对象生命结束时的情形
# import weakref
# s1 = {1, 2, 3}
# s2 = s1
# def bye():
#     print('Gone   with the wind...')
# ender = weakref.finalize(s1, bye)
# print(ender.alive)
# del s1
# print(ender.alive)
# s2 = 'spam'
# print(ender.alive)
"""
8.6 弱引用
正是因为有引用,对象才会在内存中存在.当对象的引用数量归零后,
垃圾回收程序会把对象销毁.但是,
有时需要引用对象,而不让对象存在的时间超过所需时间.这经常用在缓存中.
弱引用不会增加对象的引用数量.引用的目标对象称为所指对象(referent)
因此我们说,弱引用不会妨碍所指对象被当做垃圾回收
弱引用在缓存应用中很有用,因为我们不想仅因为被缓存引用着而时钟保存缓存对象
"""
# 示例8-17展示了如何使用weakref.ref实例获取所指对象.如果对象存在,调用弱引用可以获得对象;否则返回None
# 示例8-17是一个控制台会话,Python控制台会自动把_变量绑定到结果不为None的表达式结果上.
# 微观管理内存时,往往会得到意外的结果,因为不明显的隐式赋值会对对象创建新引用.
# 控制台中的_变量是一例.调用跟踪对象也常导致意料之外的引用
# 示例8-17 弱引用是可调用对象.返回的是被引用的对象;如果所指对象不存在了,返回None
# import weakref
# a_set = {1, 2}
# wref = weakref.ref(a_set)
# print(wref)
# print(wref())
# a_set = {2, 3, 4}
# print(wref())
# print(wref() is None)
# print(wref() is None)
"""
8.6.1 WeakValueDictionary简介
WeakValueDictionary类实现是一种可变映射,里面的值是对象的弱引用.
被引用的对象在程序中的其他地方被当做垃圾回收后,对应的键会自动从WeakValueDictionary中删除.
因此,WeakValueDictionary经常用于缓存
"""
# 示例8-18 实现一个简单的类,代表各种奶酪
# class Cheese:
#     def __init__(self, kind):
#         self.kind = kind
#     def __repr__(self):
#         return 'Cheese(%r)' % self.kind
# import weakref
# stock = weakref.WeakValueDictionary()
# catalog = [Cheese('Red Leicester'), Cheese('Tilsit'),
#            Cheese('Brie'), Cheese('Parmesan')]
# for cheese in catalog:
#     stock[cheese.kind] = cheese
# print(cheese)
# print(sorted(stock.keys()))
# del catalog
# print(sorted(stock.keys()))
# del cheese
# print(sorted(stock.keys()))
"""
临时变量引用了对象,这可能导致该变量的存在时间比预期常.通常,
这对局部变量来说不是问题,因为他们在函数返回时会被销毁.
但是在上述中,for循环中的变量cheese是全局变量,除非显式删除,否则不会消失

8.6.2 弱引用的局限
基本的list和dict实例不能作为所指对象(作为弱引用的目标),但是他们的子类可以轻松解决这个问题.
int和tuple实例不能作为弱引用的目标,甚至他们的子类也不行

8.7 Python对不可变类型施加的把戏
8.8 本章小结
每个Python对象都有标识,类型和值.只有对象的值会不时变化
其实对象的类型也可以改变,方法只有一种,为__class__属性指定其他类
如果两个变量指代的不可变对象具有相同的值(a==b为True),实际上他们指代的是副本还是同一个对象的别名
基本没什么关系,因为不可变对象的值不会变,但是有一个例外.
不可变的集合,如元组和frozenset:如果不可变集合保存的是可变元素的引用,那么可变元素的值发生变化后,
不可变集合也会随之改变.实际上,这种情况不是很常见.不可变集合不变的是所含对象的标识
变量保存的是引用:
简单的赋值不创建副本
对+=或*=所做的增量赋值来说,如果左边的变量绑定的是不可变对象,会创建新对象;如果是可变对象,会就地修改
为现有的变量赋予新值,不会修改之前绑定的变量.这叫重新绑定:
现在变量绑定了其他对象.如果变量是之前那个对象的最后一个引用,对象会被当做垃圾回收.
函数的参数以别名的形式传递,这意味着,函数可能会修改通过参数传入的可变对象.
这一行为无法避免,除非在本地创建副本,或者使用不可变对象(例如,传入元组,而不传入列表)
使用可变类型作为函数参数的默认值有危险,因为如果就地修改了参数,默认值也变了,
这会影响以后使用默认值的调用
弱引用:保存对象的引用,但不留存对象本身
"""