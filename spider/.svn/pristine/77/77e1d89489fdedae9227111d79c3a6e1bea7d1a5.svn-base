# -*- coding: utf-8 -*-

from pymysql import *
from tieba.models.es_model import Sina_type
from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch
import sys
import importlib
from tieba.models.news_qinggan_analysis import lstm_predict


class DBPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = connect(
            # host='47.92.77.18',
            host='192.168.3.15',
            db='spider',
            user='root',
            # password='admin8152', # 生产服务器
            password='root',
            port=3306,
            charset='utf8'

        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # 获取情感分类
        q = lstm_predict(item['content'])
        # q = 0
        es2 = Elasticsearch(hosts=['192.168.3.15'])
        # 存入mysql,同时存入es
        res2 = es2.exists(index="spider", doc_type='article', id=item['article_id'])
        if res2 is not True:
            try:
                # 插入数据
                # item的update_time 应插入到mysql的pubulishtime的位置，因为前端是以publish_time进行倒序排列的，item的time应插入到mysql的update_time的位置
                self.cursor.execute(
                    "INSERT INTO tieba (id,article_id,content,title,url,publish_time,update_time,create_time,qinggan,comm_num,read_num,fav_num,env_num,hot_value) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    ('0', str(item['article_id']),
                     str(item['content']),
                     str(item['title']),
                     str(item['url']),
                     item['update_time'],
                     item['time'],
                     item['create_time'],
                     str(q),
                     str(item['comm_num']), str(item['read_num']), str(item['fav_num']), str(item['env_num']),
                     str(item['comm_num']),

                     )
                )
                self.connect.commit()
                print('mysql一条数据插入成功')
            except Exception as e:
                # 出现错误时打印错误日志
                print('mysql 错误', e)

        # 将数据存入es
        es = connections.create_connection(Sina_type._doc_type.using)
        # item的update_time 应插入到es的pubulishtime的位置，因为前端是以publish_time进行倒序排列的，item的time应插入到es的update_time的位置
        try:
            print("04%" * 30)
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
