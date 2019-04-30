# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 浙江在线
    name = 'zhejiangzaixian'
    allowed_domains = ['zjol.com.cn']
    start_urls =['http://zjnews.zjol.com.cn/zjnews/zjxw/','http://opinion.zjol.com.cn/bwgd/','http://china.zjol.com.cn/gnxw/','http://china.zjol.com.cn/gnxw/','http://py.zjol.com.cn/pyxw/','http://py.zjol.com.cn/zjsj/','http://zjnews.zjol.com.cn/gaoceng_developments/','http://zjnews.zjol.com.cn/ztjj/zt/']
    def parse(self, response):
        res = response.xpath('//*[@id="main"]/div[1]/ul/li/a/@href').extract()
        for url in res:
            url = 'http://'+url.split('//')[1]
            yield scrapy.Request(url,callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//div[@class=\"contTit\"]/font/text()|//div[@class=\"contTit\"]/text()").extract_first()
        item['time'] = response.xpath("//*[@id=\"pubtime_baidu\"]/text()").extract()
        item['content'] = response.xpath('//div[@class="contTxt"]/div[1]/*//text()|//*[@id="main"]/div[1]/*//p/text()').extract()
        if item['content'] and item['time'] and item['title']:
            try:
                item['time'] = item['time'][1].strip('\n').replace('年','/').replace('月','/').replace('年',' ')
            except:
                item['time'] =item['time'].replace('年','/').replace('月','/').replace('年',' ')
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '浙江在线'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            try:
                item['come_from'] =response.xpath('//*[@id="source_baidu"]/text()').split('来源')[1]
            except:
                item['come_from'] = '浙江在线'
            item['addr_province'] = '浙江'
            yield item


