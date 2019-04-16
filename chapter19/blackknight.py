# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/16 10:48
# @Author   : tangky
# @Site     : 
# @File     : blackknight.py
# @Software : PyCharm

# 示例19-26 blackknight.py:灵感来自电影<<巨蟒与圣杯>>中黑衣骑士角色


class BlackKnight:

    def __init__(self):
        self.members = ['an arm', 'another arm',
                        'a leg', 'another leg']
        self.phrases = ["'Tis but a scratch.",
                        "It's just a flesh wound.",
                        "I'm invincible!",
                        "All right, we'll call it a draw."]

    @property
    def member(self):
        print('next member is:')
        return self.members[0]

    @member.deleter
    def member(self):
        text = 'BLACK KNIGHT (loses {})\n-- {}'
        print(text.format(self.members.pop(0), self.phrases.pop(0)))


if __name__ == '__main__':
    knight = BlackKnight()
    print(knight.member)
    del knight.member
    del knight.member
    del knight.member
    del knight.member
"""
在不适用装饰器的经典调用句法中,fdel参数用于设置删除函数.
例如,在BlackKnight类的定义体中可以像下面这样创建member特性:
member = property(member_getter, fdel=member_deleter)
如果不使用特性,可以实现底层特殊的__delattr__方法处理删除属性的操作,
"""
