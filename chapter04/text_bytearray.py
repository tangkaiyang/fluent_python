# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/1 19:15
# @Author   : tangky
# @Site     : 
# @File     : text_bytearray.py
# @Software : PyCharm

"""
第4章 文本和字节序列
Python3明确区分了人类可读的文本字符串和原始的字节序列.
Unicode字符串,二进制序列,二者之间转换时使用的编码
字符,码位和字节表述
bytes,bytearray和memoryview等二进制序列的独特特性
全部Unicode和陈旧字符集的编解码器
避免和处理编码错误
处理文本文件的最佳实践
默认编码的陷阱和标志I/O的问题
规范化Unicode文本,进行安全的比较
规范化,大小写折叠和暴力移除音调符号的实用函数
使用locale模块和PyUCA库正确地排序Unicode文本
Unicode数据库中的字符元数据
能处理字符串和字节序列的双模式API

4.1 字符问题
一个字符串是一个字符序列.
"字符"的最佳定义是Unicode字符.
Python3的str对象中获取的元素是Unicode字符,

Unicode标准把字符的标识和具体的字节表述进行了如下的明确区分:
字符的标识,即码位,是0~1 114 111的数字(十进制),在Unicode标准中以4~6个
十六进制数字表示,而且加前缀"U+".例如字母A的码位是U+0041
字符的具体表述取决于所用的编码.编码是在码位和字节序列之间转换时使用的算法.
在UTF-8编码中,A(U+0041)的码位编码成单个字节\x41,在UTF-16LE编码中编码成
两个字节\x41\x00
把码位转换成字节序列的过程是编码;把字节序列转换成码位的过程是解码
"""
# # 示例4-1 编码和解码
# s = 'café'
# print(len(s))
# b = s.encode('utf8')    # str 编码成 bytes,以b开头
# print(b)
# print(len(b))
# print(b.decode('utf8')) # bytes 解码成 str
"""
.decode()和.encode()的区别,可以把字节序列想成晦涩难懂的机器磁芯转储,
把Unicode字符串想成"人类可读"的文本.那么,把字节序列变成人类可读的文本字符串
就是解码,把字符串变成用于存储或传输的字节序列就是编码

4.2 字节概要
Python内置了两种基本的二进制序列类型:
bytes类型和可变bytearray类型.
bytes或bytearray对象的各个元素是介于0~255(含)之间的整数,
然而,二进制序列的切片始终是同一类型的二进制序列,包括长度为1的切片
"""
# 示例4-2 包含5个字节的bytes和bytearray对象
# cafe = bytes('café', encoding='utf_8')  # bytes从str指定编码构建
# print(cafe)
# print(cafe[0])  # 各个元素都是range(256)内的整数
# print(cafe[:1])  # bytes对象的切片还是bytes对象,即使只有一个字节的切片
# cafe_arr = bytearray(cafe)
# print(cafe_arr)  # bytearray对象没有字面量句法,而是以bytearray()和字节序列字面量参数的形式显示
# print(cafe_arr[-1:])  # bytearray对象的切片还是bytearray对象
"""
s[0]==s[:1]只对str这个序列类型成立.
对其他各个序列类型来说,s[i]返回一个元素,而s[i:i+1]返回一个相同类型的序列,
里面是s[i]元素
虽然二进制序列其实是整数序列,但是他们的字面量表示法表明其中有ASCII文本.
因此,各个字节的值可能会使用下列三种不同的方式显示:
    可打印的ASCII范围内的字节(从空格到~),使用ASCII字符本身
    制表符,换行符,回车符和\对应的字节,使用转义序列\t,\n,\r和\\
    其他字节的值,使用十六进制转义序列(例如,\x00是空字节)
除了格式化方法(format和format_map)和几个处理Unicode数据的方法(包括
casefold,isdecimal,isidnetifier,isnumeric,isprintable和encode)之外,
str类型的其他方法都支持bytes和bytearray类型.
这意味着,我们可以使用熟悉的字符串方法处理二进制序列,
如endswith,replace,strip,translate,upper等,
只有少数几个其他方法的参数是bytes对象,而不是str对象.
此外,如果正则表达式编译自二进制序列而不是字符串,re模块中的正则表达式函数也能处理二进制序列.
二进制序列有个类方法是str没有的,名为fromhex,它的作用是
解析十六进制数字对(数字之间的空格是可选的),构建二进制序列:
"""
# print(bytes.fromhex('31 4B CE A9'))
"""
构建bytes和bytearray实例还可以调用各自的构造方法,传入下述参数:
    一个str对象和一个encoding关键字参数
    一个可迭代对象,提供0~255之间的数值
    一个实现了缓冲协议的对象(如bytes,bytearray,memoryview,array.array);此时,把源对象中的字节序列复制到新建的二进制序列中.
使用缓冲类对象构建的二进制序列是一种低层操作,可能涉及类型转换.
"""
# # 示例4-3 使用数组中的原始数据初始化bytes对象
# import array
#
# numbers = array.array('h', [-2, -1, 0, 1, 2])  # 指定类型代码h,短整数(16位)
# octets = bytes(numbers)  # octets保存组成numbers的字节序列的副本
# print(octets)  # 这些是表示那5个短整数的10个字节
"""
使用缓冲类对象创建bytes或bytearray对象时,始终赋值源对象中的字节序列.
与之相反,memoryview对象允许在二进制数据结构之间共享你内存.
如果想从二进制序列中提取结构化信息,struct模块是重要的工具

结构体和内存视图
struct模块提供了一些函数,把打包的字节序列转换成不同类型字段组成的元组,
还有一些函数用于执行反向转换,把元组转换成打包的字节序列.
struct模块能处理bytes,bytearray和memoryview对象
memoryview类不是用于创建或存储字节序列的,而是共享内存,让你访问其他二进制
序列,打包的数组和缓冲中的数据切片,而无需赋值字节序列,
例如Python Imaging Library(PIL)就是这样处理图像的
"""
# 示例4-4 使用memoryview和struct查看一个GIF图像的首部
# import struct
#
# fmt = '<3s3sHH'  # 结构体格式:<是小字节序,3s3s是两个3字节序列,HH是两个16位二进制整数
# with open('filter.gif', 'rb') as fp:
#     img = memoryview(fp.read())
# header = img[:10]
# print(bytes(header))
# print(struct.unpack(fmt, header))  # 拆包memoryview对象,得到一个元组,包含类型,版本,宽度和高度
# del header  # 删除引用,释放memoryview实例占用的内存
# del img
"""
注意,memoryview对象的切片是一个新的memoryview对象,而且不会赋值字节序列.

4.3 基本的编解码器
Python自带了超过100中编解码器(codec,encoder/decoder),用于在文本和字节之间
相互转换.每个编解码器都有一个名称,如'utf_8',而且经常有几个别名,
如'utf8','utf-8'和'U8'.这些名称可以传给open(),str.encode(),
bytes.decode()等函数的encoding参数.
"""
# 示例4-5 使用3个编解码器编码字符串"El Niño",得到的字节序列差异很大
# for codec in ['latin_1', 'utf_8', 'utf_16']:
#     print(codec, 'El Niño'.encode(codec), sep='\t')
"""
4.4 了解编解码的问题
出现与Unicode有关的错误时,首先要明确异常的类型.
导致编码问题的是UnicodeEncodeError,UnicodeDecodeError,
还是如SyntaxError的其他错误
4.4.1 处理UnicodeEncodeError
多数非UTF编解码器只能处理Unicode字符的一小部分子集.
把文本转换成字节序列时,如果目标编码中没有定义某个字符,就会抛出
UnicodeEncodeError异常,除非把errors参数传给编码方法或函数,对错误进行特殊处理.
"""
# 示例4-6 编码成字节序列:成功和错误处理
# city = 'São Paulo'
# print(city.encode('utf_8'))
# print(city.encode('utf_16'))
# print(city.encode('iso8859_1'))
# # print(city.encode('cp437'))
# print(city.encode('cp437', errors='ignore'))
# print(city.encode('cp437', errors='replace'))  # 无法编码的替换成?
# print(city.encode('cp437', errors='xmlcharrefreplace'))  # 替换成XML实体
"""
编解码器的错误处理方式是可扩展的.
可以为errors参数注册额外的字符串,
方法是把一个名称和一个错误处理函数传给codecs.register_error函数

4.4.2 处理UnicodeDecodeError
不是每一个字节都包含有效的ASCII字符,也不是每一个字符序列都是有效的UTF-8或者
UTF-16.因此,把二进制序列转换成文本时,如果假设是这两个编码中的一个,遇到无法转换的字节序列时
会抛出UnicodeDecodeError
乱码字符称为鬼符(gremlin)或mojibake
"""
# 示例4-7 把字节序列解码成字符串:成功和错误处理
# octets = b'Montr\xe9al'
# print(octets.decode('cp1252'))
# print(octets.decode('iso8859_7'))
# print(octets.decode('koi8_r'))
# print(octets.decode('utf_8', errors='replace')) # 替换为�
# print(octets.decode('utf_8'))

"""
4.4.3 使用预期之外的编码加载模块是抛出SyntaxError
Python3默认使用UTF-8编码源码,Python2(从2.5开始)则默认使用ASCII.
如果加载的.py模块中包含UTF-8之外的数据,而且没有声明编码,会得到类似:
SyntaxError: Non-UTF-8 code starting....
解决:文件顶部# coding: cp1252

4.4.4 如何找出字节序列的编码
如何找出字节序列的编码?不能,
统一字符编码侦测包Chardet,能识别所支持的30中编码.
Chardet是一个Python库,可以在程序中使用,不过它也提供了命令行工具chardetect.
如:chardetect 04-text-byte.asciidoc

4.4.5 BOM: 有用的鬼符
BOM,即字节序标记(byte-order-mark),指明编码时使用Intel CPU的小字节序.
UTF-8的一大优势是,不管设备使用哪种字节序,生成的字节序列始终一致,
因此不需要BOM.

4.5 处理文本文件
处理文本的最佳实践"Unicode三明治":
要尽早把输入(例如读取文件时)的字节序列解码成字符串.
这种三明治中的"肉片"是程序的业务逻辑,在这里只能处理字符串对象.
在其他处理过程中,一定不能编码或解码.
对输出来说,则要尽量晚地把字符串编码成字节序列.
Python3内置的open函数在会在读取文件时做必要的解码,以文本模式写入文件时
还会做必要的编码,所以调用my_file.read()方法得到的以及传给my_file.write(text)方法的都是字符串对象
"""
# 示例4-9 一个平台上的编码问题(可能会发生,也可能不会)
# open('cafe.txt', 'w', encoding='utf_8').write('café')
# print(open('cafe.txt').read())
"""
如果打开文件是为了写入,但是没有指定编码参数,会使用区域和设置中的默认编码,
而且使用那么编码也能正确读取文件.但是,如果脚本要生成文件,
而字节的内容取决于平台或同一平台中的区域设置,那么就可能导致兼容问题
需要在多台设备中或多种场合下运行的代码,一定不能依赖默认编码.
打开文件时始终应该明确传入encoding=参数,因不同的设备使用的默认编码可能不同,
"""
# 实例4-10 仔细分析在Windows中运行的实例4-9,找出并修正问题,输入输出字符数不一致
# fp = open('cafe.txt', 'w', encoding='utf_8')
# print(fp)
# fp.write('café')
# fp.close()
# import os
# os.stat('cafe.txt').st_size
# fp2 = open('cafe.txt')
# print(fp2)
# print(fp2.encoding)
# print(fp2.read())
# fp3 = open('cafe.txt', encoding='utf_8')
# print(fp3)
# print(fp3.read())
# fp4 = open('cafe.txt', 'rb')    # 返回的是BufferReader而不是TextIOWrapper
# print(fp4)
# print(fp4.read())
"""
除非相判断编码,否则不要在二进制模式中打开文件;
即使如此,也应该用Chardet,
常规代码只应该使用二进制模式打开二进制文件,如光栅图像

编码默认值:一团糟
"""
# 示例4-11 探索编码默认值
import sys, locale
expressions = """
    locale.getpreferredencoding()
    type(my_file)
    my_file.encoding
    sys.stdout.isatty()
    sys.stdout.encoding
    sys.stdin.isatty()
    sys.stdin.encoding
    sys.stderr.isatty()
    sys.stderr.encoding
    sys.getdefaultencoding()
    sys.getfilesystemencoding()
"""
my_file = open('dummy', 'w')
for expression in expressions.split():
    value = eval(expression)
    print(expression.rjust(30), '->', repr(value))
# chcp输出当前控制台激活的代码页:
# 把输出重定向到文件 python .py > encodings.log
# locale.getpreferredencoding()返回的编码是最重要的:
# 这是打开文件的默认编码,也是重定向到文件的sys.stdout/stdin/stderr的默认编码
# 别依赖默认值
"""
4.6 为了正确比较而规范化Unicode字符串
因为Unicode有组合字符(变音符号和符加到前一个字符上的记号,打印时作为一个整体),所以字符串比较起来很复杂.
例如"café"这个词可以使用两种方式构成,分别有4个和5个码位,但是结果完全一样:
s1 = 'café'
s2 = 'cafe\u0301'
s1, s2 --> ('café', 'café')
len(s1), len(s2) --> (4, 5)
s1 == s2 --> False
U+0301是COMBINING ACUTE ACCENT,加在"e"后面得到"é".
在Unicode标准中,上述这样的序列叫做"标准等价物"(canonical equivalent),
应用程序应该把他们视作相同的字符.但是,Python所看到的的是不同的码位序列,
因此判定两者不相等.
这个问题的解决方案是使用unicodedata.normalize函数提供的Unicode规范化.
这个函数的第一个参数是这4个字符串中的一个:
'NFC', 'NFD', 'NFKC' 和'NFKD'
NFC(Normalization Form C)使用最少的码位构成等价的字符串,而NFD把
组合字符分解成基字符和单独的组合字符.这两种规范化方式都能让比较行为符合预期:
"""
# from unicodedata import normalize
# s1 = 'café' # 把e和重音符组合在一起
# s2 = 'cafe\u0301'   # 分解成e和重音符
# print(len(s1), len(s2))
# print(len(normalize('NFC', s1)), len(normalize('NFC', s2)))
# print(len(normalize('NFD', s1)), len(normalize('NFD', s2)))
# print(normalize('NFC', s1) == normalize('NFC', s2))
# print(normalize('NFD', s1) == normalize('NFD', s2))
"""
用户输入的文本默认是NFC形式.不过安全起见,保存文本之前,最好使用normalize('NFC', user_text)清洗字符串

"""