# -*- coding: utf-8 -*-
# from pymysql import *
from w3lib.html import remove_tags
from WB.models.es_model import Sina_type
from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch
import sys
import importlib
# from WB.models.news_qinggan_analysis import lstm_predict
from aip import AipNlp
importlib.reload(sys)


class WbPipeline(object):
    def process_item(self, item, spider):
        return item

class DBPipeline(object):

    def process_item(self, item, spider):
        # 获取情感分类
        # 百度api的相关信息 ,本人的api
        APP_ID = '11677563'
        API_KEY = 'MP7pDCgKAiVcWWrQ3dhjHmc9'
        SECRET_KEY = 'FQHM4Rn27NWpGDlUx0IEzYi7q1You0Gh'
        # 百度api链接
        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

        # q = lstm_predict(item['content'])
        # q = 0
        es2 = Elasticsearch(hosts=['localhost'])
        # 存入mysql,同时存入es
        res2 = es2.exists(index="spider", doc_type='article', id=item['article_id'])
        if (res2 is not True) and item['content']:
            try:
                item['content'] = item['content'].encode('utf8').decode('utf8')
            except:
                pass


            """ 调用情感倾向分析 """
            q = 0
            qinggan = 0
            try:
                qinggan = client.sentimentClassify(item['content'])
            except:
                pass
            try:
                if qinggan['items'][0]['sentiment'] == 2:  # 正向
                    q = 1
                if qinggan['items'][0]['sentiment'] == 1:  # 中性
                    q = 0
                if qinggan['items'][0]['sentiment'] == 0:  # 负面
                    q = 2
            except Exception as e:
                print('情感api获得的错误',e)

            """进行新闻分类"""
            res = {}
            if 'title' in item.keys():
                try:
                    res = client.topic(item['title'], item['content'])
                except:
                    pass
            else:
                try:
                    res = client.topic('1', item['content'])
                except:
                    pass
            # print(res)
            try:
                classify = res["item"]['lv1_tag_list'][0]['tag']
            except:
                try:
                    classify = res["item"]['lv2_tag_list'][0]['tag']
                except:
                    classify = '其他'

            # 将数据存入es
            es = connections.create_connection(Sina_type._doc_type.using)
            try:
                print("04%" * 30)
                art = Sina_type()
                content = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\\u3000', u' ').replace(u'\\xa0', u' ')
                art.content = remove_tags(content)
                art.media = '微博'
                art.publish_time = item['time']
                art.create_time = item['create_time']
                art.url = item['url']
                art.qinggan = q
                art.comm_num = int(item['comm_num'])
                art.read_num = int(item['read_num'])
                art.fav_num = int(item['fav_num'])
                art.env_num = int(item['env_num'])
                art.hot_value = int(item['comm_num']) + int(item['read_num']) + int(item['fav_num']) + int(
                    item['env_num'])
                art.user_id = item['user_id']
                art.user_name = item['user_name']
                art.meta.id = item['article_id']
                art.classify = classify
                art.media_type = item['media_type']

                art.save()
                print("elasticsearch 存入一条数据",item['article_id'])
            except Exception as e:
                print('将数据存入es产生的error', e)
                print("03" * 30)
        return item


