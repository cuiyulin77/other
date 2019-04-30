# -*- coding: utf-8 -*-

# from pymysql import *
from somenew.models.es_model import Sina_type
from w3lib.html import remove_tags
from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch
import sys
import importlib
# from somenew.models.news_qinggan_analysis import lstm_predict
from aip import AipNlp
importlib.reload(sys)

# q = lstm_predict(item['content'])

class SomenewPipeline(object):
    def process_item(self, item, spider):
        return item


class DBPipeline(object):
    # def __init__(self):
    #     # 连接数据库
    #     self.connect = connect(
    #         # host='47.92.77.18',
    #         # host='192.168.3.54',
    #         host='127.0.0.1',
    #         db='spider',
    #         user='root',
    #         # password='admin8152', # 生产服务器
    #         password='root',
    #         port=3306,
    #         charset='utf8'
    #
    #     )
    #     self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # 获取情感分类
        # 百度api的相关信息 ,李帅江的api
        APP_ID = '11678620'
        API_KEY = '3NutK9nnuIFNaHWo99DBFQPO'
        SECRET_KEY = 'wOEplSNzrgFyyjTrqHxPQA0kVPnNh7Lr'
        # 百度api链接
        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


        # q = 0
        # es2 = Elasticsearch(hosts=['47.92.77.18'])
        es2 = Elasticsearch(hosts=['localhost'])
        # es2 = Elasticsearch(hosts=['192.168.3.15'])
        # 存入mysql,同时存入es
        res2 = es2.exists(index="spider", doc_type='article', id=item['article_id'])
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
            # try:
            #     # 插入数据
            #     self.cursor.execute(
            #         "INSERT INTO article (id,article_id,title,content,url,media,publish_time,create_time,qinggan,comm_num,read_num,fav_num,env_num) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            #         ('0', str(item['article_id']),
            #          str(item['title']),
            #          str(item['content']),
            #          str(item['url']),
            #          str(item['media']),
            #          item['time'],
            #          item['create_time'],
            #          str(q),
            #          str(item['comm_num']), str(item['read_num']), str(item['fav_num']), str(item['env_num'])
            #          )
            #     )
            #     self.connect.commit()
            #     print('mysql一条数据插入成功')
            # except Exception as e:
            #     # 出现错误时打印错误日志
            #     print(e)

            # 将数据存入es
            es = connections.create_connection(Sina_type._doc_type.using)
            try:
                print("04%" * 30)
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
                # query_json = {
                #     "title":item['title'],'content':remove_tags(content),'media':item['media'],'publish_time':item['time'],
                #     'create_time':item['create_time'],'url':item['url'],'qinggan':q,'comm_num':item['comm_num'],
                #     'read_num':item['read_num'],'fav_num':item['fav_num'],'env_num':item['env_num']
                # }

                art.save()
                # res = es2.index(index="spider", doc_type='article', id=item['article_id'],body={"query": query_json})
                print("elasticsearch 存入一条数据", item['article_id'])
            except Exception as e:
                print(e)
                print("03" * 30)
        return item

# class SaveToEsPipeline(object):
#     def process_item(self, item, spider):
#         # 存入es中
#         es = connections.create_connection(Sina_type._doc_type.using)
#         # es2 = Elasticsearch(hosts=['47.92.77.18'])
#         # 通过id查看是否存在
#         res2 = es2.exists(index="test", doc_type='article', id=item['article_id'])
#         print("01"*30)
#         # 如果不存在，就往es里存
#         if res2 is not True:
#             print("02==" * 30)
#             try:
#                 print("04%" * 30)
#                 art = Sina_type()
#                 art.title = item['title']
#                 content = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\\u3000', u' ').replace(u'\\xa0', u' ')
#                 art.content = remove_tags(content)
#                 art.media = item['media']
#                 art.publish_time = item['time']
#                 art.create_time = item['create_time']
#                 art.url = item['url']
#                 art.comm_num = int(item['comm_num'])
#                 art.read_num = int(item['read_num'])
#                 art.fav_num = int(item['fav_num'])
#                 art.env_num = int(item['env_num'])
#                 art.meta.id = item['article_id']
#
#                 art.save()
#                 print("elasticsearch 存入一条数据",item['article_id'])
#             except Exception as e:
#                 print(e)
#                 print("03" * 30)
#         print("*@*"*30)
#         return item