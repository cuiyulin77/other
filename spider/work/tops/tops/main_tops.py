# coding=utf8
from scrapy.cmdline import execute

import sys
import os

# while True:
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# execute(['scrapy','crawl','weibo_top'])
#
#
# execute(['scrapy','crawl','baidu_top'])

execute(['scrapy','crawl','zhihu_top'])
