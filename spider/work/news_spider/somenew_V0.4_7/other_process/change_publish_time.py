# coding=utf8
# 修改article集合中的publish_time，从字符串更新为date格式
from pymongo import *
import datetime
import re

try:
    clien = MongoClient(host='127.0.0.1',port=27017)
    print("111")
    db = clien.spider
    msg_list = db.article.find()
    for msg in msg_list:
        print('002')
        # create_time_1 = None
        # create_time_2 = None
        # create_time_3 = None
        # print(msg)
        try:
            publish_time_self = msg['publish_time']
            print("005")
            if publish_time_self is not None:
                # 时间格式20180510 141214
                try:
                    print('006')
                    publish_time_1 = re.match(r'\d{8} \d{6}',publish_time_self).group()
                    if publish_time_1 is not None:
                        print('create_time_1')
                        date_time = datetime.datetime.strptime(publish_time_1, '%Y/%m/%d %H:%M')
                        # date_time = datetime.datetime.strptime(create_time_1, '%Y%m%d %H%M%S')
                        db.article.update_one({'_id': msg['_id']}, {'$set': {'publish_time': date_time}})
                except Exception as e:
                    print('006=======')
                    # print(e)

                try:
                    print('007')
                    # 时间格式2018/05/10 14：12：14
                    publish_time_2 = re.match(r'\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}', publish_time_self).group()
                    if publish_time_2 is not None:
                        print('create_time_1')
                        # date_time = datetime.datetime.strptime(create_time_2, '%Y/%m/%d %H:%M:%S')
                        date_time = datetime.datetime.strptime(publish_time_2, '%Y/%m/%d %H:%M')
                        db.article.update_one({'_id': msg['_id']}, {'$set': {'publish_time': date_time}})
                except Exception as e:
                    print('007+++++++')
                    # print(e)

                try:
                    print('008')
                    # 时间格式2018-05-10 14：12：14
                    publish_time_3 = re.match(r'\d{4}-d{2}-d{2} \d{2}:\d{2}', publish_time_self).group()
                    if publish_time_3 is not None:
                        print('create_time_1')
                        date_time = datetime.datetime.strptime(publish_time_3, '%Y/%m/%d %H:%M')
                        # date_time = datetime.datetime.strptime(create_time_3, '%Y%m%d %H%M%S')
                        db.article.update_one({'_id': msg['_id']}, {'$set': {'publish_time': date_time}})
                except Exception as e:
                    print('008********')

        except Exception as e:
            print(e)
except Exception as e:
    print(e)


