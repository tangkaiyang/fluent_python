# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/17 10:50
# @Author   : tangky
# @Site     : 
# @File     : descriptorkinds.py
# @Software : PyCharm

# 示例20-8 几个简单的类,用于研究描述符的覆盖行为
### 辅助函数,仅用于显示 ###
def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]


def display(obj):
    cls = type(obj)
    if cls is type:
        return '<class {}>'.format(obj.__name__)
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return '<{} object>'.format(cls_name(obj))


def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print('-> {}.__{}__({})'.format(cls_name(args[0]), name, pseudo_args))


### 对这个示例更重要的类 ###
class Overriding:  # 1.有__get__和__set__方法的典型覆盖型描述符
    """也称数据描述符或强制描述符"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)  # 2.各个描述符的每个方法都调用了print_args函数

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:  # 3.没有__get__方法的覆盖型描述符
    """没有``__get__``方法的覆盖型描述符"""

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:  # 4.没有__set__方法,所以这是非覆盖型描述符
    """也称非数据描述符或遮盖型描述符"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:  # 5.托管类,使用各个描述符类的一个实例
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):  # 6.spam方法放在这里是为了对比,因为方法也是描述符
        print('-> Managed.spam({})'.format(display(self)))


if __name__ == '__main__':
    # 示例20-9 覆盖型描述符的行为,
    # obj = Managed()  # 1.
    # obj.over  # 2.触发描述符的__get__方法,第二个参数的值是托管实例obj
    # Managed.over  # 3.Manage.over触发描述符的__get__方法,第二个参数(instance)的值是None
    # obj.over = 7  # 4.赋值,触发描述符的__set__方法,最后一个参数的值是7
    # obj.over  # 5.读取obj.ove,仍会触发描述符的__get__方法
    # obj.__dict__['over'] = 8  # 6.跳过描述符,直接通过obj.__dict__属性设值
    # print(vars(obj))  # 7.确认值在obj.__dict__属性中,在over键名下
    # obj.over  # 8.即使是名为over的实例属性,Managed.over描述符仍会覆盖读取obj.over这个操作

    # 示例20-10 没有__get__方法的覆盖型描述符
    # print(obj.over_no_get)  # 1.这个覆盖型描述符没有__get__方法,从类中获取描述符实例
    # print(Managed.over_no_get)  # 2.直接从托管类中读取描述符实例
    # obj.over_no_get = 7  # 3.赋值会触发描述符的__set__方法
    # print(obj.over_no_get)  # 4.__set__方法没有修改属性,所以仍获取托管类中的描述符实例
    # obj.__dict__['over_no_get'] = 9  # 5.通过实例的__dict__属性设置名为over_no_get的实例属性
    # print(obj.over_no_get)  # 6.over_no_get实例属性会遮盖描述符,但是只有读操作是如此
    # obj.over_no_get = 7  # 7.为obj.over_no_get赋值,仍然经过描述符的__set__方法处理
    # print(obj.over_no_get)  # 8.读值时,只要有同名的实例属性,描述符就会被遮盖

    # 示例20-11 非覆盖型描述符的行为
    # obj = Managed()
    # obj.non_over  # 1.触发描述符的__get__方法,第二个参数的值是obj
    # obj.non_over = 7  # 2.非覆盖型描述符,没有干涉赋值操作的__set__方法
    # print('3', obj.non_over)  # 3.obj的non_over实例属性,覆盖了Managed类的同名描述符属性
    # print('4', Managed.non_over)  # 4.Managed.non_over描述符依然存在,会通过类截获这次访问
    # del obj.non_over  # 5.删除实例属性non_over
    # print('6', obj.non_over)  # 6.触发类中描述符的__get__方法;第二个参数的值是托管实例

    # 示例20-12 通过类可以覆盖任何描述符
    # obj = Managed()  # 1.
    # Managed.over = 1  # 2.覆盖类中的描述符属性
    # Managed.over_no_get = 2
    # Managed.non_over = 3
    # print(obj.over, obj.over_no_get, obj.non_over)  # 3.描述符真不见了

    # 示例20-13 方法是非覆盖型描述符
    obj = Managed()
    print(obj.spam)  # 1.obj.spam获取的是绑定对象方法
    print(Managed.spam)  # 2.Managed.spam获取的是函数
    obj.spam = 7  # 3.如果为obj.spam赋值,会遮盖类属性,导致无法通过obj实例访问spam方法
    print(obj.spam)
