# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/4 15:02
# @Author   : tangky
# @Site     : 
# @File     : closure_decorator.py
# @Software : PyCharm
"""
第7章 函数装饰器和闭包
nonlocal
除了在装饰器中有用处之外,还是回调式异步编程和函数式编程风格的基础

装饰器工作原理,包括最简单的注册装饰器和比较复杂的参数化装饰器

Python如何计算装饰器句法
Python如何判断变量是不是局部的
闭包存在的原因和工作原理
nonlocal能解决什么问题

进一步探讨装饰器:
实现行为良好的装饰器
标准库中有用的装饰器
实现一个参数化装饰器
7.1 装饰器基础知识
装饰器是可调用对象,其参数是另一个函数(被装饰的函数)
装饰器可能会处理被装饰的函数,然后把它返回,或者将其替换成另一个函数或可调用对象
Python也支持类装饰器
@decorate
def target():
    print('running target()')
效果与以下写法一致
def target():
    print('running target()')
target = decorate(target)
上述两个片段代码执行完毕后得到的target不一定是原来那个target函数,而是decorate(target)返回的函数
"""

# 实例7-1 确认被装饰的函数会被替换,装饰器通常把函数替换成另一个函数
# def deco(func):
#     def inner():
#         print('running inner()')
#
#     return inner
#
#
# @deco
# def target():
#     print('running target()')
#
#
# print(target())
# print(target) # 调用被装饰的target其实会运行inner.target现在是inner的引用

"""
严格来说,装饰器只是语法糖.装饰器可以像常规的可调用对象那样调用,其参数是另一个函数.
有时,这样做更方便,尤其是做元编程(在运行是改变程序的行为)时.
综上,装饰器的一大特性是,能把被装饰的函数替换成其他函数.
第二个特性是,装饰器在加载模块时立即执行

7.2 Python何时执行装饰器
装饰器的一个关键特性是,它们在被装饰的函数定义之后立即运行.
这通常是在导入时(即Python加载模块时)
导入时和运行时的区别
装饰器函数与被装饰的函数在同一模块中定义.实际情况是,装饰器通常在一个模块中定义,然后应用到其他模块中的函数中.
register装饰器返回的函数与通过参数传入的相同.实际上,大多数装饰器会在内部定义一个函数,然后将其返回

7.3 使用装饰器改进"策略"模式
定义体中有函数的名称,但是best_promo用来判断哪个折扣幅度最大的promos列表中也有函数名称.
这种重复是个问题,因为新增策略函数后可能会忘记把它添加到promos列表中,导致best_promo忽略新策略,而且不报错
"""
# 示例7-3 promos列表中的值使用promotion装饰器填充
# promos = []
# def promotion(promo_func):
#     promos.append(promo_func)
#     return promo_func
# @promotion
# def fidelity(order):
#     """为积分为1000或以上的顾客提供5%折扣"""
#     return order.total() * .05 if order.customer.fidelity >= 1000 else 0
# @promotion
# def bulk_item(order):
#     """单个商品为20个或以上时提供10%折扣"""
#     discount = 0
#     for item in order.cart:
#         if item.quantity >= 20:
#             discount += item.total() * .1
#     return discount
# @promotion
# def large_order(order):
#     """订单中的不同商品达到10个或以上时提供7%折扣"""
#     distinct_items = {item.product for item in order.cart}
#     if len(distinct_items) >= 10:
#         return order.total() * .07
#     return 0
#
# def best_promo(order):
#     """选择可用的最佳折扣"""
#     return max(promo(order) for promo in promos)
"""
优点:
促销策略函数无需使用特殊的名称(即用以_promo结尾)
@promotion装饰器突出了被装饰的函数的作用,还便于临时禁用某个促销策略:只需要把装饰器注释掉
促销折扣策略可以在其他模块中定义,在系统中的任何地方都行,只要使用@promotion装饰即可


7.4 变量作用域规则
from dis import dis : LOAD_FAST (对本地的引用)

7.5 闭包
闭包指延伸了作用域的函数,其中包含函数定义体中引用,但是不在定义体中定义的非全局变量.
函数是不是匿名没有关系,关键是它能访问定义体之外定义的非全局变量
"""
# 示例7-8 average_oo.py:计算移动平均值的类
# class Averager():
#     def __init__(self):
#         self.series = []
#     def __call__(self, new_value):
#         self.series.append(new_value)
#         total = sum(self.series)
#         return total/len(self.series)
# # Averager的实例是可调用对象:
# avg = Averager()
# print(avg(10))
# print(avg(11))
# print(avg(12))
# 实例7-9 函数式实现,使用高阶函数make_averager: 计算移动平均值的高阶函数
# def make_averager():
#     series = []
#     def averager(new_value):
#         series.append(new_value)
#         total = sum(series)
#         return total/len(series)
#     return averager
# #
# # 调用make_averager时,返回一个averager函数对象.每次调用averager时,它会把参数添加到系列值中,然后计算当前平均值
# avg = make_averager()
# print(avg(10))
# print(avg(11))
# print(avg(12))
"""
注意,series是make_averager函数的局部变量,因为那个函数的定义体中初始化了series: series=[],
可是,调用avg(10)时,make_averger函数已经返回了,而它的本地作用域也一去不复返了.
在averager函数中,series是自由变量(free variable).
指未在本地作用域中绑定的变量
averager的闭包延伸到那个函数的作用域之外,包含自由变量series的绑定
"""

# 实例7-11 审查make_averager创建的函数
# avg = make_averager()
# print(avg.__code__.co_varnames)
# print(avg.__code__.co_freevars)
# print(avg.__closure__)
# print(avg.__closure__[0].cell_contents)
# cell对象,有个cell_contents属性,保存着真正的值
"""
闭包是一种函数,它会保留定义函数时存在的自由变量的绑定,
这样调用函数时,虽然定义作用域不可用了,但是仍能使用那些绑定.
注意,只要嵌套在其他函数中的函数才可能需要处理不在全局作用域中的外部变量

7.6 nonlocal声明
更好的实现方式,只存储目前的总值和元素个数,然后使用这两个数计算平均值.
"""
# 示例7-13 计算移动平均值的高阶函数,不保存所有历史值,但有权限
# def make_average():
#     count = 0
#     total = 0
#     def averager(new_value):
#         # 更新变量为自由变量
#         nonlocal count, total
#         count += 1
#         total += new_value
#         return total / count
#     return averager
# avg = make_averager()
# print(avg(10))
# print(avg(11))
# print(avg(12))
"""
当count是数字或任何不可变类型时,count += 1语句的作用其实与count = count + 1一样.
因此,我们中averager的定义体重为count赋值了,这会把count编程局部变量.total变量也受这个影响
7-9中的没有给series赋值,只是调用了series.append,并把它传给sum和len,利用了列表是可变的对象
但是对数字,字符串,元组等不可变类型,只能读取,不能更新.如果尝试重新绑定,例如count = count + 1,其实会
隐式创建局部变量count.这样,count就不是自由变量了,因此不会保存在闭包中.
nonlocal(Python3引入)解决这个问题.
它的作用是把变量标记为自由变量,即使在函数中为变量赋值,也会变成自由变量.
如果为nonlocal声明的变量赋予新值,闭包中保存的绑定会更新.
Python2(没有nonlocal)处理方式:把内部函数需要修改的变量(如count和total)存储为可变对象(如字典或简单的实例)的元素或属性,并把哪个对象绑定给一个自由变量


7.7 实现一个简单的装饰器
"""
# 实例7-15:一个简单的装饰器,输出函数的运行时间
# import time
# def clock(func):
#     def clocked(*args):
#         t0 = time.perf_counter()    # 精准的计时器
#         result = func(*args)        # 接收func的所有参数
#         elapsed = time.perf_counter() - t0  # 计算时间差
#         name = func.__name__    # 获取func的函数名
#         arg_str = ', '.join(repr(arg) for arg in args)      # 用", "隔开args中的各个参数组成参数字符串
#         print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
#         return result
#     return clocked
# 示例7-16 使用clock装饰器
# import time
# @clock
# def snooze(seconds):    # 运行snooze实际运行snooze(seconds) = clock(snooze)(seconds) = clocked(seconds)
#     time.sleep(seconds)
# @clock
# def factorial(n):
#     return 1 if n < 2 else n*factorial(n-1)
#
#
# if __name__ == '__main__':
#     print('*' * 40, 'Calling snooze(.123)')
#     snooze(.123)
#     print('*' * 40, 'Calling factorial(6)')
#     print('6! =', factorial(6))
#     print(factorial.__name__)

# 示例7-15中实现的clock装饰器有几个缺点:不支持关键字参数,而且遮盖了被装饰函数的__name__和__doc__属性.
# 示例7-17使用functools.wraps装饰器把相关的属性从func复制到clocked中.此外,还可以正确处理关键字参数

# from clockdeco2 import clock
#
# @clock
# def sample(*args, **kwargs):
#     """just testing"""
#     for arg in args:
#         print(arg)
#     for k, w in kwargs:
#         print(k, w)
#     print(sample.__name__)
#     print(sample.__doc__)
#
#
# if __name__ == '__main__':
#     sample((1, 2, 3), {'a': 1, 'b': 2, 'c': 3})
"""
7.8 标准库中的装饰器
Python内置的三个用于装饰方法的函数:
property, classmethod, staticmethod
另一个常见的装饰器是functools.wraps,它的作用是协助构建行为良好的装饰器.
标准库中最值得关注的两个装饰器是lru_cache和singledispatch(Python3.4新增)
7.8.1 使用functools.lru_cache做备忘
实现了备忘(memoization)功能.
把耗时的函数的结果保存起来,避免传入相同的参数时重复计算.
LRU:Least Recently Used,表明缓存不会无限制增长,一段时间不用的缓存条目会被扔掉
生成第n个斐波那契这种慢速递归函数适合使用lru_cache,
"""
# 示例7-18 生成第n个斐波那契数,递归方式非常耗时
# import functools
# from clockdeco2 import clock
# @functools.lru_cache() # lru_cache可以接受配置参数
# @clock # @lru_cache()应用到@clock返回的函数上
# def fibonacci(n):
#     if n < 2:
#         return n
#     return fibonacci(n-2) + fibonacci(n-1)
#
#
# if __name__ == '__main__':
#     print(fibonacci(6))
# 示例7-19: 使用缓存实现,速度更快
"""
除了优化递归算法之外,lru_cache在从Web中获取信息的应用中也能发挥巨大作用.
lru_cache可以使用两个可选的参数来配置:functools.lru_cache(maxsize=128, typed=False)
maxsize参数指定存储多少个调用的结果.满了之后,旧的结果会被扔掉.为了得到最佳性能,应设置为2的幂
typed参数如果设置为True,把不同参数类型得到的结果分开保存,即把通常认为相等的浮点数和整数参数(如1和1.0)区分开.
lru_cache使用字典存储结果,而且键根据调用时传入的定位参数和关键字参数创建,所以被lru_cache装饰的函数,它的所有参数都必须是可散列的

7.8.2 单分派泛函数
"""
# 示例7-20 生成HTML的htmlize函数,调整了几种对象的输出
# import html
# def htmlize(obj):
#     content = html.escape(repr(obj))
#     return '<pre>{}</pre>'.format(content)
#
#
# print(htmlize({1, 2, 3}))
# print(htmlize(abs))
# print(htmlize('Heimlich & Co.\n- a game'))
# print(htmlize(42))
# print(htmlize(['alpha', 66, {3, 2, 1}]))
"""
因为Python不支持重载方法或函数,所以我们不能使用不同的签名定义htmlize的变体,也无法使用不同的方式处理不同的数据类型.
在Python中,一种常见的做法是把htmlize变成一个分派函数,使用一串if/elif/elif,调用专门的函数,如htmlize_str等.这样不便于
模块的用户扩展,还显得笨拙:时间一长,分派函数htmlize会变得很大,而且它与各个专门函数之间的耦合也很紧密
Python3.4新增的functools.singledispatch(dispatch分派)装饰器可以把整体方案拆分成多个模块,甚至可以为你无法修改的类提供专门的函数.使用@singledispatch装饰的普通函数会变成泛函数(generic function):根据一个参数的类型,以不同的方式执行相同操作的一组函数
"""
# 示例 7-21 singledispatch创建一个自定义的htmlize.register装饰器,把多个函数绑在一起组成一个泛函数
# from functools import singledispatch
# from collections import abc
# import numbers
# import html
#
# @singledispatch
# def htmlize(obj):
#     content = html.escape(repr(obj))
#     return '<pre>{}</pre>'.format(content)
# @htmlize.register(str)
# def _(text):
#     content = html.escape(text).replace('\n', '<br>\n')
#     return '<p>{0}</p>'.format(content)
# @htmlize.register(numbers.Integral)
# def _(n):
#     return '<pre>{0} (0x{0:x})</pre>'.format(n)
# @htmlize.register(tuple)
# @htmlize.register(abc.MutableSequence)
# def _(seq):
#     inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
#     return '<ul>\n<li>' + inner + '</li>\n</ul>'
# @singledispatch标记处理object类型的基函数
# 各个专门函数使用@<<base_function>>.register(<<type>>)装饰
# 专门函数的名称无关紧要:_是个不错的选择
# 为每个需要特殊处理的类型注册一个函数.numbers.Integral是int的虚拟超类
# 可以叠放多个register装饰器,让同一个函数支持不同类型
"""
只要可能,注册的专门函数应该处理抽象基类(如numbers.Integral和abc.MutableSequence),不要处理具体实现(如int和list)
这样,代码支持的兼容类型更广泛.
使用抽象基类检查类型,可以让代码支持这些抽象基类现有和未来的具体子类或虚拟子类.

@singledispatch不是为了把Java的那种方法重载带入Python.在一个类中为同一个方法定义多个重载变体,比在一个函数中使用
一长串if/elif/elif/elif块要更好.但是这两种方案都有缺陷,因为他们让代码单元(类或函数)承担的职责太多
@singledispatch的优点是支持模块化扩展:各个模块可以为它支持的各个类型注册一个专门函数

7.9 叠放装饰器
@d1
@d2
def f():
    print('f')
< == >
def f():
    print('f')
f = d1(d2(f))

7.10 参数化装饰器
创建一个装饰器工厂函数,把参数传给他,返回一个装饰器,然后再把它应用到要装饰的函数上.
"""
# 示例7-22 registration.py模块的删减版
# registry = []
# def register(func):
#     print('running register(%s)' % func)
#     registry.append(func)
#     return func
# @register
# def f1():
#     print('running f1()')
#
# print('running main()')
# print('registry ->', registry)
# f1()
"""
7.10.1 一个参数化的注册装饰器
为register提供一个可选的active参数,
从概念上来看,这个新的register函数不是装饰器,而是装饰器工厂函数.调用它会返回真正的装饰器,这才是应用到目标函数上的装饰器
"""
# 示例7-23 为了接受参数,新的register装饰器必须作为函数调用
# registry = set()
# def register(active=True):
#     def decorate(func):
#         print('running register(active=%s) -> decorate(%s)' % (active, func))
#         if active:
#             registry.add(func)
#         else:
#             registry.discard(func)
#         return func
#     return decorate
# @register(active=False)
# def f1():
#     print('running f1()')
# @register()
# def f2():
#     print('running f2()')
# def f3():
#     print('running f3()')
#
# # f1()
# # f2()
# # f3()
# # 示例7-24 如何把函数添加到registry中,以及如何从中删除函数
# print(registry)
# print(register()(f3))
# print(registry)
# print(register(active=False)(f2))
# print(registry)
"""
7.10.2 参数化clock装饰器
为clock装饰器添加一个功能:让用户传入一个格式字符串,控制被装饰函数的输出
"""
# 示例7-25 clockdeco.py模块:参数和clock装饰器
# import time
# from clockdeco import clock
#
# DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'
#
#
# def clock(fmt=DEFAULT_FMT):
#     def decorate(func):
#         def clocked(*_args):
#             t0 = time.perf_counter()
#             _result = func(*_args)
#             elapsed = time.perf_counter() - t0
#             name = func.__name__
#             args = ', '.join(repr(arg) for arg in _args)
#             result = repr(_result)
#             print(fmt.format(**locals()))  # 使用**locals()是为了在fmt中引用clocked的局部变量
#             return _result
#
#         return clocked
#
#     return decorate
#
#
# if __name__ == '__main__':
#     # @clock()
#     # @clock('{name}: {elapsed}s')
#     @clock('{name}({args}) dt={elapsed:0.3f}s')
#     def snooze(seconds):
#         time.sleep(seconds)
#
#
#
#     for i in range(3):
#         snooze(.123)
"""
工业级装饰器技术
装饰器最好通过实现__call__方法的类实现,不应该像本章的实例那样通过函数实现
7.11 本章小结
高级的Python框架中有注册装饰器的用武之地
参数化装饰器基本上都涉及至少两层嵌套函数,如果想使用@functools.wraps生成装饰器,
为高级技术提供更好的支持,嵌套层级可能还会更深,
functools模块中两个出色的函数装饰器@lru_cache()和@singledispatch
区分导入时和运行时,变量作用域,闭包和新增的nonlocal声明.

"""