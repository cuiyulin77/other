# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import *
import datetime
import time

class TopsPipeline(object):
    def process_item(self, item, spider):
        return item

class DBPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = connect(
            host='47.92.166.26',
            # host='192.168.3.15',
            db='xuanyuqing',
            user='root',
            password='admin8152', # 生产服务器
            # password='root',
            port=3306,
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        '''

        top_type = scrapy.Field()
        top_title = scrapy.Field()
        url = scrapy.Field()
        hot_value = scrapy.Field()
        media = scrapy.Field()

        top_num = scrapy.Field()

        '''

        hisdate = datetime.date.today()

        # 获取整点时间
        unit = 3600
        cur_time = int(time.time())
        hour_stamp = cur_time - (cur_time % unit)
        timeArray = time.localtime(hour_stamp)
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # print(otherStyleTime)
        try:
            # 插入数据
            self.cursor.execute(
                "INSERT INTO tops (id,top_type,top_title,url,hot_value,media,top_num,create_time,hisdate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                ('0', str(item['top_type']),
                 str(item['top_title']),
                 str(item['url']),
                 str(item['hot_value']),
                 item['media'],
                 item['top_num'],
                 create_time,
                 str(hisdate),
                 # item['summary']

                 )
            )
            self.connect.commit()
            print('mysql一条数据插入成功')
        except Exception as e:
            # 出现错误时打印错误日志
            print('mysql 错误',e)
        return item