# -*- coding: utf-8 -*-

import pymysql
# from somenew.models.es_model import Sina_type
# from w3lib.html import remove_tags
# from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch
import sys
import importlib
importlib.reload(sys)
import datetime
import time

class LvyouPipeline(object):
    def process_item(self, item, spider):
        return item

class DBPipeline(object):
    def __init__(self):
        # 连接数据库
        print('链接mysql数据库')
        self.connect = pymysql.connect(
            # host='192.168.3.15',
            # host="127.0.0.1",
            host = "47.92.166.26",
            db='tpdata',
            user='root',
            # passwd='root',
            passwd = 'admin8152',
            port=3306,
            charset='utf8',
            )

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        print('进入process_item')
        my_id = None
        truetime = str(int(time.time()))
        # es = Elasticsearch(hosts=['192.168.3.15'])
        es = Elasticsearch(hosts=['localhost'])
        # url是否存在
        res = es.exists(index="urls", doc_type='url', id=item['article_id'])
        if (res is not True) and item['content']:
            try:
                # 插入文章内容到tp_ecms_news_check_data
                self.cursor.execute(
                    "INSERT INTO tp_ecms_news_index (id,classid,checked,newstime,truetime,lastdotime,havehtml) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    ('0', item['classid'], '0',                 # id,classid,checked,
                     item['newstime'],truetime, truetime, '1',  # newstime,truetime,lastdotime,havehtml

                     ))
                print('tp_ecms_news_index 插入成功')
                my_id = self.cursor.lastrowid
                # 如果获得id,再进行插入
                if my_id:
                    # 插入文章内容到tp_ecms_news_check_data
                    self.cursor.execute(
                        "INSERT INTO tp_ecms_news_check_data (id,classid,keyid,dokey,newstempid,closepl,haveaddfen,infotags,writer,befrom,newstext) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (my_id,item['classid'],item['keyid'],          # id,classid,keyid
                         '1','0','0','0',                            # dokey,newstempid,closepl,haveaddfen
                         ' ',item['writer'],                         # infotags,writer
                         item['media'],                              # befrom
                         item['content'],                            # newstext
                         ))
                    print('tp_ecms_news_check_data 插入成功')
                    newspath = str(datetime.date.today())
                    truetime = str(int(time.time()))

                    titleurl = "/e/action/ShowInfo.php?classid={classid}&id={id}".format(classid=item['classid'],id=my_id)
                    flag = self.cursor.execute(
                        "INSERT INTO tp_ecms_news_check  (id,classid,ttid,onclick,plnum,totaldown,newspath,filename,userid,username,firsttitle,isgood,ispic,istop,isqf,ismember,isurl,truetime,lastdotime,havehtml,groupid,userfen,titlefont,titleurl,stb,fstb,restb,keyboard,title,newstime,titlepic,ftitle,smalltext,diggtop,diqu,hangye) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (str(my_id), item['classid'], 0,              # id,classid,ttid
                         '10', '0', '0', newspath,             # onclick,plnum,totaldown,newspath,
                         str(my_id), '2',                      # filename,userid
                         'theping','0','1','1',                # username,firsttitle,isgood,ispic,
                         '0','0','0','0',                      # istop,isqf,ismember,isurl,
                         truetime,truetime,'1','0','0','',   # truetime,lastdotime,havehtml,groupid,userfen,titlefont
                         titleurl,'1','1','1',' ',           # titleurl,stb,fstb,restb,keyboard,
                         item['title'],item['newstime'],     # title,newstime
                         item['titlepic'],' ',               # ,titlepic,ftitle,
                         ' ','0','0','0'                     # smalltext,diggtop,diqu,hangye
                         ))
                    # 提交sql语句

                    self.connect.commit()
                    print('已经提交数据','id为',my_id)
                    if flag == 1:
                        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        create_time = create_time.replace(" ","T")
                        data = {
                            "url":item['url'],
                            "title":item['title'],
                            "mysql_id":my_id,
                            "create_time":str(create_time)

                        }
                        result = es.index(index="urls", doc_type='url',id=item['article_id'],body=data)
                        print(result['result'])
                        # es_result = result['_shards']['created']
                        # if es_result == "true":
                        #     print("插入elasticsearch成功")
            except Exception as e:
                # 出现错误时打印错误日志
                print('插入文章内容出错')
                print(e)
        return item

