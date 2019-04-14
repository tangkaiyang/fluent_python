# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/14 17:22
# @Author   : tangky
# @Site     : 
# @File     : flags_threadpool_ac.py
# @Software : PyCharm


# 示例17-4 flags_threadpool_ac.py: 把download_many函数中的executor.map方法换成executor.submit方法和futures.as_completed函数

from concurrent import futures
from flags import save_flag, get_flag, show, main

MAX_WORKERS = 20


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    # 1.使用人口最多的5个国家
    cc_list = cc_list[:5]
    # 2.把max_worker硬编码为3,以便在输出中观察待完成的期物
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        # 3.按照字母表顺序迭代国家代码,明确表明输出的顺序与输入一致
        for cc in sorted(cc_list):
            # 4.executor.submit方法排定可调用对象的执行时间,然后返回一个期物,表示这个待执行的操作
            future = executor.submit(download_one, cc)
            # 5.存储各个期物,后面转给as_completed函数
            to_do.append(future)
            msg = 'Scheduled for {}: {}'
            # 6.显示一个消息,包含国家代码和相对应的期物.
            print(msg.format(cc, future))

        results = []
        # 7.as_completed函数在期物运行结束后产出期物
        for future in futures.as_completed(to_do):
            # 8.获取该期物的结果
            res = future.result()
            msg = '{} result: {!r}'
            # 9.显示期物及其结果
            print(msg.format(future, res))
            results.append(res)
    return len(results)
if __name__ == '__main__':
    main(download_many())
# 注意这个示例中调用future.result()方法绝不会阻塞,因为
# future由as_completed函数产生
"""
# 排定的期物按字母表排序:期物的repr()方法会显示期物的状态:前三个期物的状态是running,因为有三个工作的线程
Scheduled for BR: <Future at 0x100791518 state=running>
Scheduled for CN: <Future at 0x100791710 state=running>
Scheduled for ID: <Future at 0x100791a90 state=running>
# 后两个期物的状态是pending,等待有线程可用
Scheduled for IN: <Future at 0x101807080 state=pending>
Scheduled for US: <Future at 0x101807128 state=pending>
# 这一行里的第一个CN是运行在一个工作线程中的download_one函数输出的,随后的内容是download_many函数输出的
CN <Future at 0x100791710 state=finished returned str> result: 'CN'
# 这里有两个线程输出国家代码,然后主线程中的download_many函数输出第一个线程的结果
BR ID <Future at 0x100791518 state=finished returned str> result: 'BR'
<Future at 0x100791a90 state=finished returned str> result: 'ID'
IN <Future at 0x101807080 state=finished returned str> result: 'IN'
US <Future at 0x101807128 state=finished returned str> result: 'US'
5 flags downloaded in 0.70s
"""