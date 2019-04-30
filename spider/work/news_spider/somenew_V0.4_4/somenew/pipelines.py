# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import *
import datetime

class SomenewPipeline(object):
    def process_item(self, item, spider):
        return item


class DBPipeline(object):
    def __init__(self):
        # 连接数据库
        self.client = MongoClient(
            host='127.0.0.1',
            port=27017,
        )
        self.db = self.client.spider

    def process_item(self, item, spider):
        try:
            # 插入数据
            self.db.article.insert_one(
                {'_id': item['article_id'], 'title': item['title'], 'content': item['content'], 'url': item['url'],
                 'media': item['media'], 'publish_time': item['time'], 'create_time': datetime.datetime.strptime(item['create_time'], '%Y/%m/%d %H:%M:%S')})
            print('一条数据插入成功')
        except Exception as e:
            # 出现错误时打印错误日志
            print(e)
        return item
