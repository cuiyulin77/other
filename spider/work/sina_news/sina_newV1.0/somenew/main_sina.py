# coding=utf-8

import time
import os

while True:


    os.system("scrapy crawl sina")
    print("*sina*" * 100)
    # time.sleep(10)  # 休息 运行下一个爬虫

    os.system("scrapy crawl toutiao")
    print("toutiao" * 100)
    # time.sleep(10)  # 休息 运行下一个爬虫

