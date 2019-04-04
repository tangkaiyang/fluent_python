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
promos = []
def promotion(promo_func):
    promos.append(promo_func)
    return promo_func
@promotion
def fidelity(order):
    """为积分为1000或以上的顾客提供5%折扣"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0
@promotion
def bulk_item(order):
    """单个商品为20个或以上时提供10%折扣"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount
@promotion
def large_order(order):
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0

def best_promo(order):
    """选择可用的最佳折扣"""
    return max(promo(order) for promo in promos)
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
def make_averager():
    series = []
    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)
    return averager
#
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
# 实例7-15: