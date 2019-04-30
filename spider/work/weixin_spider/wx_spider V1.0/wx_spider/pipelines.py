# -*- coding: utf-8 -*-

from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch
import sys
import importlib
# from WB.models.news_qinggan_analysis import lstm_predict
from aip import AipNlp
importlib.reload(sys)
from wx_spider.models.es_model import Sina_type

class WxSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class DBPipline(object):
    def process_item(self,item,spider):
        # 获取情感分类
        # 百度api的相关信息 ,杨春强的api
        APP_ID = '11678988'
        API_KEY = 'zgPHgI5TSrIyGMuNWTtnzSs4'
        SECRET_KEY = '71G1yqiZCMGKf9SCRKEIBZSeKURZ0Gj1'
        # 百度api创建连接
        client = AipNlp(APP_ID,API_KEY,SECRET_KEY)
        es2 = Elasticsearch(hosts=['localhost'])
        res2 = es2.exists(index='spider',doc_type='article',id=item['article_id'])
        if res2 is not True:
            q = 0
            """ 调用情感倾向分析 """
            qinggan = client.sentimentClassify(item['content'])
            try:
                if qinggan['items'][0]['sentiment'] == 2:  # 正向
                    q = 1
                if qinggan['items'][0]['sentiment'] == 1:  # 中性
                    q = 0
                if qinggan['items'][0]['sentiment'] == 0:  # 负面
                    q = 2
            except Exception as e:
                print(e)

            # 将数据存入es
            es = connections.create_connection(Sina_type._doc_type.using)
            try:
                art = Sina_type()
                art.title=item['title']
                art.content = item['content']
                art.media = '微信公众号'
                art.publish_time = item['time']
                art.create_time = item['create_time']
                art.url = item['url']
                art.qinggan = q
                art.comm_num = int(item['comm_num'])
                art.read_num = int(item['read_num'])
                art.fav_num = int(item['fav_num'])
                art.env_num = int(item['env_num'])
                art.hot_value = int(item['comm_num']) + int(item['read_num']) + int(item['fav_num']) + int(item['env_num'])
                # art.user_id = item['user_id']
                art.user_name = item['user_name']
                art.meta.id = item['article_id']
                art.save()
                print("elasticsearch 存入一条数据", item['article_id'])
            except Exception as e:
                print(e)
                print("es存入错误  " * 30)
        return item




