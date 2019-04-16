# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/16 15:28
# @Author   : tangky
# @Site     : 
# @File     : schedule2.py
# @Software : PyCharm

"""
schedule2.py: traversing OSCON schedule data
    >>> import shelve
    >>> db = shelve.open(DB_NAME)
    >>> if CONFERENCE not in db: load_db(db)
    >>> DbRecord.set_db(db)
    >>> event = DbRecord.fetch('event.33950')
    >>> event
    <Event 'There *Will* Be Bugs'>
    >>> event.venue
    <DbRecord serial='venue.1449'>
    >>> event.venue.name
    'Portland 251'
    >>> for spkr in event.speakers:
    ...     print('{0.serial}: {0.name}'.format(spkr))
    ...
    speaker.3471: Anna Ravenscroft
    speaker.5199: Alex Martelli
    >>> db.close()
"""

# BEGIN SCHEDULE2_RECORD
import warnings
import inspect  # 1.inspect模块在load_db函数中使用

import osconfeed

DB_NAME = 'schedule2_db'  # 2.因为要存储几个不同类的实例,所以我们要创建并使用不同的数据库文件;
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):  # 3.
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented


# 一个自定义的异常类型
class MissingDatabaseError(RuntimeError):  # 1.自定义的异常通产格式标志类,没有定义体
    """
    Raised when a database is required but was not set.
    需要数据库但没有指定数据库时抛出
    """


class DbRecord(Record):  # 2.DbRecord类扩展Record类
    __db = None  # 3.__db类属性存储了一个打开的shelve.Shelf数据库引用

    @staticmethod  # 4.set_db是静态方法,一次强调不管调用多少次,效果始终一样
    def set_db(db):
        DbRecord.__db = db  # 5.即使调用Event.set_db(my_db), __db属性仍在DbRecord类中设置

    @staticmethod  # 6.get_db也是静态方法,因为不管怎样调用,返回值始终是DbRecord.__db引用的对象
    def get_db():
        return DbRecord.__db

    @classmethod  # 7.fetch是类方法,因此在子类中易于制定它的行为
    def fetch(cls, ident):
        db = cls.get_db()
        try:
            return db[ident]  # 8.从数据库中获取ident键对应的记录
        except TypeError:
            if db is None:  # 9.如果捕获到TypeError异常,而且db变量的值是None,抛出自定义的异常,说明必须设置数据库
                msg = "database not set; call '{}.set_db(my_db)'"
                raise MissingDatabaseError(msg.format(cls.__name__))
            else:  # 10.否则重新抛出TypeError异常,因为我们不知道怎么处理
                raise

    def __repr__(self):
        if hasattr(self, 'serial'):  # 11.如果记录有serial属性,在字符串表示形式中使用
            cls_name = self.__class__.__name__
            return '<{} serial={!r}>'.format(cls_name, self.serial)
        else:
            return super().__repr__()  # 12.否则,调用继承的__repr__方法


class Event(DbRecord): # 1.Event类扩展DbRecord类

    @property
    def venue(self):
        key = 'venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key) # 2.在venue特性中使用venue_serial属性构建key,然后传给继承自DbRecord类的fetch类方法

    @property
    def speakers(self):
        if not hasattr(self, '_speaker_objs'): # 3.speakers特性检查记录是否有_speakers_objs属性
            spkr_serials = self.__dict__['speakers'] # 4.如果没有,直接从__dict__实例属性中获取'speakers'属性的值,防止无限递归,因为这个特性的公开名称也是speakers
            fetch = self.__class__.fetch # 5.获取fetch类方法的引用
            self._speaker_objs = [fetch('speaker.{}'.format(key))
                                  for key in spkr_serials] # 6.使用fetch获取speakers记录列表,然后赋值给self._speaker_objs
        return self._speaker_objs # 7.返回前面获取的列表

    def __repr__(self):
        if hasattr(self, 'name'): # 8.如果记录有name属性,在字符串表示形式中使用
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)
        else:
            return super().__repr__() # 9.否则,调用继承的__repr__方法


def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        record_type = collection[:-1] # 1.
        cls_name = record_type.capitalize() # 2.把record_type变量的值首字母变成大写,获取可能的类名
        cls = globals().get(cls_name, DbRecord) # 3.从模块的全局作用域中获取那个名称对应的对象;如果找不到对象,使用DbRecord
        if inspect.isclass(cls) and issubclass(cls, DbRecord): # 4.如果获取的对象是类,而且是DbRecord的子类...
            factory = cls # 5....把对象赋值给factory变量.因此,factory的值可能是DbRecord的任何一个子类,具体的只取决于record_type的值
        else:
            factory = DbRecord # 6.否则,把DbRecord赋值给factory变量
        for record in rec_list: # 7.这个for循环创建key,然后保存记录,这与之前一样,不过....
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = factory(**record) # 8....存储在数据库中的对象由factory构建,factory可能是DbRecord类,也可能是根据record_type的值确定的某个子类
