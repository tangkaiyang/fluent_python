# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/14 16:54
# @Author   : tangky
# @Site     : 
# @File     : flags_threadpool.py
# @Software : PyCharm

# 示例17-3 flags_threadpool.py: 使用futures.ThreadPoolExecutor类实现多线程下载的脚本
from concurrent import futures
from flags import save_flag, get_flag, show, main

MAX_WORKERS = 20


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    # 设定工作的线程数量:使用允许的最大值与要处理的数量之间较小的那个值,以免创建多余的线程
    workers = min(MAX_WORKERS, len(cc_list))
    # 使用工作线程数实例化ThreadPoolExecutor类,executor.__
    # exit__方法会调用executor.shutdown(wait=True)方法,
    # 它会在所有线程都执行完毕前阻塞线程
    with futures.ThreadPoolExecutor(workers) as executor:
        # map方法的作用域内置的map函数类似,不过download_one函数会在多个线程中并发调用;
        # map方法返回一个生成器,因此可以迭代,获取各个函数返回的值
        res = executor.map(download_one, sorted(cc_list))

    return len(list(res))


if __name__ == '__main__':
    main(download_many())
