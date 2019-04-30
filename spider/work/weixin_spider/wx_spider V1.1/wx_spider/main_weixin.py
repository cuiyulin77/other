import os
import time

while True:
    os.system("scrapy crawl sogou")
    print('休息'*10)
    time.sleep(10)

