# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
import hashlib
from somenew.items import SomenewItem
from copy import deepcopy
import json

class WangyiSpider(scrapy.Spider):
    name = 'wangyi1'
    allowed_domains = ['163.com']
    start_urls = ['https://news.163.com/']
    # custom_settings = {'DOWNLOAD_DELAY': 0.1}


    def parse(self, response):

    #
        # NBA
        b= ['index','hj','ketr','qsh','ysh','okc','huren','mc']
        for i in range(1,10):
                for j in b:
                    if i != 1:
                        url ='http://sports.163.com/special/000587PK/newsdata_nba_%s_%02d.js?callback=data_callback'%(j,i)
                    else:
                        url = 'http://sports.163.com/special/000587PK/newsdata_nba_{}.js?callback=data_callback'.format(j)
                    print(url)
                    yield scrapy.Request(url, callback=self.get_detail_url)

        # 体育综合
        c= ['index','wq','sch','yy','ppq','ymq','bj','tq','pq','tj','ts','bx','qt']
        for i in range(1,10):
                for j in c:
                    if i != 1:
                        url ='http://sports.163.com/special/000587PQ/newsdata_allsports_%s_%02d.js?callback=data_callback'%(j,i)
                    else:
                        url = 'http://sports.163.com/special/000587PQ/newsdata_allsports_{}.js?callback=data_callback'.format(j)
                    print(url)
                    yield scrapy.Request(url, callback=self.get_detail_url)
        # 教育
        c= ['index','wq','sch','yy','ppq','ymq','bj','tq','pq','tj','ts','bx','qt']
        for i in range(1,10):
                for j in c:
                    if i != 1:
                        url ='http://sports.163.com/special/000587PQ/newsdata_allsports_%s_%02d.js?callback=data_callback'%(j,i)
                    else:
                        url = 'http://sports.163.com/special/000587PQ/newsdata_allsports_{}.js?callback=data_callback'.format(j)
                    print(url)
                    yield scrapy.Request(url, callback=self.get_detail_url)
        # # 电影
        a= ['index','chinese','oversea','comment']
        for i in range(1,10):
            for j in a:
                if i != 1:
                    url = 'http://ent.163.com/special/000380VU/newsdata_%s_%02d.js?callback=data_callback'%(j,i)
                else:
                    url = 'http://ent.163.com/special/000381Q1/newsdata_{}.js?callback=data_callback'.format(j)
                yield scrapy.Request(url, callback=self.get_detail_url)
        #      音乐
        for i in range(1,10):
                if i != 1:
                    url = 'http://ent.163.com/special/000381P3/newsdata_tv_workshop_%02d.js?callback=data_callback'%i
                else:
                    url = 'http://ent.163.com/special/000381P3/newsdata_tv_workshop.js?callback=data_callback'
                yield scrapy.Request(url, callback=self.get_detail_url)
        #  科技
        for i in range(1,10):
                if i != 1:
                    url = 'http://tech.163.com/special/00097UHL/tech_datalist_%02d.js?callback=data_callback'%i
                else:
                    url = 'http://tech.163.com/special/00097UHL/tech_datalist.js?callback=data_callback'
                yield scrapy.Request(url, callback=self.get_detail_url)

        # 数码
        for i in range(1,10):
                if i != 1:
                    url = 'http://digi.163.com/special/index_datalist_%02d/?callback=data_callback'%i
                else:
                    url = 'http://digi.163.com/special/index_datalist/?callback=data_callback'
                yield scrapy.Request(url, callback=self.get_detail_url)
    #     旅游
        for i in range(1,10):
                if i != 1:
                    url = 'http://travel.163.com/special/00067VEJ/newsdatas_travel_%02d.js?callback=data_callback'%i
                else:
                    url = 'http://travel.163.com/special/00067VEJ/newsdatas_travel.js?callback=data_callback'
                yield scrapy.Request(url, callback=self.get_detail_url)

        # # 教育
        q= ['hot','liuxue','yimin','en','daxue','gaokao']
        for i in range(1,10):
            for j in q:
                if i != 1:
                    url = 'http://edu.163.com/special/002987KB/newsdata_edu_%s_%02d.js?callback=data_callback'%(j,i)
                else:
                    url = 'http://edu.163.com/special/002987KB/newsdata_edu_{}.js?callback=data_callback'.format(j)
                yield scrapy.Request(url, callback=self.get_detail_url)

    def get_detail_url(self,response):

        res1 = response.body.decode(encoding='gb18030')
        res2 = res1.replace('data_callback(','').strip(')')
        try:
            res3 = json.loads(res2)
            for node in res3:
                print(node['docurl'])
                yield scrapy.Request(node['docurl'], callback=self.get_detail)
        except:
            print(response.url,'111111111111111111111111111111111111111111111111111111111111111111111111111')
            print('可能没有数据','2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222')

    def get_detail(self,response):
        item=SomenewItem()
        item['title'] = response.xpath("//*[@id=\"epContentLeft\"]/h1/text()").extract_first()
        item['media'] = "网易"
        item['time'] = response.xpath("//*[@id=\"epContentLeft\"]/div[1]/text()[1]").extract_first()
        item['content'] = response.xpath("//*[@id=\"endText\"]/p/text()").extract()
        item['come_from']= response.xpath("//*[@id=\"ne_article_source\"]/text()").extract_first()
        print(response.url,'我是响应的rul')
        if item['title'] and item['content']:
            item['time'] = item['time'].split('\u3000')[0].strip('\n').strip()
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '网易'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '全国'
            print('网易'*100)
            yield item










