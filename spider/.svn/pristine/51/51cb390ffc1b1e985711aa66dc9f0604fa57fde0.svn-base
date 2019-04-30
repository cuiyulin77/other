# -*- coding: utf-8 -*-s
import os
import pymysql
import time

while True:
    connect = pymysql.connect(
        host='47.92.166.26',
        # host='192.168.3.15',
        db='xuanyuqing',
        user='root',
        password='admin8152',  # 生产服务器
        # password='root',
        port=3306,
        charset='utf8'
    )
    cursor = connect.cursor()
    cursor.execute("select create_time from tops where id=(select max(id) from tops)")
    result = cursor.fetchone()[0]
    print('最后更新时间',result)

    # 获取整点时间
    unit = 3600
    cur_time = int(time.time())
    hour_stamp = cur_time - (cur_time % unit)
    timeArray = time.localtime(hour_stamp)
    # print(timeArray)
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    # 如果现在整点大于最后更新的整点,就进行更新
    if create_time > str(result):
        print('现在进行更新',create_time)
        os.system('scrapy crawl weibo_top')
        os.system('scrapy crawl baidu_top')
        os.system('scrapy crawl zhihu_top')

    time.sleep(300)
