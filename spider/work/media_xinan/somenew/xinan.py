# coding=utf-8

import time
import os

while True:
    os.system("scrapy crawl sichuanxinwenwang")
    os.system("scrapy crawl sichanzaixian")
    os.system("scrapy crawl xingyizhichuang")
    os.system("scrapy crawl xinlangsichuan")
    os.system("scrapy crawl yunnanwang")
    os.system("scrapy crawl yunnanxinxigang")
    os.system("scrapy crawl yunshiwang")
    time.sleep(30000)
