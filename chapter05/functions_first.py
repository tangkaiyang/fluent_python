# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/2 19:48
# @Author   : tangky
# @Site     : 
# @File     : functions_first.py
# @Software : PyCharm

"""
第三部分
把函数视作对象
第5章一等函数
在Python中,函数是一等对象.
在运行时创建
能赋值给变量或数据结构中的元素
能作为参数传给函数
能作为函数的返回结果
5.1 把函数视作对象
实例5-1中的控制台会话表明,Python函数时对象.这里我们创建了一个函数,然后调用它,读取它的__doc__
属性,并确定函数对象本身是function类的实例
"""


# 实例5-1 创建并测试一个函数,然后读取它的__doc__属性,再检查它的类型
def factorial(n):
    """
    returns n!
    """
    return 1 if n < 2 else n * factorial(n - 1)


# print(factorial(42))
# print(factorial.__doc__)
# print(type(factorial))
"""
示例5-2展示了函数对象的"一等"本性.我们可以把factorial函数赋值给变量fact,然后通过变量名调用.
我们还能把他作为参数传给map函数.map函数返回一个可迭代对象,里面的元素是把第一个参数(一个函数)
应用到第二个参数(一个可迭代对象,这里是range(11))中各个元素上得到的结果
"""
# 实例5-2 通过别的名称使用函数,再把函数作为参数传递
fact = factorial
# print(fact)
# print(fact(5))
# print(map(factorial, range(11)))
# print(list(map(fact, range(11))))
"""
有了一等函数,就可以使用函数式风格编程.
函数式编程的特点之一就是使用高阶函数
5.2高阶函数
接受函数为参数,或者把函数作为结果返回的函数是高阶函数(higher-order function).
map就是高阶函数,内置函数sorted也是:可选的key参数用于提供一个函数,它会应用到各个元素上进行排序
最为人熟知的高阶函数:
map,filter,reduce和apply(Python3已移除)
如果想使用不定量的参数调用函数,可以编写fn(*args, **keywords),不用再编写apply(fn, args, kwargs)
map,filter和reduce的现代替代品
由于引入了列表推导和生成器表达式,他们变得没那么重要了.
列表推导或生成器表达式具有map和filter两个函数的功能,而且更易于阅读
"""
# 实例5-5 计算阶乘列表:map和filter与列表推导比较
# print(list(map(fact, range(6))))
# print([fact(n) for n in range(6)])
# print(list(map(factorial, filter(lambda n: n % 2, range(6)))))
# print([factorial(n) for n in range(6) if n % 2])
# 实例5-6 使用reduce和sum计算0~99之和
# from functools import reduce
# from operator import add
#
# print(reduce(add, range(100)))
# print(sum(range(100)))
"""
sum和reduce的通用思想是把某个操作连续应用到序列的元素上,累计之前的结果,把一系列值归约成一个值.
all和any也是内置的归约函数
all(iterable)如果iterable的每个元素都是真值,返回True;all([])返回True
any(iterable)主要iterable中有元素是真值,就返回True;any([])返回False

5.3匿名函数
lambda关键字在Python表达式内创建匿名函数
然而,Python简单的句法限制了lambda函数的定义体只能使用纯表达式.
lambda函数的定义体内不能赋值,也不能使用while和try等Python语句.
在参数列表中最适合使用匿名函数
"""
# 实例5-7 使用lambda表达式反转拼写,然后依此给单词列表排序
# fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
# print(sorted(fruits, key=lambda word: word[::-1]))
"""
lambda表达式会创建函数对象

5.4 可调用对象
除了用户定义的函数,调用运算符(即())还可以应用到其他对象上.
相判断对象能否调用,可以用内置的
callable()函数.
Python数据模型文档列出了7种可调用对象:
用户定义的函数:使用def语句或lambda表达式创建
内置函数:使用C语言(CPython)实现的函数,如len或time.strftime.
内置方法:使用C语言实现的方法,如dict.get
方法:在类的定义体中定义的函数
类:调用类时会运行类的__new__方法创建一个实例,然后运行__init__方法,初始化实例,最后把实例返回给调用方.
因为Python没有new运算符,所以调用类相当于调用函数.(通常,调用类会创建那个类的实例,不过覆盖
__new__方法,也可能出现其他行为)
类的实例:如果类定义了__call__方法,那么它的实例可以作为函数调用
生成器函数:使用yield关键字的函数或方法.调用生成器函数返回的是生成器对象
生成器函数在很多方面与其他可调用对象不同.
生成器函数还可以作为协程
Python中有各种各样可调用的类型,因此判断对象能否调用,最安全的方法是使用内置的
callable()函数:
"""
# abs, str, 13
# print([callable(obj) for obj in (abs, str, 13)])
"""
5.5 用户定义的可调用对象
不仅Python函数是真正的对象,
任何Python对象都可以表现得像函数.
为此,只需要实现实例方法__call__
实例5-8实现了BingoCage类,这个类的实例使用任何可迭代对象构建,
而且会在内部存储一个随机顺序排列的列表.
调用实例会取出一个元素
"""
# 示例5-8 bingocall.py:调用BingoCage实例,从打乱的列表中取出一个元素
# import random
#
#
# class BingoCage:
#     def __init__(self, items):
#         self._items = list(items)
#         random.shuffle(self._items)  # shuffle将序列或元组随机排列
#
#     def pick(self):
#         try:
#             return self._items.pop()
#         except IndexError:
#             raise LookupError('pick from empty BingoCage')
#
#     def __call__(self):
#         return self.pick()
# bingo = BingoCage(range(3))
# print(bingo.pick())
# print(bingo())
# print(callable(bingo))
"""
实现__call__方法的类是创建函数对象的简便方式,此时必须在内部维护一个状态,让他在调用之间可用,
例如BingoCage中剩余元素.
装饰器就是这样.装饰器必须是函数,而且有时要在多次调用之间"记住"某些事[例如
备忘(memoization),即缓存消耗大的计算结果,供后面使用].
创建保有内部状态的函数,还有一种截然不同的方式--使用闭包.

5.6 函数内省
除了__doc__,函数对象还有很多属性,使用dir函数可以知道:dir(factorial)
其中大多数是Python对象共有的.
与用户定义的常规类一样,函数使用__dict__属性存储赋予它的用户属性.
这相当于一种基本形式的注解.
下面重点说明函数专有而用户定义的一般对象没有的属性.
计算两个属性集合的差集便能得到函数专有属性列表
"""
# 实例5-9 列出常规对象没有而函数有的属性
# class C: pass
# obj = C()
# def func(): pass
# print(sorted(set(dir(func)) - set(dir(obj))))
"""
5.7 从定位参数到仅限关键字参数
Python提供了极为灵活的参数处理机制,
而且Python3进一步提供了仅限关键字参数(keyword-only argument).
与之密切相关的是,调用函数时使用*和**"展开"可迭代对象,映射到单个参数.
"""
# 实例5-10 tag函数用于生成HTML标签;使用名为cls的关键字参数传入"class"属性,这是一种变通方法,因"class"是Python的关键字
def tag(name, *content, cls=None, **attrs):
    """生成一个或多个HTML标签"""
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value)
                            for attr, value
                            in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)
# tag函数的调用方式有很多
print(tag('br'))
print(tag('p', 'hello'))
print(tag('p', 'hello', 'world'))
print(tag('p', 'hello', id=33))
print(tag('p', 'hello', 'world', cls='sidebar'))
print(tag(content='testing', name='img'))
my_tag = {'name': 'img', 'title': 'Sunset Boulevard',
          'src': 'sunset.jpg', 'cls': 'framed'}
print(tag(**my_tag))

"""
仅限关键字参数是Python3新增的特性
定位函数时若想指定仅限关键字参数,要把他们放到前面有*的参数后面.
如果不想支持数量不定的定位参数,但是想支持仅限关键字参数,在签名中放一个*,
def f(a, *, b):
    return a, b
f(1, b=2) --> (1, 2)
注意,仅限关键字参数不一定要有默认值,
"""