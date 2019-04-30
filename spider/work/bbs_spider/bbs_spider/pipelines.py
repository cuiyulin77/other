# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from bbs_spider.models.es_model import Sina_type
from w3lib.html import remove_tags
from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch
import sys
import importlib
# from somenew.models.news_qinggan_analysis import lstm_predict
from aip import AipNlp
importlib.reload(sys)

class BbsSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class DBPipeline(object):

    def process_item(self, item, spider):
        # print('开始进入管道')
        # 获取情感分类
        # 百度api的相关信息 ,崔玉林的api
        APP_ID = '15164532'
        API_KEY = 'L1wnpBlotOk1QP97CCdhh01M'
        SECRET_KEY = 'EjjUs57i1bTNvYiiTlaPT82EbVVzEQy5'
        # 百度api链接
        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

        # q = 0
        # es2 = Elasticsearch(hosts=['47.92.77.18'])
        es2 = Elasticsearch(hosts=['localhost'])
        # es2 = Elasticsearch(hosts=['192.168.3.15'])
        #存入es

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
            print(classify,'我是取得的值-------------------------------------------------------------------------------------------')
            # 将数据存入es
            es = connections.create_connection(Sina_type._doc_type.using)
            try:
                print("04%" * 30)
                if item['content']:
                    content = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\\u3000',
                                                                                                               u' ').replace(
                        u'\\xa0', u' ')

                    art = Sina_type()
                    art.title = item['title']
                    art.content = remove_tags(content)
                    art.media = item['media']
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
                    art.meta.id = item['article_id']
                    art.classify = classify
                    art.media_type = item['media_type']
                    if 'come_from' in item.keys():
                        art.come_from = item['come_from']
                    if 'addr_province' in item.keys():
                        art.addr_province = item['addr_province']
                    if 'addr_city' in item.keys():
                        art.addr_city = item['addr_city']
                    art.save()
                # res = es2.index(index="spider", doc_type='article', id=item['article_id'],body={"query": query_json})
                print("elasticsearch 存入一条数据", item['article_id'])
            except Exception as e:
                print(e)
                print("03" * 30)
        return item
