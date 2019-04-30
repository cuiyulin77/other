# coding=utf-8

import time
import os

while True:
    os.system("scrapy crawl beiqingwang")
    os.system("scrapy crawl wangyi_neimenggu")
    os.system("scrapy crawl xinjingbao")
    os.system("scrapy crawl xinlangneimenggu")
    os.system("scrapy crawl neimengguoxinwenwang")
    time.sleep(30000)
