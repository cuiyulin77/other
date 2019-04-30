# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 扬子晚报
    name = 'yangziwanbao'
    allowed_domains = ['yangtse.com']
    start_urls = ['http://www.yangtse.com/app/qinggan/','http://www.yangtse.com/app/internet/','http://www.yangtse.com/app/internet/','http://www.yangtse.com/app/ent/','http://www.yangtse.com/app/bzxc/','http://www.yangtse.com/app/education/','http://www.yangtse.com/app/health/','http://www.yangtse.com/app/qinggan/','http://www.yangtse.com/app/qinggan/','http://www.yangtse.com/app/politics/','http://www.yangtse.com/app/livelihood/','http://www.yangtse.com/app/zhengzai/','http://www.yangtse.com/app/jiangsu/kanjiangsu/','http://www.yangtse.com/app/jiangsu/nanjing/']
    custom_settings = {'DOWNLOAD_DELAY': 0.8}
    def parse(self, response):
        res = response.xpath('//div[@class="box-text-title"]/a/@href').extract()
        for url  in res:
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail_url(self,response):
        res = response.xpath('//*[@id="content"]/ul/li/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//div[@class=\"text-title\"]/text()").extract_first()
        item['time'] = response.xpath("//div[@class=\"text-time\"]/text()").extract()[0]
        item['content'] = response.xpath('//*[@id="content"]/p/text()').extract()
        item['come_from'] = response.xpath("//div[@class=\"text-time\"]/text()").extract()[0]
        item['content']= ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').replace( '\r', '').replace( '\r\n', '').strip()
        # print(item)
        if item['content'] and item['title']:
            item['time'] = item['time'].split('\u3000')[1]
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '扬子晚报'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['come_from'] = item['come_from'].split('\u3000')[0].split('来源：')[1]
            yield item


