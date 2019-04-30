# coding=utf-8

import time
import os

while True:

    # 是在爬虫运行完毕之后开始计时
    os.system("scrapy crawl huanqiu")
    print("0" * 100)
    time.sleep(10)  # 休息 运行下一个爬虫

    os.system("scrapy crawl pengpai")
    print("1" * 100)
    time.sleep(10)  # 休息 运行下一个爬虫


    os.system("scrapy crawl qqnews")
    print("2" * 100)
    time.sleep(10)  # 休息 运行下一个爬虫

    os.system("scrapy crawl sina")
    print("3" * 100)
    time.sleep(10)  # 休息 运行下一个爬虫

    # os.system("scrapy crawl weibo")
    # print("3" * 100)
    # time.sleep(10)  # 休息 运行下一个爬虫

    os.system("scrapy crawl toutiao")
    print("3" * 100)
    time.sleep(10)  # 休息 运行下一个爬虫

    os.system("scrapy crawl wangyi_zhejiang")
    print("3" * 100)
    time.sleep(10)  # 休息 运行下一个爬虫

    os.system("scrapy crawl xinjingbao")
    print("3" * 100)
    time.sleep(10)  # 休息 运行下一个爬虫

    os.system("scrapy crawl xinlangshanxi")
    print("3" * 100)
    time.sleep(10)  # 休息 运行下一个爬虫

