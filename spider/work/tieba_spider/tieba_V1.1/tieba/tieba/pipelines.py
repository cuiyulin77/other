# -*- coding: utf-8 -*-

from pymysql import *
from tieba.models.es_model import Sina_type
from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch
import sys
import importlib
from tieba.models.news_qinggan_analysis import lstm_predict


class DBPipeline(object):

    def process_item(self, item, spider):
        # 获取情感分类
        q = lstm_predict(item['content'])
        # q = 0
        es2 = Elasticsearch(hosts=['localhost'])
        # 存入mysql,同时存入es
        res2 = es2.exists(index="spider", doc_type='article', id=item['article_id'])

        # 将数据存入es
        es = connections.create_connection(Sina_type._doc_type.using)
        try:
            # print("04%" * 30)
            art = Sina_type()
            content = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
            art.content = content
            art.title = item['title']
            art.media = '百度贴吧'
            art.publish_time = item['update_time']
            art.create_time = item['create_time']
            art.url = item['url']
            art.qinggan = q
            art.comm_num = int(item['comm_num'])
            art.read_num = int(item['read_num'])
            art.fav_num = int(item['fav_num'])
            art.env_num = int(item['env_num'])
            art.hot_value = int(item['comm_num']) + int(item['read_num']) + int(item['fav_num']) + int(
                item['env_num'])
            art.update_time = item['time']
            art.media_type = item['media_type']
            art.meta.id = item['article_id']

            art.save()
            print("elasticsearch 存入一条数据", item['article_id'])
        except Exception as e:
            print(e)
            print("03" * 30)
        return item


class TiebaPipeline(object):
    def process_item(self, item, spider):
        return item
