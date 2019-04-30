# -*- coding: utf-8 -*-
import scrapy
import hashlib
import datetime
from somenew.items import SomenewItem


class LingyizaixianSpider(scrapy.Spider):
    name = 'lingyizaixian'
    allowed_domains = ['lywww.com']
    start_urls = ['http://www.lywww.com/','http://meili.lywww.com/lybd/xq/','http://meili.lywww.com/gngj/ms/','http://meili.lywww.com/lybd/fz/','http://meili.lywww.com/lybd/qm/','http://meili.lywww.com/lybd/cs/','http://meili.lywww.com/lybd/wybl/','http://meili.lywww.com/lybd/hd/','http://meili.lywww.com/lybd/rw/']

    def parse(self, response):
        res = response.xpath('//*[@id="tuijianc"]/ul/li/a/@href|//*[@id="hdbgtop"]/div[6]/div[2]/div/div/div/ul/li/a/@href').extract()
        res1 = response.xpath('//div[@class="article_list"]/ul/li/a/@href').extract()
        print(len(response.url))
        if len(response.url) == 21:
            for url in res:
                if 'health' not in url and 'lvyou' not in url:
                    yield scrapy.Request(url, callback=self.get_detail)
        elif response.url  in ('http://meili.lywww.com/lybd/cs/','http://meili.lywww.com/lybd/xq/'):
            for i in range(2,7):
                url ='http://meili.lywww.com/lybd/xq/{}.html'.format(i)
                yield scrapy.Request(url, callback=self.get_detail_url)
        else:
            for url in res1:
                url = 'http://meili.lywww.com/'+url
                print(url,'我是发送的url')
                yield scrapy.Request(url, callback=self.get_detail)

    def get_detail_url(self,response):
        res1 = response.xpath('//div[@class="article_list"]/ul/li/a/@href').extract()
        for url in res1:
            url = 'http://meili.lywww.com/' + url
            print(url, '我是发送的url')
            yield scrapy.Request(url, callback=self.get_detail)


    def get_detail(self,response):
        print(response.url)
        item = SomenewItem()
        item['content'] = response.xpath('//*[@id="zh_content"]/div/text()|//*[@id="zh_content"]/text()|//*[@id="zh_content"]/div[1]/div/text()|//*[@id="zh_content"]/p/text()|//div[@class="works_con2"]/div[2]/*/text()').extract()
        item['title'] = response.xpath('//div[@class="one_news"]/h3/text()|//div[@class="one_news"]/h3/text()|/html/body/div[6]/div[1]/div[2]/h3/text()').extract()
        item['time'] = response.xpath('//div[2]/p/text()').extract_first()
        if  item['title'] and item['content'] and item['time']:
            item['time'] = item['time'].split(' 来源：')[0]
            item['title'] = ''.join(item['title']).replace('\n','').replace('\t','').replace('\u3000','').replace('\r','')
            item['content'] = ''.join(item['content']).replace('\u3000','').replace('\ufeff','').replace('\xa0','').replace('\n','').replace('\t','').replace('\r','').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '临沂在线'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['come_from'] =response.xpath("/html/body/div[5]/div[1]/div[2]/p/font[1]/text()").extract_first()
            item['addr_province'] = '山东省'
            item['addr_city'] = '临沂'
            yield item

