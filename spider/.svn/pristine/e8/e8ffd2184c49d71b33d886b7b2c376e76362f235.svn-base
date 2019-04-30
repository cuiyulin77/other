# -*- coding: utf-8 -*-
import scrapy
import pymysql
import re
from WB.items import WbItem
import json
from copy import deepcopy
import datetime
import hashlib
from copy import deepcopy
from w3lib.html import remove_tags

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.com','m.weibo.cn']
    # 获取用户id
    url_list = []
    # 使用本地服务器mysql
    connect = pymysql.connect(
        # host='127.0.0.1',
        host='192.168.3.15',
        db='spider',
        user='root',
        # password='admin8152',
        password='root',
        port=3306,
        charset='utf8'
    )
    cursor = connect.cursor()
    cursor.execute("select user_id,containerid from weibo_user where fans>20000")
    result = cursor.fetchall()
    for ret in result:
        # print(ret)
        # print("*" * 10)
        user_id,containerid = ret
        # 下边的正则是为测试数据使用的
        # user_id = re.match(r'https\:\/\/m\.weibo\.cn\/u\/(\d+)\?uid.*', ret).group(1)
        print(user_id)
        # 通过用户id组成url，生成url列表
        for i in range(1, 3):
            weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + str(user_id) + '&containerid=' + str(containerid) + '&page=' + str(i)
            url_list.append(weibo_url)
    start_urls = url_list

    def parse(self, response):
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
                        # today = datetime.date.today()

                        re_time = re.match('.*?(\d+:\d+)',created_at)
                        if re_time is not None:
                            time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d ")
                            item['time'] = time + re_time.group(1)

                    # print('日期 ' + created_at)
                    # 只有非空的item['time'] 才是今年的数据,才值得被采用
                    if item['time'] is not None:
                        print('weibo.py',item['time'])
                        item['env_num'] = mblog.get('reposts_count')  # 转发数
                        item['url'] = cards[j].get('scheme')    # 网址
                        content = remove_tags(mblog.get('text'))
                        content = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\u200b',
                                                                                                           u' ')
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
                            content2 = ''.join(content2).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(
                                u'\u200b', u' ')
                            item['content'] = content + "\n" + content2
                        item['user_id']=mblog.get('user').get('id')
                        item['user_name'] = mblog.get('user').get('screen_name')
                        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                        m = hashlib.md5()
                        url = str(item['url'])
                        m.update(str(url).encode('utf8'))
                        article_id = str(m.hexdigest())
                        item['article_id'] = article_id
                        item['read_num'] = 0
                        yield scrapy.Request(item['url'],callback=self.get_content,meta={'item': deepcopy(item)})

    def get_content(self,response):
        item = deepcopy(response.meta['item'])
        html = response.body.decode()
        # 获取微博全文内容
        dict = re.findall(r'render_data = \[\{\n    \"status\"\: (\{.*?\}),\n    \"hotScheme\"', html, re.S)
        if dict != []:
            dict = ''.join(dict[0]).replace('\n', '').replace(' ', '')
            json_dic = json.loads(dict)
            content1 = json_dic['text']
            content = content1
            # 是否有转发原文
            if 'retweeted_status' in json_dic:
                # 转发原文为长文
                if 'longText' in json_dic['retweeted_status']:
                    content2 = json_dic['retweeted_status']['longText']['longTextContent']
                    content = content1+content2
                # 转发原文为非长文：
                else:
                    content2 = json_dic['retweeted_status']['text']
                    content = content1 + content2
            # if content == []:
            content = remove_tags(content)
            item['content'] = content.replace(u'\u3000',u' ').replace(u'\xa0', u' ').replace(u'\u200b',u' ')
            yield item
        else:
            # 直接返回非全文的json中的内容
            yield item























