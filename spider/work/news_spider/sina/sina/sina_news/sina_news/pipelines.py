# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# from sina_news.settings import MYSQL_HOST,MYSQL_DBNAME,MYSQL_USER,MYSQL_PASSWD,MYSQL_PORT
from models.es_types import Sina_type
from w3lib.html import remove_tags
from elasticsearch_dsl.connections import connections

es = connections.create_connection(Sina_type._doc_type.using)

def gen_suggests(index, info_tuple):
    # 根据字符串生成搜索建议
    used_words = set()
    suggests = []
    for text,weight in info_tuple:
        if text:
            words = es.indices.analyze(index=index,body={'text':text,'analyzer':"ik_max_word","filter": ["lowercase"]},)
            anylzed_word = set([r['token'] for r in words['tokens'] if len(r['token'])>=2])
            new_words = anylzed_word-used_words
        else:
            new_words = set()
        if new_words:
            suggests.append({'input':list(new_words),'weight':weight})
    return suggests


class SinaNewsPipeline(object):
    def process_item(self, item, spider):
        return item

class DBPipeline(object):
    def __init__(self):
        # 连接mysql数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',
            database='spider',
            user='root',
            passwd='root',
            port=3306,
            charset='utf8'
            )
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self,item,spider):
        try:
            # 插入数据
            self.cursor.execute(
                "INSERT INTO article (id,article_id,url,media,publish_time,create_time) VALUES (%d,%s,%s,%s,%s,%s)",
                (0,str(item['article_id']),
                 str(item['url']),
                 item["media"],
                 item['time']),
                item['create_time'])
            self.connect.commit()

            art = Sina_type()
            art.title = item['title']
            # art.time = item['time']
            art.content = remove_tags(item['content'])
            # art.url = item['url']
            art.meta.id = item['article_id']

            art.suggest = gen_suggests(Sina_type._doc_type.index, ((art.title, 10), (art.content, 7)))
            art.save()

        except Exception as e:
            # 出现错误时打印错误日志
            print(e)
        return item

# class ElasticsearchPipline(object):
#     def process_item(self,item,spider):
#         sina = Sina_type()
#         sina.title = item['title']
#         sina.time = item['time']
#         sina.content = remove_tags(item['content'])
#         sina.url = item['url']
#         sina.meta.id = item['article_id']
#
#         sina.suggest = gen_suggests(Sina_type._doc_type.index,((sina.title,10),(sina.content,7)))
#         sina.save()
#         return item
