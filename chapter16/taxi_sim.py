# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/14 14:02
# @Author   : tangky
# @Site     : 
# @File     : taxi_sim.py
# @Software : PyCharm
import collections
import queue

DEPARTURE_INTERVAL = 5
Event = collections.namedtuple('Event', 'time proc action')


class Simulator:
    """
    Simulator类的主要数据结构
    self.events
        PriorityQueue对象,保存Event实例.元素可以放进(使用put方法)PriorityQueue对象中,
        然后按item[0](即Event对象的time属性)依序取出(使用get方法)
    self.procs
        一个字典,把出租车的编号映射到仿真过程中激活的进程(表示出租车的生成器对象).
        这个属性会绑定前面所示的taxis字典副本
    优先队列是离散事件仿真系统的基础构建:创建时间的顺序补丁,放入这种队列之后,可以按照各个
    事件排定的时间顺序取出.
    Simulator.run方法实现的算法:
        (1)迭代表示各辆出租车的进程
            a.在各辆出租车上调用next()函数,预激协程.这样会产生各辆出租车的第一个时间
            b.把各个事件放入Simulator类的self.events属性(队列)中
        (2)满足sim_time < end_time条件时,运行仿真系统的主循环
            a.检查self.events属性是否为空;如果为空,跳出循环.
            b.从self.events中获取当前事件(current_event),即PriorityQueue对象中时间值
            最小的Event对象
            c.显示获取的Event对象
            d.获取current_event的time属性,更新仿真时间
            e.把事件发给current_event的proc属性标识的协程,产出下一个事件(next_event)
            f.把next_event添加到self.events队列中,排定next_event
    """

    def __init__(self, procs_map):
        self.events = queue.PriorityQueue()  # 1.保存排定事件的PriorityQueue对象,按时间正向排序
        self.procs = dict(
            procs_map)  # 2.获取的procs_map参数是一个字典(或其他映射),可是又从中构建一个字典,创建本地副本,因为在仿真过程中,出租车回家后会从self.procs属性中移除,而我们不想修改用户传入的对象

    def run(self, end_time):  # 1.
        """排定并显示时间,直到时间结束"""
        # 排定各辆出租车的第一个事件
        for _, proc in sorted(self.procs.items()):  # 2.
            first_event = next(proc)  # 3.
            self.events.put(first_event)  # 4.
        # 这个仿真系统的主循环
        sim_time = 0  # 5.
        while sim_time < end_time:  # 6.
            if self.events.empty():  # 7.
                print('*** end of events ***')
                break
            current_event = self.events.get()  # 8.
            sim_time, proc_id, previous_action = current_event  # 9.
            print('taxi:', proc_id, proc_id * ' ', current_event)  # 10.
            active_proc = self.procs[proc_id]  # 11.
            next_time = sim_time  # + compute_duration(previous_action) # 12.
            try:
                next_event = active_proc.send(next_time)  # 13.
            except StopIteration:
                del self.procs[proc_id]  # 14.
            else:
                self.events.put(next_event)  # 15.
        else:  # 16.
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))


# 示例16-20 taxi_process协程实现各辆出租车的活动
def taxi_process(ident, trips, start_time=0):  # 1
    """
    每次改变状态时创建事件,把控制权让给仿真器
    1)每辆出租车调用一次taxi_process函数,创建一个生成器对象,表示各辆出租车的运营过程.
    ident是出租车的编号;trips是出租车回家之前的行程数量;start_time是出租车离开车库的时间
    2)产出的第一个Event是'leave garage'.执行到这一行时,协程会暂停,让仿真主循环着手处理排定的下一个事件.需要重新激活这个进程时,主循环会发送(使用send方法)当前的仿真时间,赋值给time
    3)每次行程都会执行一遍这个代码块
    4)产出一个Event实例,表示拉到乘客了.协程在这里暂停.需要重新激活这个协程时,主循环会发送(使用send方法)当前的时间
    5)产出一个Event实例,表示乘客下车了.协程在这里暂停,等待主循环发送时间,然后重新激活
    6)指定的行程数量完成后,for循环结束,最后产出的'going home'事件.此时,协程最后一次暂停
    仿真主循环发送时间后,协程重新激活;不过,这里没有把产出的值赋值给变量,因为用不到
    7)协程执行到最后时,生成器对象抛出StopIteration异常

    """
    time = yield Event(start_time, ident, 'leave garage')  # 2 garage:车库
    for i in range(trips):  # 3
        time = yield Event(time, ident, 'pick up passenger')  # 4
        time = yield Event(time, ident, 'drop off passenger')  # 5

    yield Event(time, ident, 'going home')  # 6
    # 出租车进程结束


# 示例16-21 驱动taxi_process协程
# taxi = taxi_process(ident=13, trips=2, start_time=0)
# print(next(taxi))
# print(taxi.send(_.time + 7))
# print(taxi.send(_.time + 23))
# print(taxi.send(_.time + 5))
# print(taxi.send(_.time + 48))
# print(taxi.send(_.time + 1))
# print(taxi.send(_.time + 10))
# if __name__ == '__main__':
# taxis = {i: taxi_process(i, i + 1) * 2, i * DEPARTURE_INTERVAL)
#     for i in range(num_taxis)}
# sim = Simulator(taxis)
