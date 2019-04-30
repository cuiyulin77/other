# coding=utf-8

import os
from scrapy.cmdline import execute

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy','crawl','tianya'])




