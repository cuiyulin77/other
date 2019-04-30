# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime,re

class DezhouxinwenSpider(scrapy.Spider):
    # 中国安徽网
    name = 'zhongguoanhuiwang'
    allowed_domains = ['anhuinews.com']
    start_urls= ['http://www.anhuinews.com/']
    custom_settings = {'DOWNLOAD_DELAY': 1.2}
    def parse(self, response):
        xp='/html/body/div[1]/div/div/div/ul/li/a/@href|/html/body/div[1]/div[15]/div[1]/div[2]/h1/a/@href\
           |//*[@id]/li/a/@href|/html/body/div[1]/div[15]/div[2]/div[3]/div[3]/div[2]/div/ul/li/a/@href\
           |//*[@id]/dl/dt/a/@href|//*[@id]/dl/dd/ul/li/a/@href|//*[@id]/ul/li/a/@href\
           |/html/body/div/div/div/dl/dt/a/@href|/html/body/div[6]/div[1]/div/dl/dd/ul/li/a/@href\
           |/html/body/div[6]/div/div/ul/li/a/@href|/html/body/div/div/div/dl/dd/ul/li/a/@href\
           |/html/body/div[7]/div/div/ul/li/a/@href|/html/body/div[8]/div/div/ul/li/a/@href'
        res = response.xpath(xp).extract()
        for url in res:
            if 'shtml'in url and 'ahsjb' not in url:
                print(url)
                yield scrapy.Request(url,callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//div[@class=\"fl cola\"]/h1/text()|//td[@background]/table[2]/tr[1]/td/span|//div[@class=\"cola\"]/h1/text()|//div[@class=\"g-in\"]/*//h1/text()|//div[@class=\"fl\"]/h1/text()").extract_first()
        item['time'] = response.xpath("/html/body/div[5]/div[1]/div[2]/div[1]/text()|//div[@class=\"source\"]/text()[1]|//div[@class=\"fl\"]/text()").extract()
        item['come_from'] = '中安在线'
        print(len(item['come_from']))
        item['content'] = response.xpath('//div[@class="info"]/p/text()').extract()
        # print(item)
        if item['content'] and item['time'] and item['title']:
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').strip()
            item['time'] = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", item['time'][0])[0]
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '中国安徽网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '安徽'
            print(item)
            yield item


