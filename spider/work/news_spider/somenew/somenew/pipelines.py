# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from somenew.settings import MYSQL_HOST,MYSQL_DBNAME,MYSQL_USER,MYSQL_PASSWD,MYSQL_PORT

class SomenewPipeline(object):
    def process_item(self, item, spider):
        return item

class DBPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=MYSQL_HOST,
            db=MYSQL_DBNAME,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWD,
            port=MYSQL_PORT,
            charset='utf8',
            )

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 插入数据
            flag = self.cursor.execute(
                "INSERT INTO article2 (article_id,title,content,url,media,publish_time,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (str(item['article_id']),
                 str(item['title']),
                 str(item['content']),
                 str(item['url']),
                 str(item['media']),
                 item['time'],
                item['create_time']))

            # 提交sql语句
            self.connect.commit()
            if flag == 1:
                print('文章---' + title + '保存成功！')
                print(str(article_id) + '-----' + str(time))
            else:
                print('文章---' + title + '保存失败！')

        except Exception as e:
            # 出现错误时打印错误日志
            print(e)
        return item