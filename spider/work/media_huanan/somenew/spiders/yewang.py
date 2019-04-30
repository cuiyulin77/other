import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime,json

class DezhouxinwenSpider(scrapy.Spider):
    # 椰网
    name = 'yewang'
    allowed_domains = ['hndnews.com']
    start_urls = ['http://www.hndnews.com/16/1.html','http://www.hndnews.com/19/1.html','http://www.hndnews.com/18/1.html','http://www.hndnews.com/22/1.html','http://www.hndnews.com/23/1.html','http://www.hndnews.com/20/1.html','http://www.hndnews.com/61/1.html','http://www.hndnews.com/17/1.html','http://www.hndnews.com/14/1.html','http://www.hndnews.com/15/1.html','http://www.hndnews.com/','http://www.hndnews.com/2/1.html','http://www.hndnews.com/33/1.html','http://www.hndnews.com/36/1.html','http://www.hndnews.com/12/1.html','http://www.hndnews.com/3/1.html','http://www.hndnews.com/4/1.html','http://www.hndnews.com/34/1.html']
    def parse(self, response):
        res = response.xpath('//div[@class="news-img-list"]/li/div[1]/a/@href').extract()
        for i in res:
            url = 'http://www.hndnews.com'+i
            yield scrapy.Request(url, callback=self.get_detail)
        for i in range(2,10):
            url = response.url[:-6]+'{}.html'.format(i)
            yield scrapy.Request(url, callback=self.get_detail_url)
    def get_detail_url(self,response):
        res = response.xpath('//div[@class="news-img-list"]/li/div[1]/a/@href').extract()
        for i in res:
            url = 'http://www.hndnews.com'+i
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        item = SomenewItem()
        item['title'] = response.xpath('//h1[@class="title"]/text()').extract()[0]
        item['time'] = response.xpath('//div[@class="desc"]/text()').extract()
        item['content'] = response.xpath('//*[@id="detail_file"]/p/text()').extract()
        try:
            item['come_from'] = response.xpath('//div[@class="desc"]/a/text()').extract()[0]
        except:
            pass
        item['time'] = ''.join(item['time']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                          '').replace(
            '\u2002', '').replace('\r', '').replace('\r\n', '').strip()
        item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                          '').replace(
            '\u2002', '').replace('\r', '').replace('\r\n', '').strip()
        # print(item)
        if item['content'] and item['title']:
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '椰网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '海南'
            print(item)

            # yield item