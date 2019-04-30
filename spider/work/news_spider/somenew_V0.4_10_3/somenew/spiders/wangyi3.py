# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
import hashlib
from somenew.items import SomenewItem
from copy import deepcopy
import json

# 北京青年报爬虫
class WangyiSpider(scrapy.Spider):
    name = 'wangyi3'
    allowed_domains = ['163.com']
    start_urls = ['https://news.163.com/']
    # custom_settings = {'DOWNLOAD_DELAY': 0.1}


    def parse(self, response):
        # 要闻
        m = ['guonei','guoji','hangkong','wurenji','money','yaowen','dujia','war','tech','jiankang','hangkong','housebeijing','auto','lady','ent','sports']
        for i in range(1,4):
            for j in m:
                if i != 1:
                    url = 'http://temp.163.com/special/00804KVA/cm_{}_0{}.js?callback=data_callback'.format(j,i)
                else:
                    url = 'http://temp.163.com/special/00804KVA/cm_{}.js?callback=data_callback'.format(j)
                yield scrapy.Request(url, callback=self.get_detail)
        #
        n = ['index','stock','biz','licai','fund']
        for i in range(1,8):
                for j in n:
                    if i != 1:
                        url ='http://money.163.com/special/00259BVP/news_flow_{}_0{}.js?callback=data_callback'.format(j,i)
                    else:
                        url = 'http://temp.163.com/special/00804KVA/cm_{}.js?callback=data_callback'.format(j)
                    yield scrapy.Request(url, callback=self.get_detail_url)
        # # 娱乐
        w = ['index', 'star', 'tv', 'show', 'movie', 'music']
        for i in range(1,10):
                for j in w:
                    if i != 1:
                        url ='http://ent.163.com/special/000380VU/newsdata_%s_%02d.js?callback=data_callback'%(j,i)
                    else:
                        url = 'http://ent.163.com/special/000380VU/newsdata_{}.js?callback=data_callback'.format(j)
                    yield scrapy.Request(url, callback=self.get_detail_url)
        # 股票
        z = ['index','usstock','ipo','bitcoin','hkstock','dy']
        for i in range(1,10):
                for j in z:
                    if i != 1:
                        url ='http://money.163.com/special/002557S6/newsdata_gp_%s_%02d.js?callback=data_callback'%(j,i)
                    else:
                        url = 'http://money.163.com/special/002557S6/newsdata_gp_{}.js?callback=data_callback'.format(j)
                    print(url)
                    yield scrapy.Request(url, callback=self.get_detail_url)
        # 商业
        y  = ['shangye','chungtou','guanli','yingxiao','anlie','zhichang','chaoshenghuo','sydl']
        for i in range(1,10):
                for j in y:
                    if i != 1:
                        url ='http://money.163.com/special/002557RF/data_idx_%s_%02d.js?callback=data_callback'%(j,i)
                    else:
                        url = 'http://money.163.com/special/002557RF/data_idx_{}.js?callback=data_callback'.format(j)
                    print(url)
                    yield scrapy.Request(url, callback=self.get_detail_url)

        # # 中国足球
        x = ['index','zhch','yg','gzh','zhj','zxb','hd']
        for i in range(1,10):
                for j in x:
                    if i != 1:
                        url ='http://sports.163.com/special/000587PM/newsdata_china_%s_%02d.js?callback=data_callback'%(j,i)
                    else:
                        url = 'http://sports.163.com/special/000587PM/newsdata_china_{}.js?callback=data_callback'.format(j)
                    print(url)
                    yield scrapy.Request(url, callback=self.get_detail_url)
        # 世界足球
        a = ['gjd','ych','xj','yj','dj','og','ol','gjd']
        for i in range(1,10):
                for j in a:
                    if i != 1:
                        url ='http://sports.163.com/special/000587PN/newsdata_world_%s_%02d.js?callback=data_callback'%(j,i)
                    else:
                        url = 'http://sports.163.com/special/000587PN/newsdata_world_{}.js?callback=data_callback'.format(j)
                    print(url)
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
            print(item)










