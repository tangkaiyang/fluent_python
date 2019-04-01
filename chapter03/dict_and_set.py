# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/3/31 14:08
# @Author   : tangky
# @Site     : 
# @File     : dict_and_set.py
# @Software : PyCharm

"""
第三章 字典和集合
dict类型不但在各种程序中广泛使用,它也是Python语言的基石.
模块的命名空间,实例的属性和函数的关键字参数中都可以看到字典的身影.
跟它有关的内置函数都在__builtins__.__dict__模块中.
Python对字典的实现做了高度优化,而散列表是字典类型性能出众的根本原因.
集合(set)的实现其实也依赖于散列表,
理解散列表的原理
3.1 泛映射类型
collections.abc模块中有Mapping和MutableMapping这两个抽象基类,他们的作用是为dict和其他类似的类型定义形式接口
然而,非抽象映射类型一般不会直接继承这些抽象基类,他们会直接对dict或是collections.User.Dict进行扩展.这些抽象基类的主要作用是作为形式化的文档,
它们定义了构建一个映射类型所需要的最基本的接口.
然后它们还可以跟isinstance一起被用来判定某个数据是不是广义上的映射类型
"""
# from collections import abc
# my_dict = {}
# print(isinstance(my_dict, abc.Mapping))
"""
这里用isinstance而不是type来检查某个参数是否为dict类型,因为这个参数有可能不是dict,而是一个比较另类的映射类型.
标准库里的所有映射类型都是利用dict来实现的,因此它们有个共同的限制,
即只有可散列的数据类型擦能用作这些映射里的键(只有键有这个要求,值并不需要是可散列的数据类型)
什么是可散列的数据类型?hashable
如果一个对象是可散列的,那么在这个对象的生命周期中,它的散列值是不变的,而且这个对象需要实现__hash__()方法.另外可散列对象还要有__qe__()方法,这样才能跟其他键做比较.
如果两个可散列对象是相等的,那么它们的散列值一定是一样的...
原子不可变数据类型(str,bytes和数值类型)都是可散列类型,frozenset也是可散列的,因为根据其定义,frozenset里只能容纳可散列类型.
元组的话,只有当一个元组包含的所有元素都是可散列类型的情况下,它才是可散列的.
"""
# tt = (1, 2, (30, 40))
# print(hash(tt))
# t1 = (1, 2, [30, 40])
# try:
#     print(hash(t1))
# except TypeError as e:
#     print(e)
# tf = (1, 2, frozenset([30, 40]))
# print(hash(tf))
"""
Python里所有的不可变类型都是可散列的.
这个说法其实是不准确的,比如虽然元组本身是不可变序列,
它里面的元素可能是其他可变类型的引用.
一般来说用户自定义的类型的对象都是可散列的,散列值就是他们的id()函数的返回值,所以所有这些对象在比较的时候都是不相等的.如果一个对象实现了__eq__方法,
并且在方法中用到了这个对象的内部状态的话,那么只有当所有这些内部状态都是不可变的情况下,这个对象才是可散列的.
"""
# a = dict(one=1, two=2, three=3)
# print(a)
# b = {'one': 1, 'two': 2, 'three': 3}
# print(b)
# c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
# print(c)
# d = dict([('two', 2), ('one', 1), ('three', 3)])
# print(d)
# e = dict({'three': 3, 'one': 1, 'two': 2})
# print(e)
# print(a == b == c == d == e)
"""
3.2 字典推导
字典推到(dictcomp)可以从任何以键值对作为元素的可迭代对象中构建出字典
3.3 常见的映射方法
dict,defaultdict和OrderedDict,后面两个数据类型是dict的变种,位于collections模块内
*default_factory并不是一个方法,而是一个可调用对象(callable),它的值在
defaultdict初始化的时候由用户设定.
# OrderedDict.popitem()会移除字典里最先插入的元素(先进先出);
同时这份方法还有一个可选的last参数,若为真,则会移除最后插入的元素(后进先出)
d.update(m, [**kwargs]):m是可以是映射或键值对迭代器,用来更新d里对应的条目.
update方法处理参数m的方式,是典型的"鸭子类型".
函数首先检查m是否有keys方法,如果有,那么update函数就把它当做映射对象来处理.否则,函数会退一步,转而把m当做包含了键值对(key, value)元素的迭代器.
Python里大多数映射类型的构造方法都采用了类似的逻辑,因此你既可以用一个映射对象来新建一个映射对象,也可以用包含(key, value)元素的可迭代对象来初始化一个映射对象
用setdefault处理找不到的键
d.get(k, default)给找不到的键一个默认的返回值
实例3-2 从索引中获取单词出现的频率信息,并把他们写进对应的列表
"""
"""创建一个从单词到其出现情况的映射"""
# import sys
# import re
# WORD_RE = re.compile(r'\w+') # w匹配字母数字及下划线
# index = {}
# with open(sys.argv[1], encoding='utf-8') as fp:
#     for line_no, line in enumerate(fp, 1):
#         for match in WORD_RE.finditer(line): # 返回一个产生匹配对象实体的迭代器
#             word = match.group()
#             column_no = match.start()+1
#             location = (line_no, column_no)
#             # 这其实是一种很不好的实现,这样写只是为了证明论点
#             # occurrences = index.get(word, [])
#             # occurrences.append(location)
#             # index[word] = occurrences
#             index.setdefault(word, []).append(location) # setdefault一行替三行,两者效果一样,但是后者键查询次数少
#             # 以字母顺序打印出结果
# for word in sorted(index, key=str.upper):
#     print(word, index[word])
"""
3.4 映射的弹性键查询
查询某个键在映射里不存在,通过这个键读取得到一个默认值.
一是通过defaultdict这个类型而不是普通的dict,
另一个是自己定义一个dict的子类,然后在子类中实现__missing__方法
3.4.1 defaultdict:处理找不到的键的一个选择
示例3.5collections.defaultdict优雅的解决了示例3-4的问题,在用户创建defaultdict对象的时候,就需要给他配置一个为找不到的键创造默认值的方法.
在实例化一个defaultdict的时候,需要给构造方法提供一个可调用对象,这个
可调用对象会在__getitem__碰到找不到的键的时候被调用,让__getitem__返回某种默认值.
dd = defaultdict(list),
dd['new-key']('new-key'不存在)会按照以下步骤行事:
(1)调用list()来建立一个新列表;
(2)把这个新列表作为值,'new-key'作为它的键,放到dd中.
(3)返回这个列表的引用.
而这个用来生成默认值的可调用对象存放在名为default_factory的实例属性中.
"""
# 实例3-5:index_default.py:利用defaultdict实例而不是setdefault方法:
# import sys
# import re
# import collections
# WORD_RE = re.compile(r'\w+')
# index = collections.defaultdict(list)
# with open(sys.argv[1], encoding='utf-8') as fp:
#     for line_no, line in enumerate(fp, 1):
#         for match in WORD_RE.finditer(line):
#             word = match.group()
#             column_no = match.start()+1
#             location = (line_no, column_no)
#             index[word].append(location)
# # 以字母顺序打印出结果
# for word in sorted(index, key=str.upper):
#     print(word, index[word])
"""
把list构造方法作为default_factory来创建一个defaultdict.
如果index没有word的记录,那么default_factory会被调用,为查询不到的键创造一个值.这个值在这里是一个空的列表,然后这个空列表被赋值给index[word],
继而被当做返回值返回,
如果在创建defaultdict的时候没有指定default_factory,查询不存在的键会触发KeyError.
defaultdict里的default_factory只会在__getitem__里被调用,
在其他的方法里完全不会发挥作用.
比如,dd是个defaultdict,k是找不到的键,dd[k]这个表达式会调用default_factory创造某个默认值.
而dd.get(k)则会返回None
背后其实是特殊方法__missing__.
它会在defaultdict遇到找不到的键的时候调用default_factory,而实际上这个特性是所有映射类型都可以选择去支持的

3.4.2 特殊方法__missing__
所有的映射类型在处理找不到的键的时候,都会牵扯到__missing__方法.
虽然基类dict并没有定义这个方法,但是如果有一个类继承了dict,然后这个继承类提供了__missing__方法,那么在__getitem__碰到找不到的键的时候,Python
就会自动调用它,而不是抛出一个KeyError异常

__missing__方法只会被__getitem__调用.
提供__missing__方法对get或者__contains__(in)这些方法的使用没有影响.

有时候,希望查询的时候,映射类型里的键统统转换成str.
"""

# 示例3-6:当有非字符串的键被查找时,StrKeyDict0是如何在该键不存在的情况下,把它转换为字符串的
# 通过get(1, 'N/A')将N/A附给不存在的键1,示例3-7实现
# 如果要自定义一个映射类型,更合适的策略其实是继承collections.UserDict类.
# 示例3-7: StrKeyDict0在查询的时候把非字符串的键转换为字符串
# class StrKeyDict0(dict):
#     def __missing__(self, key):
#         if isinstance(key, str):
#             raise KeyError(key)
#         return self[str(key)]
#
#     def get(self, key, default=None):
#         try:
#             return self[key]
#         except KeyError:
#             return default
#
#     def __contains__(self, key):
#         return key in self.keys() or str(key) in self.keys()
# 这里isinstance(key, str)在__missing__中是必需的.
# 如果没有这个测试,只要str(k)返回的是一个存在的键,那么__missing__是没有问题的,不管是字符串还是非字符串键,它都能正常运行.
# 但是如果str(k)不是一个存在的键,代码就会陷入无限递归.
# 因为__missing__最后的self[str(key)]会调用__getitem__,而这个str(key)不存在,于是__missing__又会被调用
# 为了保持一致性,__contains__方法在这里也是必需的.
# 这是因为k in d这个操作会调用它,但是我们从dict继承的__contains__方法不会在找不到键的时候调用__missing__方法.
# __contains__里还有个细节,就是我们这里没有用更具Python风格的方式--k in my_dict来检查键是否存在,因为那会导致__contains__被递归调用,
# 这里采用了更显式的方法,直接在这个self.keys()里查询
# 像k in my_dict.keys()这种操作在Python3中是很快的,而且几遍映射类型对象很庞大也没关系.
# 这是因为dict.keys()的返回值是一个"视图".视图就像一个集合,而且跟字典类似的是,在视图里查找一个元素的速度很快.

"""
3.5 字典的变种
collections.OrderedDict
这个类型在添加键的时候会保持顺序,因此键的迭代次序总是一致的.
OrderedDict的popitem方法默认删除并返回的是字典里的最后一个元素,
但是如果像my_odict.popitem(last=False)这样调用它,
那么它删除并返回第一个被添加进去的元素.
collections.ChainMap
该类型可以容纳数个不同的映射对象,然后在进行键查找操作的时候,
这些对象会被当做一个整体被逐一查找,知道键被找到为止.
这个功能在给嵌套作用域的语言做解释器的时候很有用,
可以用一个映射对象来代表一个作用域的上下文.
import builtins
pylookup = ChainMap(locals(), globals(), vars(builtins))
collections.Counter
这个映射类型会给键准备一个整数计数器.
每次更新一个键的时候都会增加这个计数器.所以这个类型可以用来给可散列表对象计数,
或者是当成多重集来用--多重集合就是集合里的元素可以出现不止一次.
Counter实现了+和-运算符用来合并记录,还有像most_common([n])这类很有用的方法.
most_common([n])会按照次序返回映射里最常见的n个键和它们的计数.
"""
# 利用Counter来计算单词中各个字母出现的次数:
# import collections
# ct = collections.Counter('abracadabra')
# print(ct)
# ct.update('aaaaazzz')
# print(ct)
# print(ct.most_common(2))

"""
collections.UserDict
这个类其实就是把标准dict用纯Python又实现了一遍.
跟OrderedDict,ChanMap和Counter这些开箱即用的类型不同,
UserDict是让用户继承写子类的.

3.6 子类化UserDict
更倾向于从UserDict而不是dict继承的主要原因是,后者有时会在某些方法的实现上走一些捷径,导致我们不得不在它的子类中重写这些方法,但是UserDict就不会带来这种问题.
UserDict并不是dict的子类,但是UserDict有一个叫做data的属性,是dict的实例,这个属性实际上是UserDict最终存储数据的地方.
这样做的好处是,UserDict的子类就能在实现__setitem__的时候避免不必要的递归,也可以让__contains__里的代码更简洁
3.8利用UserDict改写3.7中的StrKeyDict类:把所有的键都以字符串的形式存储,
还能处理一些创建或者更新实例时包含非字符串类型的键这类意外情况
"""
# 示例3.8 无论是添加,更新还是查询操作,StrKeyDict都会把非字符串的键转换为字符串
import collections


class StrKeyDict(collections.UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item


# __contains__更简洁.这里可以放心假设所有以及存储的键都是字符串.
# 因此,只要在self.data上查询就好了,并不需要向StrKeyDict0那样去麻烦self.keys()
# __setitem__会把所有的键都转换成字符串.由于把具体的实现委托给了self.data属性,
"""
因为UserDict继承的是MutableMapping,所以StrKeyDict里剩下的那些映射类型的方法都是从UserDict,MutableMapping和Mapping这些超类继承而来的.
特别是最后的Mapping类,它虽然是一个抽象基类(ABC),但它却提供了几个实用的方法:
MutableMapping.updata
这个方法不但可以为我们所直接利用,它还用在__init__里,让构造方法可以利用传入的各种参数(其他映射类型,元素是(key, value)对的可迭代对象和键值参数)来新建实例.
因为这个方法在背后是使用self[key]=value类添加新值的,所以它其实是在使用我们的__setitem__方法
Mapping.get
在StrKeyDict0中,我们不得不改写get方法,好让它的表现跟__getitem__一致.
而在3.8则没这个必要了,因为它继承了Mapping.get方法
Python3.5之后,TransformDict新类型:比起StrKeyDict,TransformDict的通用性更强,也更复杂.
因为它吧键存放成字符串的同时,还要按照它原来的样子存一份.

3.7 不可变映射类型
Python3.3开始,types模块中引入了一个封装类名叫
MappingProxyType.如果给这个类一个映射,它会返回一个只读的映射视图.
虽然只是个只读视图,但是它是动态的.
这意味着如果对原映射做处理改动,我们通过这个视图可以观察到,但是无法通过这个视图对原映射做出修改
"""
# 实例3-9 用MappingProxyType来获取字典的只读实例mappingproxy
# from types import MappingProxyType
# import logging
# d = {1: 'A'}
# d_proxy = MappingProxyType(d)
# print(d_proxy)
# print(d_proxy[1])
# try:
#     d_proxy[2] = 'x'
# except TypeError:
#     print(logging.INFO)
# d[2] = 'B'
# print(d_proxy)
# print(d_proxy[2])
# d_proxy是动态的,对d所作的任何改动都会反馈到它上
"""
3.8 集合论
set,frozenset
集合的本质是许多唯一对象的聚集.
集合可以用于去重
集合中的元素必须是可散列的,set类型本身是不可散列的,但是frozenset可以.
因此可以创建一个包含不同frozenset的set
中缀运算符:
a | b 并集
a & b 交集
a - b 差集
例如,我们有一个电子邮件地址的集合(haystack),还要维护一个较小的电子邮件地址集合(needles),
然后求出needles中有多少地址也出现在了haystack里
示例3-10: needles的元素在haystack里出现的次数,两个变量都是set类型
found = len(needles & haystack)
示例3-11: needles的元素在haystack里出现的次数
found = 0
for n in needles:
    if n in haystack:
        found += 1
3-10比3-11要快一些;3-11可以用在任何迭代对象needles和haystack上,而示例3-10要求两个对象都是集合.
3-12 可以用在任何可迭代对象上
found = len(set(needles) & set(haystack))
found = len(set(needles).intersection(haystack))
速度极快的查找功能(背后的散列表)

3.8.1 集合字面量
创建一个空集,set(),不带任何参数,{}是一个空字典
3.8.2 集合推导(setcomps)
"""
# 示例3-13 新建一个Latin-1字符集合,该集合里的每个字符的Unicode名字都有"SIGN"这个单词
# from unicodedata import name
# print({chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i), '')})
"""
3.8.3 集合的操作
中缀运算符需要两侧被操作的对象都是集合类型,
但是其他的所有方法则要求所传入的参数是可迭代对象
例:相求4个聚合类型a,b,c和d的合集,可以用a.union(b, c, d)
这里a必须是个set,但是其他可以是任何类型的可迭代对象

3.9 dict和set的背后
散列表
3.9.1 一个关于效率的实验
dict.fromkeys([1, 2, 3], ['one', 'two', 'three']) -->
{1: ['one', 'two', 'three'], 2: ['one', 'two', 'three'], 3: ['one', 'two', 'three']}
3.9.2 字典中的散列表
散列表其实是一个稀疏数组(总是有空白元素的数组称为稀疏数组).
散列表里的单元通常叫做表元(bucket).
在dict的散列表中,每个键值对都占用了一个表元,每个表元都有两部分,
一个是对键的引用,另一个是对值的引用.
所以所有表元的大小一致,所以可以通过偏移量来读取某个表元.
因为Python会设法博阿正大概还有三分之一的表元是空的,所以在快要达到这个
阈值的时候,原有的散列表会被复制到一个更大的空间里面
如果要把一个对象放入散列表,那么首先要计算这个元素键的散列值.
hash()
01.散列值和相等性
内置的hash()方法可用于所有的内置类型对象.如果是自定义对象调用hash()的话,
实际上是运行的自定义的__hash__.如果两个对象在比较的时候是相等的,
那他们的散列值必须相等,都在散列表就不能正常运行了.
如1==1.0为真,那么它们的散列值相等也为真,但是这两个数字的内部构造完全不一样
为了让散列值能够胜任散列表索引这一角色,他们必须在索引空间中尽量分散开来.
这意味着在最理想的状况下,越是相似但不相等的对象,他们散列值的差别应该越大.
从Python3.3开始,str,bytes和datetime对象的散列值计算过程中,
多了随机的"加盐"这一步.所加盐值是Python进程内的一个常量,但是每次启动
Python解释器都会生成一个不同的盐值.
随机盐值的加入是为了防止DOS攻击而采取的一种安全措施
02.散列表算法
插入新值时,Python可能会按照散列表的拥挤程度决定是否要重新分配内存为它扩容.
如果增加了散列表的大小,那散列值所占的位数和用作索引的位数都会随之增加,这样做的目的是为了减少发生散列冲突的概率.冲突发生几率很低

3.9.3 dict的实现及其导致的结果
01,键必须是可散列的:
一个可散列的对象:
(1)支持hash()函数,并且通过__hash__()方法所得到的的散列值是不变的
(2)支持通过__eq__()方法来检测相等性
(3)若a==b为真,则hash(a)==hash(b)也为真
所有由用户自定义的对象默认都是可散列的,因为他们的散列值由id()来获取,
而且他们都是不相等的.
02,字典在内存上的开销巨大
03,键查询很快
04,键的次序取决于添加顺序
添加新键会出现散列冲突
05,往字典里添加新键可能会改变已有键的顺序
不要对字典同时进行迭代和修改
Python3中,.keys(),.items()和.values()方法返回的都是字典视图.更像集合.视图有动态的特性,可以实时反馈字典的变化
"""
# 示例3-17 用同样的数据创建了3个字典,唯一的区别就是数据出现的顺序不一样.虽然键的次序是乱的,这3个字典仍然被视作相等的
# 世界人口数量前10位国家的电话区号
# DIAL_CODES = [
#     (85, 'China'),
#     (91, 'India'),
#     (1, 'United States'),
#     (62, 'Indonesia'),
#     (55, 'Brazil'),
#     (92, 'Pakistan'),
#     (880, 'Bangladesh'),
#     (234, 'Nigeria'),
#     (7, 'Russia'),
#     (81, 'Japan'),
# ]
# d1 = dict(DIAL_CODES)
# print('d1:', d1.keys())
# d2 = dict(sorted(DIAL_CODES))
# print('d2:', d2.keys())
# d3 = dict(sorted(DIAL_CODES, key=lambda x: x[1]))
# print('d3:', d3.keys())
# assert d1 == d2 and d2 == d3

"""
3.9.4 set的实现以及导致的结果
set和frozenset的实现也依赖散列表,但是他们的散列表里存放的只有元素的引用.字典只存放键没有相应的值,字典加上无意义的值当做集合
集合里的元素必须是可散列的.
集合很消耗内存.
可以很高效的判断元素是否存在与某个集合
元素的次序取决于被添加到集合里的次序
往集合里添加元素,可能会改变集合里已有元素的次序

3.10 本章小结

"""