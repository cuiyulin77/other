# coding=utf-8

import time
import os

while True:
    os.system("scrapy crawl guanxixinwenwang")
    os.system("scrapy crawl jinyangwang")
    os.system("scrapy crawl nanfangwang")
    os.system("scrapy crawl shenzhengxinwenwang")
    os.system("scrapy crawl leqingshizhengfu")
    time.sleep(15000)

