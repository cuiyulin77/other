# -*- coding: utf-8 -*-

from pymysql import *
from somenew.models.es_model import Sina_type
from w3lib.html import remove_tags
from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch
import sys
import importlib
importlib.reload(sys)

class SomenewPipeline(object):
    def process_item(self, item, spider):
        return item


class DBPipeline(object):
    def process_item(self, item, spider):

        # es2 = Elasticsearch(hosts=['47.92.77.18'])
        es2 = Elasticsearch(hosts=['localhost'])
        # es2 = Elasticsearch(hosts=['192.168.3.15'])
        # 更新es
        # 将数据存入es
        es = connections.create_connection(Sina_type._doc_type.using)
        try:
            print("04%" * 30)
            # art = Sina_type()
            # art.comm_num = int(item['comm_num'])
            # art.read_num = int(item['read_num'])
            # art.fav_num = int(item['fav_num'])
            # art.env_num = int(item['env_num'])
            # art.hot_value = int(item['hot_value'])
            # art.meta.id = item['article_id']
            #
            # art.save()
            query_json = {
                "comm_num":int(item['comm_num']),
                "read_num":int(item['read_num']),
                "fav_num":int(item['fav_num']),
                "env_num":int(item['env_num']),
                'hot_value':int(item['hot_value'])
            }
            es2.update(index='test', doc_type='article', id=item["article_id"], body=query_json)
            print("elasticsearch 更新热度值",item['article_id'])
        except Exception as e:
            print(e)
            print("03" * 30)
        return item

