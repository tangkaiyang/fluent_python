# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/9 9:53
# @Author   : tangky
# @Site     : 
# @File     : Python_style_object.py
# @Software : PyCharm
"""
第9章 符合Python风格的对象
鸭子类型(duck typing)
按照预定行为实现对象所需的方法即可

支持用于生成对此昂其他表示形式的内置函数(如repr(), bytes(),等等)
使用一个类方法实现备选构造方法
扩展内置的format()函数和str.format()方法使用的格式微语言
实现只读属性
把对象变为可散列的,以便在集合中及作为dict的键使用
利用__slots__节省内存

如何以及何时使用@classmethod和@staticmethod装饰器
Python的私有属性和受保护属性的用法,约定和局限

9.1 对象表示形式
repr()以便于开发者理解的方式返回对象的字符串表示形式
str()以便于用户理解的方式返回对象的字符串表示形式
repr() --> __repr__
str() --> __str__
为对象提供的其他表示形式:
bytes()函数调用它获取对象的字节序列表示形式.__bytes__
format()和str.format()使用特殊的格式代码显示对象的字符串表示形式.__format__
Python3中,__repr__,__str__和__format__都必须返回Unicode字符串(str类型).
只有__bytes__方法应该返回字节序列(bytes类型)

9.2 再谈向量类

9.3 备选构造方法

9.4 classmethod与staticmethod
定义操作类,而不是操作实例的方法.classmethod改变了调用方法的方式,因此类方法的第一个参数是类本身,而不是实例
classmethod最常见的用途是定义备选构造方法
staticmethod装饰器也会改变方法的调用方式,但是第一个参数不是特殊的值.其实,静态方法就是普通的函数,只是
碰巧在类的定义体中,而不是模块层定义
"""
# 实例9-4 比较classmethod和staticmethod的行为
# class Demo:
#     @classmethod
#     def klassmeth(*args):
#         return args
#     @staticmethod
#     def statmeth(*args):
#         return args
#
#
# print(Demo.klassmeth())
# print(Demo.klassmeth('spam'))
# print(Demo.statmeth())
# print(Demo.statmeth('spam'))
"""
classmethod装饰器非常有用,
如果想定义不需要与类交互的函数,那么在模块中定义就好了.

9.5 格式化显示
内置的format()函数和str.format()方法把各个类型的格式化方式委托给相应的.__format__(format_spec)方法.
format_spec是格式说明符,
format(my_obj, format_spec)的第二个参数
format(brl, '0.4f')--> '0.4115'(brl=0.41152343252454)
str.format()方法的格式字符串,{}里代换字段中冒号后面的部分
'{rate:0.2f} USD'.format(rate=brl)
'{0.mass:5.3e}'字段名:格式说明符
格式说明符使用的表示法叫格式规范微语言(Format Specification Mini-Language)
格式规范微语言为一些内置类型提供了专门的表示代码.
b:二进制int类型
x:十六进制int类型
f:小数形式的float类型
%:百分数形式
格式规范微语言是可扩展的,因为每个类可以自行决定如何解释format_spec参数.
例如:datetime模块中的类,他们的__format__方法使用的格式代码与strftime()函数一样.
from datetime import datetime
now = datetime.now()
format(now, '%H:%M:%S')
"It's now {:%I:%M %p}".format(now)
如果类没有定义__format__方法,从object继承的方法会返回str(my_object)

在微语言中添加自定义的格式代码:
为自定义的格式代码选择字母时,避免使用其他类型用过的字母
整数:bcdoxXn
浮点数:eEfFgGn%
字符串:s

9.6 可散列的Vector2d
把Vector2d实例变成可散列的,使用__hash__方法(还有__eq__方法).
此外,要让向量不可变
使用两个前导下划线(尾部没有下划线,或者一个下划线),把属性标记为私有的.
注意,向量不可变是为了实现__hash__方法.这个方法返回一个整数,理想情况下还要考虑对象属性的散列值(__eq__方法也要使用)
因为相等的对象应该具有相同的散列值.
使用位运算符异或(^)混合各分量的散列值
要想创建可散列的类型,不一定要实现特性,也不一定要保护实例特性.
只需要正确实现__hash__和__eq__方法即可.
但是,实例的散列值决不应该变化(只读特性)

9.7 Python的私有属性和"受保护的"属性
Python避免子类意外覆盖"私有"属性的机制:
如果以__mood的形式(两个前导下划线,尾部没有或只有一个下划线)命名实例属性,
Python会把属性名存入实例的__dict__属性中,而且会在前面加上一个下划线和类名.
因此,对Dog类来说,__mood--> _Dog__mood;
对Beagle来说,__mood--> _Beagle__mood;
这个语言特性叫名称改写(name mangling)
名称改写是一种安全措施,不能保证万无一失:它的目的是避免意外访问,不能防止故意做错事
只要知道改写私有属性名的机制,任何人都能直接读取私有属性__对调试和序列化有用
v1._Vector__x = 7,改写私有变量
约定使用一个下划线前缀编写"受保护"的属性(如:self._x)

9.8 使用__slots__类属性节省空间
默认情况下,Python在各个实例中名为__dict__的字典里存储实例属性
为了使用底层的散列表提升访问速度,字典会消耗大量内存.
如果要处理数百万个属性不多的实例,通过__slots__类属性,能节省大量内存,
方法是让解释器在元组中存储实例属性,而不用字典
继承自超类的__slots__属性没有效果.Python只会使用各个类中定义的__slots__属性
定义__slots__的方式是,创建一个类属性,使用__slots__这个名字,并把它的值设为一个字符串构成的可迭代对象,其中各个
元素表示各个实例属性.
作者喜欢用元组,这样定义的__slots__中所含的信息不会变化
在类中定义__slots__属性的目的是告诉解释器:"这个类中的所有实例属性都在这儿了!"这样,Python会在各个实例中使用类似
元组的结构存储实例变量,从而避免使用消耗内存的__dict__属性.
如果要处理数百万个数值对象,应该使用NumPy数组.
NumPy数组能高效使用内存,而且提供了高度优化的数值处理函数,其中很多都一次操作整个数组.
在类中定义__slots__属性之后,实例不能再有__slots__中所列名称之外的其他属性.这只是一个副作用,
不是__slots__存在的真正原因.不要使用__slots__属性禁止类的用户新增实例属性.__slots__是用于优化的,不是为了约束程序员
如果把"__dict__"这个名称添加到__slots__中,实例会在元组中保存各个实例的属性,此外还支持动态创建属性,这些属性存储在常规的__dict__中.当然,把__dict__添加到__slots__可能完全违背了出中,
这个取决于各个实例的静态属性和动态属性的数量及其用法.
此外,注意__weakref__属性,为了让对象支持弱引用,必须有这个属性.用户定义的类中默认就有__weakref__属性.可是,
如果类中定义了__slots__属性,而且想把实例作为弱引用的目标,那么要把__weakref__添加到__slots__中
__slots__属性有些需要注意的地方,而且不能滥用,不能使用它限制用户赋值的属性.
处理列表数据时__slots__属性最有用,例如模式固定的数据库记录,以及特大型数据集(NumPy库)
数据分析库pandas,处理非数值数据,而且能导入/导出很多不同的列表数据格式

__slots__的问题
每个子类都要定义__slots__属性,因为解释器会忽略继承的__slots__属性
实例只能拥有__slots__中列出的属性,除非把'__dict__'加入__slots__中
如果不把__weakref__加入__slots__,实例就不能作为弱引用的目标

9.9 覆盖类属性
类属性可以为实例属性提供默认值
如果为不存在的实例属性赋值,会新建实例属性(类似局部变量)
"""
# 示例,自定义格式代码p,格式化向量为极坐标向量:格式说明符最后一位为p时,输出为极坐标格式
# 示例9-13 设定从类中继承的typecode属性,自定义一个实例属性
# from vector2d_v0 import Vector2d
# v1 = Vector2d(1.1, 2.2)
# dumpd = bytes(v1)
# print(dumpd)
# print(len(dumpd))
# v1.typecode = 'f'
# dumpf = bytes(v1)
# print(dumpf)
# print(len(dumpf))
# print(Vector2d.typecode)
"""
9.10 本章小结
如何使用特殊方法和约定的结构,定义行为良好且符合Python风格的类
所有用于获取字符串和字节序列表示形式的方法:__repr__,__str__,__format__和__bytes__
把对象转换成数字的几个方法:__abs__,__bool__和__hash__
用于测试字节序列转换和支持散列(连同__hash__方法)的__eq__运算符
为了转换成字节序列,备选构造方法,即Vector2d.frombytes(),
@classmethod和@staticmethod
格式规范微语言是可扩展的,实现__format__方法,对提供内置函数format(obj, format_spec)的format_spec,或者提供给
str.format方法的'{:<<format_spec>>}'位于代换字段中的<<format_spec>>做简单的解析
为了把Vector2d实例变成可散列的,先让他们不可变,至少要把x和y设为私有属性,再议只读特性公开,以防意外修改他们.
随后实现__hash__方法,使用推荐的异或运算符计算实例属性的散列值
使用__slots__属性节省内存,
通过访问实例属性覆盖类属性
"""