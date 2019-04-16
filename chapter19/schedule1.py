# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/16 14:46
# @Author   : tangky
# @Site     : 
# @File     : schedule1.py
# @Software : PyCharm

# 示例19-9:访问保存在shelve.Shelf对象中的OSCON日程数据
import warnings
import osconfeed

DB_NAME = 'schedule1_db'
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)  # 2.使用关键字参数传入的属性构建实例的常用简单方式,前提是类中没有设置__slots__属性


def load_db(db):
    raw_data = osconfeed.load()  # 3.如果本地没有副本,从网上下载JSON数据与
    warnings.warn('loading' + DB_NAME)
    for collections, rec_list in raw_data['Schedule'].items():  # 4.迭代集合
        record_type = collections[:-1]  # 5.record_type的值是去掉尾部's'后的集合名(events-->event)
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])  # 6.使用record_type和'serial'字段构成key
            record['serial'] = key  # 7.把'serial'字段的值设为完整的键
            db[key] = Record(**record)  # 8.构建Record实例,存储在数据库中的可以键名下


if __name__ == '__main__':
    import shelve

    db = shelve.open(DB_NAME)  # 1.shelve.open函数打开现有的数据库文件,或者新建一个
    if CONFERENCE not in db:  # 2.判断数据库是否填充的简便方法:检查某个已知的键是否存在;
        load_db(db)  # 3.如果数据库时空的,调用loa_db(db),加载数据
    speaker = db['speaker.3471']  # 4.获取一条speaker记录
    print(type(speaker))  # 5.Record类实例
    print(speaker.name, speaker.twitter)  # 6.各个Record实例都有一系列自定义属性,对应JSON中的字段
    db.close()  # 7.一定要关闭shelve.Shelf对象.如果可以,使用with块
# 在某些应用中,Record类可能要处理不能作为属性名使用的键