#coding=utf-8
from pymysql import *
from pymongo import *

try:
    # 创建Connection连接
    conn = connect(host='192.168.3.54', port=3306, user='root', password='root', database='spider', charset='utf8')
    # 获得Cursor对象
    cs1 = conn.cursor()
    # 执行select语句，并返回受影响的行数：查询一条学生数据
    # count = cs1.execute('select ')
    count = cs1.execute('select  article_id,title,content,url,media,publish_time,create_time from article_copy')
    # 打印受影响的行数
    print(count)
    # 获取查询的结果
    result = cs1.fetchall()
    for one_result in result:
        article_id, title, content, url, media, publish_time, create_time = one_result
        try:
            # 创建连接对象
            client = MongoClient(host='127.0.0.1', port=27017)
            # 获得数据库，此处使用python数据库
            db = client.spider
            # 向集合stu中插入一条文档
            db.article.insert_one({'_id': article_id, 'title': title,'content':content, 'url':url, 'media':media, 'publish_time':publish_time, 'create_time':create_time})
            # 如果插入成功则提示ok
            print('ok')
        except Exception as e:
            print(e)


except Exception as e:
    print(e)
finally:
    # 关闭Connection对象
    conn.close()





