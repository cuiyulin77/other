# -*- coding: utf-8 -*-

import pymysql

class GovPeoplePipeline(object):
    def process_item(self, item, spider):
        return item

class DBPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='localhost',
            db= 'article_spider',
            user='root',
            passwd='root',
            port=3306,
            charset='utf8',
            )

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 插入数据
            flag = self.cursor.execute(
                "INSERT INTO gov_leaders (id,position,name,department,province,city,people_url) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                ('0',
                 str(item['position']),
                 str(item['name']),
                 str(item['department']),
                 str(item['province']),
                 item['city'],item['people_url']))

            # 提交sql语句
            self.connect.commit()
            if flag == 1:
                print(item['department'] + item['position']+ item['name'] + '保存成功！')

            else:
                print(item['department'] + item['position']+ item['name'] + '保存失败！')

        except Exception as e:
            # 出现错误时打印错误日志
            print(e)
        return item
