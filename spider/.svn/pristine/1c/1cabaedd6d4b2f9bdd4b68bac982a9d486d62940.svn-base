# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json


# =============================================================================
# 晋城新闻网爬虫 首页:
# ===========================================================================


class JinchengxinwenwangSpider(scrapy.Spider):
    name = 'jinchengxinwenwang'
    allowed_domains = ['jcnews.com.cn']
    # start_urls = ['http://www.jcnews.com.cn/stlm/jzx/fc/']
    start_urls = ['http://www.jcnews.com.cn/xw/ms009/','http://www.jcnews.com.cn/xw/jdxw/'\
        ,'http://www.jcnews.com.cn/xw/wbrd001/','http://www.jcnews.com.cn/xw/pl/',\
        'http://www.jcnews.com.cn/lm/tj/','http://www.jcnews.com.cn/xw/jcxw/',\
                  'http://www.jcnews.com.cn/xw/shxw/','http://www.jcnews.com.cn/xw/xqxw/',
                  'http://www.jcnews.com.cn/xw/sxxw/','http://www.jcnews.com.cn/xw/gnxw/',
                  'http://www.jcnews.com.cn/xw/zhxw/','http://www.jcnews.com.cn/stlm/jzx/fc/',
                  'http://www.jcnews.com.cn/stlm/jzx/qc/','http://www.jcnews.com.cn/lm/zx_2017rw/',
                  'http://www.jcnews.com.cn/stlm/jsh/ly/','http://www.jcnews.com.cn/stlm/jsh/ms/',
                  'http://www.jcnews.com.cn/stlm/jwh/wh/','http://www.jcnews.com.cn/stlm/jwh/jy/',
                  'http://www.jcnews.com.cn/stlm/jnl/ms/','http://www.jcnews.com.cn/stlm/jnl/gy/',
                  'http://www.jcnews.com.cn/stlm/jyt/yl/','http://www.jcnews.com.cn/stlm/jyt/ty/']

    def parse(self, response):
        print(len(response.url), response.url)
        res = response.xpath('//ul/li/a/@href').extract()
        for url in res:
            url = response.url+ url.replace('./','')
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)
        # http://www.jcnews.com.cn/xw/jdxw/index_3.html

        for i in range(1,9):
            url = response.url +'index_{}.html'.format(i)
            yield scrapy.Request(url, callback=self.get_detail_url,meta={'url':response.url})

    def get_detail_url(self,response):
        res = response.xpath('//ul/li/a/@href').extract()
        for url in res:
            # http://www.jcnews.com.cn/xw/jdxw/201812/t20181206_480898.html
            url = response.meta['url']+ url.replace('./','')
            print(url)

            yield scrapy.Request(url, callback=self.get_detail)


    def get_detail(self, response):
        item = SomenewItem()
        print(response.url, '我是响应的rul')
        item['title'] = response.xpath('//*[@id="title"]/text()').extract_first()
        try:
            item['time'] = response.xpath('//*[@id="article"]/div[1]/div/span[1]/text()').extract()[0]
        except:
            pass
        # item['content'] = response.xpath('//*[@id="article"]/div[3]/div[2]/div/p|//div[@class="TRS_Editor"]').xpath('string(.)').extract()
        item['content'] = response.xpath('//*[@id="article"]/div[3]/div/span/text()|//*[@id="article"]/div[3]/div[2]/p/text()|//*[@id="article"]/div[3]/div[2]/div/p/text()|//div[@class="TRS_Editor"]/div/text()').extract()
        try:
            item['come_from'] = response.xpath('//*[@id="article"]/div[1]/div/span[2]/text()').extract()[0]
        except:
            pass
        if item['title'] and item['content']:
            item['title'] = item['title'].split('\n')[1].strip()
            item['time'] = item['time'].replace('年', '/').replace('月', '/').replace('日', '')
            item['url'] = response.url
            item['come_from'] =  item['come_from'].split('来源：')[1]
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                             '').replace(
                '\u2002', '').replace('\t', '').replace('\r', '').strip()

            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '晋城新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '晋城'
            item['addr_province'] = '山西省'
            print('晋城新闻网' * 100)
            yield item




