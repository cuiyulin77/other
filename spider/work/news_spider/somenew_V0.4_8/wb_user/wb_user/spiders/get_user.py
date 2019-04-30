# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
from wb_user.items import WbUserItem
from copy import deepcopy
import re
import pymysql

class GetUserSpider(scrapy.Spider):
    name = 'get_user'
    allowed_domains = ['weibo.cn']
    # 1266321801
    # 连接mysql获取user_url,并从中获取user_id
    url_list = []
    # followers = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_1266321801&page={page}'
    connect = pymysql.connect(
        host='192.168.3.15',
        db='spider',
        user='root',
        password='root',
        port=3306,
        charset='utf8'
    )
    cursor = connect.cursor()
    cursor.execute(
        "select user_url from  weibo_user")
    result = cursor.fetchall()
    for ret in result:
        print(ret)
        print('*' * 10)
        user_id = re.match(r'https\:\/\/m\.weibo\.cn\/u\/(\d+)\?uid.*', ret[0]).group(1)
        followers = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{user_id}&page={page}'
        # 只能获得10页的关注人数，多了获取不到。另外有些大v第一页反而是一些总结性设置，所以，数据只能获得9页的关注
        for page in range(1, 11):
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print('正在爬 ' + '1266321801' + ' 第' + str(page) + '页的关注')
            url = followers.format(user_id=user_id, page=page)

            url_list.append(url)
    start_urls = url_list

    def parse(self, response):
        ret = response.body.decode()
        if ret:
            print('1'*100)
            res_json = json.loads(ret)
            print('2' * 100)
            try:
                for res in res_json['data']['cards'][0]['card_group']:

                    item = WbUserItem()
                    item['summary'] = res['desc1']
                    item['user_name'] = res['user']['screen_name']     # 昵称
                    item['user_url'] = res['user']['profile_url']    # 主页url
                    # item['user_id'] = re.match(r'https\:\/\/m\.weibo\.cn\/u\/(\d+)\?uid.*', item['user_url']).group(1)  # 用户id
                    item['fans'] = res['user']['followers_count']    # 粉丝数量
                    item['followers'] = res['user']['follow_count']  # 关注数量
                    item['get_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取信息时间
                    yield item
            except Exception as e:
                print(e)





        # ret = response.body.decode()
        # if ret:
        #     try:
        #         res_json = json.loads(ret)
        #         if 'userInfo' in res_json.keys():
        #             user = res_json['userInfo']['screen_name']
        #             user_id = res_json['userInfo']['id']
        #             user_url = res_json['userInfo']['profile_url']
        #             fans = res_json['userInfo']['followers_count']
        #
        #             followers = res_json['userInfo']['follow_count']
        #             time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #             verified = res_json['userInfo']['verified_reason']
        #             description = res_json['userInfo']['description']
        #
        #             item['user'] = user           # 用户名
        #             item['user_id'] = user_id     # id
        #             item['user_url'] = user_url   # profile_url，个人主页
        #             item['fans'] = fans           # 粉丝数量
        #             item['followers'] = followers   # 关注数量
        #             item['get_time'] = time         # 创建时间
        #             item['verified'] = verified     # 认证信息
        #             item['description'] = description  # 简介
        #     except:
        #         print('json解析出错')
        #     followers = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_1266321801&page={page}'
        #     for page in range(11):
        #         print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        #         print('正在爬 ' + '1266321801' + ' 第' + str(page) + '页的关注')
        #         url = followers.format(page = page)
        #         return scrapy.Request(url,callback=self.get_user_info,meta={"item":item})


    # def get_user_info(self,response):
    #     # item = deepcopy(response.meta['item'])
    #     ret = response.body.decode()
    #     if ret:
    #         try:
    #             res_json = json.loads(response)
    #             if 'cards' in res_json.keys():
    #                 if res_json['cards']:
    #                     results = res_json['cards'][0]
    #                     if 'card_group' in results.keys():
    #                         for res in results['card_group']:
    #                             if 'user' in res.keys():
    #                                 user = res['user']['screen_name']
    #                                 follower_user_id = res['user']['id']
    #         except Exception as e:
    #             print(e)

























