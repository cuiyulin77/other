# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import *
import re

class WbUserPipeline(object):
    def process_item(self, item, spider):
        return item


class DBPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = connect(
            # host='47.92.77.18',
            host='192.168.3.15',
            # host='127.0.0.1',
            db='spider',
            user='root',
            # password='admin8152', # 生产服务器
            password='root',
            port=3306,
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # 获取情感分类
        try:
            # 插入数据
            print("*"*100)
            user_id = re.match(r'https\:\/\/m\.weibo\.cn\/u\/(\d+)\?uid.*', item['user_url']).group(1)
            print('user_id',user_id)
            self.cursor.execute(
                "INSERT INTO weibo_user(id,summary,user_name,user_id,user_url,fans,followers,get_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                ('0', str(item['summary']),str(item['user_name']),
                 str(user_id),
                 str(item['user_url']),
                 str(item['fans']),
                 str(item['followers']),
                 str(item['get_time'])),

            )
            self.connect.commit()
            print('mysql一条数据插入成功')
        except Exception as e:
            # 出现错误时打印错误日志
            print(e)
        return item


