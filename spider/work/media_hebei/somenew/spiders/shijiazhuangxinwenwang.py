# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime


class ShijiazhuangxinwenwangSpider(scrapy.Spider):
    name = 'shijiazhuangxinwenwang'
    allowed_domains = ['sjzdaily.com.cn']
    start_urls = ['http://www.sjzdaily.com.cn/newscenter/node_7.htm','http://www.sjzdaily.com.cn/newscenter/node_6.htm','http://www.sjzdaily.com.cn/newscenter/node_8.htm','http://www.sjzdaily.com.cn/newscenter/node_17.htm']

    def parse(self, response):
        res = response.xpath('/html/body/div/div[5]/div[1]/div/ul/li/a/@href').extract()
        for url in res:
            url = 'http://www.sjzdaily.com.cn/newscenter/'+url
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self, response):
            print(response.url, '我是响应的rul')
            item = SomenewItem()
            try:
                item['title'] = response.xpath('//div[1]/h2/text()').extract()[0].strip()
            except:
                pass
            item['time'] = response.xpath('//div[@class="info"]/text()').extract()
            item['come_from'] = '石家庄新闻网'
            item['content'] = response.xpath('/html/body/div/div[5]/div[1]/div[1]/div[5]/p/text()|//div[1]/div/div/p/text()').extract()
            if item['title'] and item['content']:
                for i in item['time']:
                    data = re.findall(r'(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})', i)
                    if data:
                        item['time'] = data[0]
                item['url'] = response.url
                item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                                 '').replace(
                    '\u2002', '').replace('\t', '').replace('\r', '').strip()
                m = hashlib.md5()
                m.update(str(item['url']).encode('utf8'))
                item['article_id'] = m.hexdigest()
                item['media'] = '石家庄新闻网'
                item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                item['comm_num'] = "0"
                item['fav_num'] = '0'
                item['read_num'] = '0'
                item['env_num'] = '0'
                item['media_type'] = '网媒'
                item['addr_province'] = '河北省'
                item['addr_city'] = '河北省'
                print('石家庄新闻网' * 100)
                yield item
