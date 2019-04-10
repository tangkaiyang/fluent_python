# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/10 7:08
# @Author   : tangky
# @Site     : 
# @File     : protocol_to_abc.py
# @Software : PyCharm
"""
第11章 接口:从协议到抽象基类
接口:从鸭子类型的代表特征动态协议,
到使接口更明确,能验证实现是否符合规定的抽象基类(Abstract Base Class, ABC)
抽象基类的常见用途:实现接口时作为超类使用.
如何使用注册机制声明一个类实现了某个接口,而不进行子类化操作.
说明如何让抽象基类自动"识别"任何符合接口的类--不进行子类化或注册
不建议编写抽象基类,容易过度设计
抽象基类与描述符和元类一样,适用于构建框架的工具,
因此,只有少数Python开发者编写的抽象基类不会对用户施加不必要的限制,让他们做无用功

11.1 Python文化中的接口和协议
按照定义,受保护的属性和私有属性不在接口中:即便"受保护的"属性也只是采用命名约定实现的(单个前导下划线);私有属性可以轻松地访问
另一方面,不要觉得把公开数据属性放入对象的接口中有什么不妥,因为如果需要,
总能实现读值方法和设值方法,把数据属性变成特性,

接口的补充定义:对象公开方法的子集,让对象在系统中扮演特定的角色
接口是实现特定角色的方法集合
协议与继承没有关系.
一个类可能会实现多个接口,从而让实例扮演多个角色
协议是接口,但不是正式的(只由文档和约定定义),因此协议不能像正式接口那样施加限制
(抽象基类对接口一致性的强制).
允许一个类只实现部分接口

11.2 Python喜欢序列
Python数据模型的哲学是尽量支持基本协议.
对序列来说,即便是最简单的实现,Python也会力求做到最好
示例11-3中的Foo类,没有继承abc.Sequence,而且只实现了序列协议的一个方法:__getitem__
"""
# 示例11-3 定义__getitem__方法,只实现了序列协议的一部分,这样就足够访问元素,迭代和使用in运算符了
# class Foo:
#     def __getitem__(self, pos):
#         return range(0, 30, 10)[pos]
# f = Foo()
# print(f[1])
# for i in f:print(i)
# print(20 in f)
# print(15 in f)
"""
Python会特殊对待看起来像是序列的对象.
Python中的迭代是鸭子类型的一种极端形式:为了迭代对象,解释器会尝试调用两种不同的方法
协议的动态本性

11.3 使用猴子补丁在运行时实现协议
洗牌:random.shuffle函数(就地打乱序列)
如果遵守既定协议,很有可能增加利用现有的标准库和第三方代码的可能性,这得益于鸭子类型
shuffle函数要调换集合中元素的位置,而FrenchDeck只实现了不可变的序列协议.
可变的序列还必须提供__setitem__方法
Python是动态语言,因此我们可以在运行时修正这个问题,甚至还可以在交互式控制台中,
示例11-6 为FrenchDeck打猴子补丁,把它变成可变的,让random.shuffle能处理
def set_card(deck, position, card):
    deck._cards[position] = card
# deck可以替换为self,Python方法说到底都是普通函数,把第一个参数命名为self只是约定
FrenchDeck.__setitem__ = set_card
shuffle(deck)
这里的关键是,set_card函数要知道deck对象有一个名为_cards的属性,而且_cards的值必须是可变
序列.然后,我们把set_card函数赋值给特殊方法__setitem__,从而把他依附到FrenchDeck类上.
这种技术叫做猴子补丁:在运行时修改类或模块,而不改动源码.
猴子补丁很强大,但是打补丁的代码与要打补丁的程序耦合十分紧密,而且往往要处理隐藏和没有文档的部分
协议是动态的:random.shuffle函数不关心参数的类型,只要那个对象实现了部分可变序列协议即可.
即便对象一开始没有所需方法也没关系,后来再提供也行
"鸭子类型":对象的类型无关紧要,只要实现了特定的协议即可

11.4 Alex Martelli的水禽
参照水禽的分类学演化,在鸭子类型的基础上增加
白鹅类型(goose typing),只要cls是抽象基类,即cls的元类是abc.ABCMeta,就可以使用isinstance(obj, cls)
Python的抽象基类还有一个重要的实用优势:可以使用register类方法在终端用户的代码中把某个类"声明"为一个抽象基类的"虚拟"子类(为此,被注册的类必须满足抽象基类对方法名称和签名的要求,
最重要的是要满足底层语义契约;但是,开发哪个类时不用了解抽象基类,更不用继承抽象基类).
这大大地打破了严格的强耦合,与面向对象编程人员掌握的知识有很大出入,因此使用继承时要小心
有时,为了让抽象基类识别子类,甚至不用注册
class Struggle:
    def __len__(self): return 23
from collections import abc
isinstance(Struggle(), abc.Sized)--> True
无需注册,abc.Sized也能把Struggle识别为自己的子类,
只要实现了特殊方法__len__即可(要使用正确的句法和语义实现,前者要求没有参数,
后者要求返回一个非负整数,指明对象的长度;如果不使用规定的句法和语义实现特殊方法,会导致非常严重的问题)

继承抽象基类很简单,只需要实现所需的方法,
能通过注册虚拟子类实现
然而,即便是抽象基类,也不能滥用isinstance检查,用多了可能导致代码异味,
即表明面向对象设计得不好.在一连串if/elif/elif中使用isinstance做检查,然后根据对象的类型
执行不同的操作,通常不是好的做法;此时应该使用多态,
即采用一定的方式定义类,让解释器把调用分派给正确的方法,而不适用if/elif/elif块硬编码分派逻辑
具体使用时,上述建议有一个常见的例外:
有些Python API接受一个字符串或字符串序列;如果只有一个字符串,可以把它放到列表中,从而简化处理.
因此字符串是序列类型,所以为了把它和其他不可变序列区分开,最简单的方式是使用isinstance(x, str)检查
抽象基类用于封装框架引入的一般性概念和抽象的,例如"一个序列"和"一个确切的数".
基本上不需要自己编写新的抽象基类,只要正确使用现有的抽象基类,

11.5 定义抽象基类的子类
先利用现有的抽象基类(collections.MutableSequence),
然后自己定义.
示例11-8 frenchdeck2.py: FrenchDeck2, collections.MutableSequence的子类
导入时,Python不会检查抽象方法的实现,在运行时实例化FrenchDeck2类时才会真正检查.
如果没有正确实现某个抽象方法,Python会抛出TypeError异常,并把错误消息设为
'Can't instantiate abstract class FrenchDeck2 with abstract methods __delitem__, insert'
因此,即便FrenchDeck2类不需要__delitem__和insert提供的行为,也要实现,因为MutableSequence抽象基类需要它们
FrenchDeck2从Sequence继承了几个拿来即用的具体方法:
__contains__,__iter__,__reversed__,index和count
FrenchDeck2从MutableSequence继承了
append,extend,pop,remove和__iadd__
在collections.abc中,每个抽象基类的具体方法都是作为类的公开接口实现的,因此不用知道实例的内部接口
要想实现子类,我们可以覆盖从抽象基类中继承的方法,以更高效的方式重新实现.
例如,__contains__方法会全面扫描序列,
可是,如果你定义的序列按顺序保存元素,那就可以重新定义__contains__方法,
使用bisect函数做二分查找,从而提升搜索速度

11.6 标准库中的抽象基类
大多数抽象基类在collections.abc模块中定义,
numbers和io包中有一些抽象基类,
但是collections.abc中的抽象基类最常用
11.6.1 collections.abc模块中的抽象基类
标准库中有两个名叫abc的模块
这里的是collections.abc
另外还有一个abc模块,定义的是abc.ABC类.
每个抽象基类都依赖这个类,但是不用导入它,除非定义新抽象基类
https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes
上述连接的文档,对各个抽象基类做了总结,说明了相互之间的关系,
以及各个基类提供的抽象方法和具体方法(称为"混入方法").
讨论抽象基类时通常不用考虑多重继承
Iterable,Container和Sized
各个集合应该继承这三个抽象基类,或者至少实现兼容的协议.
Iterable通过__iter__方法支持迭代,
Container通过__contains__方法支持in运算符,
Sized通过__len__方法支持len()函数
Sequence,Mapping和Set
这三个是主要的不可变集合类型,而且各自都有可变的子类.
MutableSequence,MutableMapping和MutableSet
MappingView
在Python3中,映射方法.items(),.keys()和.values()返回的对象分别是
ItemsView,KeysView和ValuesView的实例.前两个类还从Set类继承了丰富的接口
Callable和Hashable
这两个抽象基类与集合没有太大关系,只不过因为collections.abc是标准库中定义抽象基类的第一模块,
而他们又太重要了,
这两个抽象基类的主要作用是为内置函数isinstance提供支持,以一种安全的方式判断对象能不能调用或散列
若想检查是否能调用,可以使用内置的callable()函数;但是没有类似的hashable()函数,
因此测试对象是否可散列,最好使用isinstance(my_obj, Hashable)
Iterator
注意它是Iterable的子类.

11.6.2 抽象基类的数字塔
numbers包定义的是"数字塔"(即各个抽象基类的层次结构是线性的),
其中Number是位于最顶端的超类,随后是Complex子类,依次往下,最低端是Integral类
Number--> Complex --> Real --> Rational(合理的,即有理数) --> Integral
因此,如果想检查一个数是不是整数,可以使用isinstance(x, numbers.Integral)
这样代码就能接受int,bool(int的子类),或者外部库使用numbers抽象基类注册的其他类型.
为了满足检查的需要,你或者你的API的用户可以把兼容的类型注册为numbers.Integral的虚拟子类
与之类似,如果一个值可能是浮点数类型,可以使用isinstance(x, numbers.Real)检查.
这样代码就能接受bool,int,float,fractions.Fraction(分数),或者外部库(如NumPy,它做了相应的注册)提供的非复数类型
decimal.Decimal没有注册为numbers.Real的虚拟子类.原因是如果程序需要Decimal的精度,要防止与其他低精度数字类型混淆,尤其是浮点数

11.7 定义并使用一个抽象基类
构建一个广告管理框架,名为ADAM
支持用户提供随机挑选的无重复类.
抽象基类Tombola,这是宾果机和打乱数字的滚动容器的意大利名
Tombola抽象基类有四个方法,其中两个是抽象方法.
.load(...):把元素放入容器
.pick():从容器中随机拿出一个元素,返回选中的元素
具体方法:
.loaded():如果容器中至少有一个元素,返回True
.inspect():返回一个有序元组,由容器中的现有元素构成,不会修改容器的内容(内部的顺序不保留)
其实,抽象方法可以有实现代码.即使实现了,子类也必须覆盖抽象方法,但是在子类中可以使用super()函数调用抽象方法,为它添加功能,
而不是从头开始实现.
抽象基类可以提供具体方法,只要依赖接口中的其他方法就行
选择LookupError:在Python的异常层次关系中,它与IndexError和KeyError有关,
这是两个具体实现Tombola所用的数据结构最有可能抛出的异常
# 示例11-10 异常类的部分层次结构
LookupError(lookup,检查)
IndexError是LookupError的子类,尝试从序列中获取索引超过最后位置的元素时抛出
使用不存在的键从映射中获取元素时,抛出KeyError异常
"""
# 示例11-9 tombola.py:Tombola是抽象基类,有两个抽象方法和两个具体方法
# 示例11-11 不符合Tombola要求的子类无法蒙混过关
# from tombola import Tombola
#
#
# class Fake(Tombola):
#     def pick(self):
#         return 13
#
#
# print(Fake)
# f = Fake() # 实例化Fake时抛出TypeError.Python认为Fake是抽象类,因为它没有实现load方法,这是Tombola抽象基类声明的抽象方法之一
"""
11.7.1 抽象基类句法详解
声明抽象基类最简单的方式是继承abc.ABC或其他抽象基类
abc.ABC是Python3.4新增的类.
之前的版本无法继承现有的抽象基类.
此时,必须在class语句中使用metaclass=关键字,把值设为abc.ABCMeta(不是abc.ABC)
class Tombola(metaclass=abc.ABCMeta):
...
除了@abstractmethod之外,abc模块还定义了
@abstractclassmethod,@abstractstaticmethod和@abstractproperty三个装饰器(Python3.3起废弃了,因为装饰器可以在@abstractmethod上堆叠)
例如,声明抽象类方法的推荐方式:
class MyABC(abc.ABC):
    @classmethod
    @abc.abstractmethod 
    def an_abstract_classmethod(cls, ...):
        pass
在函数上堆叠装饰器的顺序通常很重要,@abstractmethod的文档特别指出:
与其他方法描述符一起使用时,abstractmethod()应该在最里层

11.7.2 定义Tombola抽象基类的子类
示例11-12中的BingoCage类实现了所需的抽象方法load和pick,从Tombola中继承了loaded方法,覆盖了inspect方法,还增加了__call__方法
"""
# 示例11-12 bingo.py: BingoCage是Tombola的具体子类
# 示例11-13 Tombola接口的另一种实现,LotteryBlower打乱"数字球"后没有取出最后一个,而是取出随机位置上的球
# 示例11-13 lotto.py: LotteryBlower是Tombola的具体子类,覆盖了继承的inspect和loaded方法
"""
11.7.3 Tombola的虚拟子类
白鹅类型的一个基本特性(也是值得用水禽来命名的原因):
即便不继承,也有办法把一个类注册为抽象基类的虚拟子类.
这样做时,我们保证注册的类忠实地实现了抽象基类定义的接口,
而Python会相信我们,从而不做检查.
注册虚拟子类的方式是在抽象基类上调用register方法.
注册的类会变成抽象基类的虚拟子类,而且issubclass和isinstance等函数都能识别,
但是注册的类不会从抽象基类中集成任何方法或属性
虚拟子类不会继承注册的抽象基类,而且任何时候都不会检查它是否符合抽象基类的接口,
即便在实例化时也不会检查.为了避免运行时错误,虚拟子类要实现所需的全部方法
register方法通常作为普通的函数调用,不过也可以作为装饰器使用.
使用装饰器句法实现了TomboList类,这是Tombola的一个虚拟子类
TomboList是list的真实子类和Tombola的虚拟子类
"""
# 示例11-14 tombolist.py: TomboList是Tombola的虚拟子类
"""
虚拟子类,注册之后不会从父类继承任何方法或属性,所以叫做虚拟子类
继承,继承就会继承父类的东西
注册之后,使用issubclass和isinstance函数判断TomboList是不是Tombola的子类
"""
from tombola import Tombola
from tombolist import TomboList
#
# print(issubclass(TomboList, Tombola))
# t = TomboList(range(100))
# print(t)
# print(isinstance(t, Tombola))
# print(TomboList.__mro__)
"""
然而,类的继承关系在一个特殊的类属性中指定--__mro__,即方法解析顺序(Method Resolution Order)
这个属性的作用很简单,按顺序列出类及其超类,Python会按照这个顺序搜索方法
查看TomboList类的__mro__属性,只列出"真实的"超类,即list和object
其中没有Tombola,因此TomboList没有从Tombola中继承任何方法

11.8 Tombola子类的测试方法
__subclasses__():这个方法返回类的直接子类列表,不含虚拟子类
_abc_registry:只有抽象基类有这个数据属性,其值是一个WeakSet对象,
即抽象类注册的虚拟子类的弱引用
迭代Tombola.__subclasses__()和Tombola._abc_registry得到的列表,然后把各个类赋值给在doctest中使用的ConcreteTombola
"""
# 示例11-15 tombola_runner.py: Tombola子类的测试运行程序
"""
11.9 Python使用register的方式
用于注册其他地方定义的类
collections.abc模块总:
把内置类型tuple,str,range和memoryview注册为Sequence的虚拟子类:
Sequence.register(tuple)
Sequence.register(str)
Sequence.register(range)
Sequence.register(memoryview)
这些类型在导入模块是注册,因为必须导入才能使用抽象基类:
能访问MutableMapping才能编写isinstance(my_dict, MutableMapping)

11.10 鹅的行为有可能像鸭子
即便不注册,抽象基类也能把一个类识别为虚拟子类
abc.Sized实现了一个特殊的类方法,__subclasshook__
__subclasshook__在白鹅类型中添加了一些鸭子类型的踪迹.
我们可以使用抽象基类定义正式接口,可以始终使用isinstance检查,也可以完全使用不相关的类,
只要实现特定的方法即可(或者做些事情让__subclasshook__信服).
当然,只有提供__subclasshook__方法的抽象基类才能这么做
可能不需要在自己定义的抽象基类中定义__subclasshook__方法
在Python源码中只见到了Sized着一个抽象基类实现了__subclasshook__方法,而Sized只声明了一个特殊方法,
因此只用检查这么一个特苏芳芳.鉴于__len__方法的"特殊性",我们可以确定它能做到该做的事,
但是对其他特殊方法和基本的抽象基类来说,很难这么肯定.
例如,虽然映射实现了__len__,__getitem__和__iter__,但是不应该把他们视作Sequence的子类型,
因为不能使用整数偏移值获取元素,也不能保证元素的顺序.
当然,OrderedDict除外,它保留了插入元素的顺序,但是不支持通过偏移获取元素

11.11 本章小结
非正式接口(称为协议)的高度动态本性,
抽象基类的静态接口声明
抽象基类的动态特性:虚拟子类以及使用__subclasshook__方法动态识别子类
协议风格的接口与继承完全没有关系,实现同一个协议的各个类是相互独立的.
在鸭子类型中,接口就是这样的
猴子补丁,协议的动态本性
部分实现协议也是有用的
白鹅类型
使用抽象基类明确声明接口,而且类可以子类化抽象基类或使用抽象基类注册(无需在继承关系中确立静态的强链接),宣称它实现了某个接口
__subclasshook__魔法方法:这个方法的作用是让抽象基类识别没有注册为子类的类,
不要自己定义抽象基类,除非要构建允许用户扩展的框架
日常使用中,我们应该创建现有抽象基类的子类,或者使用现有的抽象基类注册
还可能在isinstance检查中使用抽象基类,

尽管抽象基类使得类型检查变得更容易了,但不应该在程序中过度使用它.
Python的核心在于它是一门动态语言,它带来了极大的灵活性.如果处处都强制实行类型约束,那么会使代码变得更加复杂,而本不应该如此.
我们应该拥抱Python的灵活性

如果觉得自己想创建新的抽象基类,先试着通过常规的鸭子类型来解决问题

Python是动态强类型语言
"""


