# -*- coding: utf-8 -*-
import scrapy
import re
import json
from somenew.items import SomenewItem
import pymysql
from w3lib.html import remove_tags
import datetime
import html
import hashlib
import requests
from copy import deepcopy


class WbSearchSpider(scrapy.Spider):
    name = 'wb_search'
    allowed_domains = ['weibo.cn']
    start_urls = ['https://weibo.cn']

    def start_requests(self):
        conn = pymysql.connect(host='47.92.166.26', port=3306, user='root', password='admin8152', database='xuanyuqing',
                               charset='utf8')
        cs1 = conn.cursor()
        #
        cs1.execute(
            'select title from company_keywords where is_del=0 and popular_feelings_id in (select id from company_popular_feelings where is_del=0)')
        result = cs1.fetchall()

        for res in result:
            for i in range(10)[1:]:
                url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D' + str(
                    res[0]) + '&page_type=searchall&page={}'.format(i)
                print(url)
                yield scrapy.Request(url, callback=self.parse)
        # # 以下为测试代码,在不调用mysql的情况下进行测试
        # for i in range(2)[1:]:
        #     url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D' + '临沂' + '&page_type=searchall&page={}'.format(
        #         i)
        #     print(url)
        #     yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = SomenewItem()
        htm_str = response.body.decode()
        # print('2' * 20)
        content_card = json.loads(htm_str).get('data').get('cards')  # 这个content是可以获得的，没有报错
        # print("=2=" * 20)
        # print('content',content)
        # print('cards',cards)
        card_groups = []
        if (len(content_card) == 1):
            card_groups = content_card[0]['card_group']
        if (len(content_card) > 1):
            for con in content_card:
                card_groups += con['card_group']
        for j in range(len(card_groups)):
            # print('=3=' * 20)
            # print(card_groups[j])
            card_type = card_groups[j].get('card_type')
            # print(card_type)
            # print('=4=' * 20)
            if (card_type == 9):
                mblog = card_groups[j].get('mblog')
                item['fav_num'] = mblog.get('attitudes_count')  # 点赞数
                item['comm_num'] = mblog.get('comments_count')  # 评论数
                created_at = mblog.get('created_at')  # 发送时间
                # item['time'] = created_at
                # 比如现在时间是2018/7/27,如果使用上边的item['time'] = created_at ,时间未经过下边的if判断,很早的数据也会被抓取.过早的数据没用,所以添加item['time'] = None
                item['time'] = None

                if len(created_at) < 6:
                    # 添加年的字符串
                    print('len(created_at) < 6')
                    today = datetime.date.today()
                    time = '%d-' % (today.year)
                    item['time'] = time + created_at
                if '刚刚' in created_at:
                    item['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                if '分钟' in created_at:
                    print("'分钟' in created_at:")
                    re_time = re.match('(\d+)分钟前', created_at)
                    if re_time is not None:
                        item['time'] = (
                            datetime.datetime.now() - datetime.timedelta(minutes=int(re_time.group(1)))).strftime(
                            "%Y-%m-%d %H:%M")
                if '小时' in created_at:
                    print("'小时' in created_at:")
                    re_time = re.match('(\d+)小时前', created_at)
                    if re_time is not None:
                        item['time'] = (
                            datetime.datetime.now() - datetime.timedelta(hours=int(re_time.group(1)))).strftime(
                            "%Y-%m-%d %H:%M")

                if '昨天' in created_at:
                    print("'昨天' in created_at:")
                    today = datetime.date.today()
                    time = '%d-%d-%d ' % (today.year, today.month, today.day - 1)
                    re_time = re.match('.*?(\d+:\d+)', created_at)
                    if re_time is not None:
                        item['time'] = time + re_time.group(1)

                # print('日期 ' + created_at)
                # 只有非空的item['time'] 才是今年的数据,才值得被采用
                if item['time'] is not None:
                    print('weibo.py', item['time'])
                    item['env_num'] = mblog.get('reposts_count')  # 转发数
                    idstr = mblog.get('idstr')
                    item['url'] = 'https://m.weibo.cn/detail/' + str(idstr)  # 网址

                    try:
                        content = remove_tags(mblog.get('text'))
                        if mblog.get('longText').get('longTextContent'):
                            content = remove_tags(mblog.get('longText').get('longTextContent'))
                    except Exception as e:
                        print(e)
                    finally:
                        item['content'] = content
                        content = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\u200b',
                                                                                                           u' ')
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
                        # print('content2',str(content2))
                        item['content'] = str(content) + "\n" + str(content2)
                    item['user_id'] = mblog.get('user').get('id')
                    item['user_name'] = mblog.get('user').get('screen_name')
                    item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                    m = hashlib.md5()
                    url = str(item['url'])
                    m.update(str(url).encode('utf8'))
                    article_id = str(m.hexdigest())
                    item['article_id'] = article_id
                    item['read_num'] = 0
                    item['media_type'] = '微博'
                    # 微博爬虫中的media是写死在pipeline中的,但是这里无法写死,所以需要添加media
                    item['media'] = '微博'

                    yield scrapy.Request(item['url'], callback=self.get_content, meta={'item': deepcopy(item)})

            if (card_type == 8):
                # 获取关键词的热门资讯、新鲜事、有缘人
                scheme = card_groups[j].get('scheme')
                scheme_re = re.match(r"https://m.weibo.cn/p/tabbar\?containerid=(\d+)", scheme)
                if scheme_re:
                    containerid = scheme_re.group(1)
                    for i in range(4)[1:]:
                        # print('$$$$$$$in-scheme==='*50)
                        url = 'https://m.weibo.cn/api/container/getIndex?containerid={containerid}&page={page}'.format(
                            containerid=containerid, page=i)
                        yield scrapy.Request(url, callback=self.parse)

            if (card_type == 24):
                # 获取关键词的搜索到的用户
                scheme = card_groups[j].get('scheme')
                scheme_re = re.match(r'.*?(containerid=.*)', scheme)
                if scheme_re:
                    # print(scheme_re.group(1))
                    json_url = 'https://m.weibo.cn/api/container/getIndex?' + scheme_re.group(1)
                    for i in range(4)[1:]:
                        # print('$$$$$$$in-scheme===' * 50)
                        url = json_url + '&page={}'.format(i)
                        yield scrapy.Request(url, callback=self.get_users)

    def get_users(self, response):
        ret = response.body.decode()
        if ret:
            res_json = json.loads(ret)
            url = response.url
            page = re.match(".*?page=(\d+)", url).group(1)
            if int(page) == 1:
                # print('1' * 100)
                card_list = res_json['data']['cards'][1]['card_group']
                # print(card_list)
            else:
                # print('2' * 100)
                card_list = res_json['data']['cards'][0]['card_group']
            try:
                for res in card_list:
                    user_id = res['user']['id']  # 用户id
                    containerid = str(107603) + str(user_id)
                    for i in range(4)[1:]:
                        weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + str(
                            user_id) + '&containerid=' + str(containerid) + '&page=' + str(i)
                        yield scrapy.Request(weibo_url, callback=self.get_user_content)
            except Exception as e:
                print(e)

    def get_user_content(self, response):
        item = SomenewItem()
        html = response.body.decode()
        # print('2' * 20)
        content = json.loads(html).get('data')
        cards = content.get('cards')
        if (len(cards) > 0):
            for j in range(len(cards)):
                card_type = cards[j].get('card_type')
                if (card_type == 9):
                    mblog = cards[j].get('mblog')
                    item['fav_num'] = mblog.get('attitudes_count')  # 点赞数
                    item['comm_num'] = mblog.get('comments_count')  # 评论数
                    created_at = mblog.get('created_at')  # 发送时间
                    # item['time'] = created_at
                    # 现在时间是2018/7/27,如果使用上边的item['time'] = created_at ,时间未经过下边的if判断,很早的数据也会被抓取.过早的数据没用,所以添加item['time'] = None
                    item['time'] = None

                    if len(created_at) < 6:
                        # 添加年的字符串
                        print('len(created_at) < 6')
                        today = datetime.date.today()
                        time = '%d-' % (today.year)
                        item['time'] = time + created_at
                    if '刚刚' in created_at:
                        item['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    if '分钟' in created_at:
                        print("'分钟' in created_at:")
                        re_time = re.match('(\d+)分钟前', created_at)
                        if re_time is not None:
                            item['time'] = (
                                datetime.datetime.now() - datetime.timedelta(minutes=int(re_time.group(1)))).strftime(
                                "%Y-%m-%d %H:%M")
                    if '小时' in created_at:
                        print("'小时' in created_at:")
                        re_time = re.match('(\d+)小时前', created_at)
                        if re_time is not None:
                            item['time'] = (
                                datetime.datetime.now() - datetime.timedelta(hours=int(re_time.group(1)))).strftime(
                                "%Y-%m-%d %H:%M")

                    if '昨天' in created_at:
                        print("'昨天' in created_at:")
                        today = datetime.date.today()
                        time = '%d-%d-%d ' % (today.year, today.month, today.day - 1)
                        re_time = re.match('.*?(\d+:\d+)', created_at)
                        if re_time is not None:
                            item['time'] = time + re_time.group(1)

                    # print('日期 ' + created_at)
                    # 只有非空的item['time'] 才是今年的数据,才值得被采用
                    if item['time'] is not None:
                        print('weibo.py', item['time'])
                        item['env_num'] = mblog.get('reposts_count')  # 转发数
                        idstr = mblog.get('idstr')
                        item['url'] = 'https://m.weibo.cn/detail/' + str(idstr)  # 网址
                        # item['url'] = cards[j].get('scheme')  # 网址
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
                        item['user_id'] = mblog.get('user').get('id')
                        item['user_name'] = mblog.get('user').get('screen_name')
                        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                        m = hashlib.md5()
                        url = str(item['url'])
                        m.update(str(url).encode('utf8'))
                        article_id = str(m.hexdigest())
                        item['article_id'] = article_id
                        item['read_num'] = 0
                        item['media_type'] = '微博'
                        # 微博爬虫中的media是写死在pipeline中的,但是这里无法写死,所以需要添加media
                        item['media'] = '微博'
                        yield scrapy.Request(item['url'], callback=self.get_content, meta={'item': deepcopy(item)})

    def get_content(self, response):
        item = deepcopy(response.meta['item'])
        item['addr_province'] = '全国'
        html = response.body.decode()
        # 获取微博全文内容
        dict = re.findall(r'render_data = \[\{\n    \"status\"\: (\{.*?\}),\n    \"hotScheme\"', html, re.S)
        if dict != []:
            dict = ''.join(dict[0]).replace('\n', '').replace(' ', '')
            json_dic = json.loads(dict)
            time = json_dic['created_at']
            # 把英文格式的时间转换为正常格式的带时区的时间
            time = datetime.datetime.strptime(time, '%a%b%d%H:%M:%S%z%Y')
            # 把带时区的时间转换为不带时区的时间
            dt = datetime.datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
            item['time'] = dt
            content1 = json_dic['text']
            content = content1
            # 是否有转发原文
            if 'retweeted_status' in json_dic:
                # 转发原文为长文
                if 'longText' in json_dic['retweeted_status']:
                    content2 = json_dic['retweeted_status']['longText']['longTextContent']
                    content = content1 + content2
                # 转发原文为非长文：
                else:
                    content2 = json_dic['retweeted_status']['text']
                    content = content1 + content2
            # if content == []:
            content = remove_tags(content)
            item['content'] = content.replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\u200b', u' ')
            # print(item)
            yield item
        else:
            # 直接返回非全文的json中的内容
            # print(item)
            yield item
