# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class BlogPipeline(object):
    def process_item(self, item, spider):
        return item

class DBPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='localhost',
            db='spider',
            user='root',
            passwd='root',
            port=3306,
            charset='utf8',
            )

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 插入数据
            self.cursor.execute(
                "INSERT INTO blog (article_id,title,content,url,media,publish_time,create_time,blogger_name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (str(item['article_id']),
                 str(item['title']),
                 str(item['content']),
                 str(item['url']),
                 str(item['media']),
                 item['publish_time'],
                item['create_time'],
                 item['blogger_name']))

            # 提交sql语句
            self.connect.commit()

        except Exception as e:
            # 出现错误时打印错误日志
            print(e)
        return item