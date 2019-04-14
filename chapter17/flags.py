# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/4/14 16:36
# @Author   : tangky
# @Site     : 
# @File     : flags.py
# @Software : PyCharm


# 示例17-2 flags.py: 依序下载的脚本;另外两个脚本会重用其中几个函数
import os
import time
import sys

import requests

POP20_CC = ('CN IN US ID BR PK NG BD RU JP'
            'MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = 'downloads/'


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content


def show(text):  # 显示一个字符串,然后刷新sys.stdout,这样才能在一行消息中看到进度.在Python中得这么做,因为正常情况下,遇到换行才会刷新stdout缓冲
    print(text, end='   ')
    sys.stdout.flush()


def download_many(cc_list):
    for cc in sorted(cc_list):
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')

    return len(cc_list)


def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many)
