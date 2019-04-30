# -*- coding: utf-8 -*-
import scrapy
import pymysql
import re
from WB.items import WbItem
import json
from copy import deepcopy
import datetime
import hashlib
from w3lib.html import remove_tags

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.com','m.weibo.cn']
    # 获取用户id
    url_list = []

    start_urls = ['https://m.weibo.cn']
    def parse(self, response):
        # 使用本地服务器mysql
        connect = pymysql.connect(
            host='127.0.0.1',
            db='spider',
            user='root',
            password='admin8152',
            port=3306,
            charset='utf8'
        )
        cursor = connect.cursor()
        cursor.execute("select user_url from weibo_user")
        result = cursor.fetchall()
        # 下边的result列表是测试数据
        # result = ['https://m.weibo.cn/u/87983312?uid=87983312&luicode=10000011&lfid=231051_-_followers_-_1218500815',
        # 'https://m.weibo.cn/u/95095?uid=95095&luicode=10000011&lfid=231051_-_followers_-_3800468188',
        # 'https://m.weibo.cn/u/9545954?uid=9545954&luicode=10000011&lfid=231051_-_followers_-_1260431382',
        # 'https://m.weibo.cn/u/972760?uid=972760&luicode=10000011&lfid=231051_-_followers_-_1156382374',
        # 'https://m.weibo.cn/u/972897?uid=972897&luicode=10000011&lfid=231051_-_followers_-_1253446435',
        # 'https://m.weibo.cn/u/99001?uid=99001&luicode=10000011&lfid=231051_-_followers_-_1170096322',
        # 'https://m.weibo.cn/u/9996568?uid=9996568&luicode=10000011&lfid=231051_-_followers_-_1705975814',]
        for ret in result:
            # print(ret)
            # print("*" * 10)
            user_id = re.match(r'https\:\/\/m\.weibo\.cn\/u\/(\d+)\?uid.*', ret[0]).group(1)
            # 下边的正则是为测试数据使用的
            # user_id = re.match(r'https\:\/\/m\.weibo\.cn\/u\/(\d+)\?uid.*', ret).group(1)
            print(user_id)
            # 通过用户id组成url，生成url列表
            url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + user_id
            yield scrapy.Request(url,callback=self.get_containerid)


    def get_containerid(self,response):

        print("1"*20)
        url = response.url
        user_id = re.match(".*?(\d+)", url)
        res = response.body.decode()
        dict = json.loads(res).get('data')
        for data in dict.get('tabsInfo').get('tabs'):
            if (data.get('tab_type') == 'weibo'):
                containerid = data.get('containerid')
                # print(containerid)
                # print('2' * 20)
                # 取20页数据
                for i in range(1,21):
                    weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + str(user_id) + '&containerid=' + containerid + '&page=' + str(i)
                    yield scrapy.Request(weibo_url,callback=self.get_content)

    def get_content(self,response):
        item = WbItem()
        html = response.body.decode()
        print('2'*20)
        content = json.loads(html).get('data')
        cards = content.get('cards')
        if (len(cards) > 0):
            for j in range(len(cards)):
                card_type = cards[j].get('card_type')
                if (card_type == 9):
                    mblog = cards[j].get('mblog')
                    item['fav_num'] = mblog.get('attitudes_count')  # 点赞数
                    item['comm_num'] = mblog.get('comments_count')   # 评论数
                    created_at = mblog.get('created_at')   # 发送时间
                    # item['time'] = created_at
                    # 现在时间是2018/7/27,如果使用上边的item['time'] = created_at ,时间未经过下边的if判断,很早的数据也会被抓取.过早的数据没用,所以添加item['time'] = None
                    item['time'] = None

                    if len(created_at) < 6:
                        # 添加年的字符串
                        print('len(created_at) < 6')
                        today = datetime.date.today()
                        time = '%d-' % (today.year)
                        item['time'] = time + created_at
                    if '分钟' in created_at:
                        print("'分钟' in created_at:")
                        re_time = re.match('(\d+)分钟前',created_at)
                        if re_time is not None:
                            item['time'] = (datetime.datetime.now()-datetime.timedelta(minutes=int(re_time.group(1)))).strftime("%Y-%m-%d %H:%M")
                    if '小时' in created_at:
                        print("'小时' in created_at:")
                        re_time = re.match('(\d+)小时前', created_at)
                        if re_time is not None:
                            item['time'] = (datetime.datetime.now() - datetime.timedelta(hours=int(re_time.group(1)))).strftime("%Y-%m-%d %H:%M")

                    if '昨天' in created_at:
                        print("'昨天' in created_at:")
                        today = datetime.date.today()
                        time = '%d-%d-%d ' % (today.year,today.month, today.day - 1)
                        re_time = re.match('.*?(\d+:\d+)',created_at)
                        if re_time is not None:
                            item['time'] = time + re_time.group(1)

                    # print('日期 ' + created_at)
                    # 只有非空的item['time'] 才是今年的数据,才值得被采用
                    if item['time'] is not None:
                        print('weibo.py',item['time'])
                        item['env_num'] = mblog.get('reposts_count')  # 转发数
                        item['url'] = cards[j].get('scheme')    # 网址
                        content = remove_tags(mblog.get('text'))
                        content = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\u200b',u' ')
                        item['content'] = content
                        # 转发原文件
                        ret_s = None
                        try:
                            ret_s = mblog.get('retweeted_status')
                        except Exception as e:
                            pass
                        if ret_s is not None:
                            content2 = mblog.get('retweeted_status').get('text')
                            content2 = remove_tags(content2)
                            content2 = ''.join(content2).replace(u'\u3000',u' ').replace(u'\xa0', u' ').replace(u'\u200b',u' ')
                            item['content'] = content+"\n"+content2
                        item['user_id']=mblog.get('user').get('id')
                        item['user_name'] = mblog.get('user').get('screen_name')
                        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                        m = hashlib.md5()
                        url = str(item['url'])
                        m.update(str(url).encode('utf8'))
                        article_id = str(m.hexdigest())
                        item['article_id'] = article_id
                        item['read_num'] = 0
                        yield item























