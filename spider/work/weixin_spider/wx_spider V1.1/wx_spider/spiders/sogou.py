# -*- coding: utf-8 -*-
import scrapy
import re
import json
from wx_spider.items import WxSpiderItem
import pymysql
from w3lib.html import remove_tags
import datetime
import time
import html
import hashlib
from urllib.parse import urlencode
from copy import deepcopy

class SogouSpider(scrapy.Spider):
    name = 'sogou'
    allowed_domains = ['sogou.com',"weixin.qq.com"]
    url_list = []
    # 连接云服务器mysql
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='admin8152', database='xuanyuqing',
                           charset='utf8')
    cs1 = conn.cursor()
    # 查询company_popular_feelings中设定的关键字
    cs1.execute('select title from company_keywords where is_del=0 and popular_feelings_id in (select id from company_popular_feelings where is_del=0)')
    result = cs1.fetchall()
    for res in result:
        # print(res)
        # 通过关键字组合成搜索首页
        url = "http://weixin.sogou.com/weixin?type=2&s_from=input&query={keyword}&ie=utf8".format(keyword=res[0])
        url_list.append(url)
        url_list = list(set(url_list))
    # url = "http://weixin.sogou.com/weixin?type=2&s_from=input&query={keyword}&ie=utf8".format(keyword="北京")
    # url_list.append(url)
    # url_list = list(set(url_list))
    start_urls = url_list

    # def start_requests(self):
    #     cookies = 'SUID=CA234A2F2113940A000000005B737EA2; SUV=00BF55432F4A23CA5B73B904C7988601; ABTEST=5|1534310857|v1; weixinIndexVisited=1; JSESSIONID=aaaGg2voXgwiOfzhMq7tw; sct=7; ppinf=5|1534389335|1535598935|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTUlQjklQjglRTglQkYlOTB8Y3J0OjEwOjE1MzQzODkzMzV8cmVmbmljazoxODolRTUlQjklQjglRTglQkYlOTB8dXNlcmlkOjQ0Om85dDJsdUdxT0JPS1Q5NlA1RWxCb3pzMDYyallAd2VpeGluLnNvaHUuY29tfA; pprdig=WmoMoarzG3Zc-jYFzy7A1ThqA4iad2iIxujarfPNTccGCwUX7-Br-I2s2JsUTsE6g1LOJjRkf4D6QMyILYdJM0gTHD0tyjeCXn8TMqBkSjoi9mtApMCX8zbKs3FXtIL4c723korLfCpObjTW_wUOFPcksnWnHW2SZn-PvljuZo0; sgid=31-36590463-AVt07FeyOWF73PQUmbRa6hk; IPLOC=JP; ppmdig=15344037450000003fd7e333a1ed391ee04f00b0213b5740; PHPSESSID=3i8sl7occ1g2t0j6sbhdqodo30; SUIR=9E771E7B54512727C0F6556F559B013A; SNUID=1FF69EFBD5D0A75C037D480ED578CCE3; successCount=1|Thu, 16 Aug 2018 08:05:53 GMT'
    #     print("start_requests**  "*10)
    #     for url in self.start_urls:
    #         yield scrapy.Request(url,callback=self.parse,cookies={ i.split("=")[0]:i.split("=")[-1] for i in cookies.split("; ")})

    def parse(self, response):
        item=WxSpiderItem()
        print("parse%% "*10)
        li_list = response.xpath("//ul[@class='news-list']/li")
        for li in li_list:
            # 发布时间的时间戳
            time_s = li.xpath(".//div[@class='s-p']/@t").extract_first()
            # 将时间戳转换为日期
            item['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time_s)))
            # 只收录7天之内的信息
            last_time = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M")
            print("1"*20)

            if item['time'] > last_time:
                print(item['time'])
                print(last_time)
                print('2'*20)
                item['title'] = li.xpath("./div[2]/h3/a/text()").extract()
                item['title'] = ''.join(item['title']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\u200b', u' ')
                item['url'] = li.xpath("./div[2]/h3/a/@data-share").extract_first()
                item['url'] = response.urljoin(item['url'])
                print(item['url'])
                item['user_name'] = li.xpath(".//div[@class='s-p']/a/text()").extract_first()
                yield scrapy.Request(item['url'], callback=self.get_content, meta={'item': deepcopy(item)})
        next_url = response.xpath("//a[@id='sogou_next']/@href").extract_first()
        if next_url is not None:
            next_url = response.urljoin(next_url)
            try:
                page = re.search('.*?page=(\d+).*', next_url).group(1)
                print(('第%s页'%(page))*10)
                # 只获取前100页
                if int(page) <= 10:
                    yield scrapy.Request(next_url,callback=self.parse)
            except Exception as e:
                print(e)
        else:
            print("下一页为空"*10)

    def get_content(self,response):
        print('3'*20)
        item = deepcopy(response.meta['item'])
        content = response.xpath("//div[@class='rich_media_content ']/p//text()").extract()
        content = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\u200b', u' ')
        content = remove_tags(content)
        item['content'] = content
        # item['url'] = response.url
        item['create_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        m = hashlib.md5()
        # url = str(item['url'])
        m.update(str(content).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        item['comm_num'] = "0"
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['env_num'] = '0'
        item['media_type'] = '微信公众号'
        # print(item)
        yield item







