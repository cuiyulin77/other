# -*- coding: utf-8 -*-

from pymysql import *
from somenew.models.es_model import Sina_type
from w3lib.html import remove_tags
from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch
import sys
import importlib
from somenew.models.news_qinggan_analysis import lstm_predict
importlib.reload(sys)


class SomenewPipeline(object):
    def process_item(self, item, spider):
        return item

def gen_suggests(index, info_tuple,es):
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

class DBPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = connect(
            host='47.92.77.18',
            db='spider',
            user='root',
            password='root',
            port=3306,
            charset='utf8'

        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # 获取情感分类
        q = lstm_predict(item['content'])
        # 存入mysql
        try:
            # 插入数据
            self.cursor.execute(
                "INSERT INTO article_copy (id,article_id,title,content,url,media,publish_time,create_time,qinggan) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                ('0',str(item['article_id']),
                str(item['title']),
                str(item['content']),
                str(item['url']),
                str(item['media']),
                item['time'],
                item['create_time'],
                 str(q))
            )
            self.connect.commit()
            print('一条数据插入成功')
        except Exception as e:
            # 出现错误时打印错误日志
            print(e)
        return item

# class SaveToEsPipeline(object):
#     def process_item(self, item, spider):
#         # 存入es中
#         es = connections.create_connection(Sina_type._doc_type.using)
#         es2 = Elasticsearch(hosts=['47.92.77.18'])
#         # 通过id查看是否存在
#         res2 = es2.exists(index="spider", doc_type='article', id=item['article_id'])
#         print("01"*30)
#         # 如果不存在，就往es里存
#         if res2 is not True:
#             print("02==" * 30)
#             try:
#                 print("04%" * 30)
#                 art = Sina_type()
#                 art.title = item['title']
#                 content = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
#                 art.content = remove_tags(content)
#                 art.media = item['media']
#                 art.publish_time = item['time']
#                 art.create_time = item['create_time']
#                 art.url = item['url']
#                 art.meta.id = item['article_id']
#                 art.suggest = gen_suggests(Sina_type._doc_type.index, ((art.title, 10), (art.content, 7)), es)
#                 art.save()
#                 print("elasticsearch 存入一条数据",item['article_id'])
#             except Exception as e:
#                 print(e)
#                 print("03" * 30)
#         print("*@*"*30)
#         return item
