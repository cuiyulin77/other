# coding=utf-8

import time
import os

while True:
    # 东方网 杭州新闻网 网易浙江爬虫 温州新闻网 温州政府网 新华报业 扬子晚报 浙江在线 中国新闻网江苏 中国江苏网
    os.system("scrapy crawl anhuiwang")
    os.system("scrapy crawl anhuizaixian")
    os.system("scrapy crawl dongfangwang")
    os.system("scrapy crawl fujianwangluodianshitai")
    os.system("scrapy crawl hangzhouxinwenwang")
    os.system("scrapy crawl nanchangxinwenwang")
    os.system("scrapy crawl wangyi_zhejiang")
    os.system("scrapy crawl wenzhouxinwenwang")
    os.system("scrapy crawl wenzhouxinwenwang2")
    os.system("scrapy crawl xinhuabaoye")
    os.system("scrapy crawl xinlangjiangxi")
    os.system("scrapy crawl yangziwanbao")
    os.system("scrapy crawl zhejiangzaixian")
    os.system("scrapy crawl zhongguoanhuiwang")
    os.system("scrapy crawl zhonguojiangsuwang")
    os.system("scrapy crawl zhongguojiangxiwang")
    os.system("scrapy crawl zhongwangxinwenwngjiangsu")
    time.sleep(15000)
