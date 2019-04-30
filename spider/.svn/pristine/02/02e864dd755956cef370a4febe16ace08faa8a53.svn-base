# -*- coding: utf-8 -*-
import scrapy
import hashlib
import datetime
from somenew.items import SomenewItem


class ShunwangSpider(scrapy.Spider):
    name = 'shunwang'
    allowed_domains = ['e23.cn']
    start_urls = ['http://www.e23.cn/','http://news.e23.cn/','http://news.e23.cn/index.html,http://news.e23.cn/jinan/']

    def parse(self, response):

        res  = response.xpath('//div[@class="article-list"]/div[@class="article"]/h3/a/@href|//ul[@class=\"list\"]/li/a/@href|//div[@class=\"article\"]/a/@href').extract()
        res2 = response.xpath('//div[@class="datt"]/div/h1/a/@href|//div[@class="jbcontent"]/div/h3/a/@href').extract()
        res4 = response.xpath('//div[@class="navl_k"]/a/@href').extract()
        res5 = response.xpath('/html/body/div/div[3]/div[1]/div[2]/div[1]/div/h4/@href|//div[@class="section"]/div/div/ul/li/a/@href').extract()
        for i in (res,res2):
            if i:
                for url in i :
                    yield scrapy.Request(url, callback=self.get_detail_url_list,dont_filter=True)
        if res4:
            for i in res4:
                url ='http://news.e23.cn'+i.split('.')[0]+'.html'
                print(url,(len(res4)))
                yield scrapy.Request(url, callback=self.get_detail_url_list)
        if res5:
            for i in res5:
                try:
                    yield scrapy.Request(i, callback=self.get_detail)
                except:
                    pass

    def get_detail_url_list(self,response):
            res = response.xpath('//div[@class="article-list"]/div/h4/a/@href').extract()
            for i in res:
                print(i,'1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111')
                yield scrapy.Request(i, callback=self.get_detail,dont_filter=True)



    def get_detail(self,response):
        item = SomenewItem()
        print(response.url)
        item['title'] = response.xpath('//div[@class="post_content_main"]/h1/text()|//div[@class="news_container"]/h1/text()|/html/body/div[1]/div[2]/div[3]/div[1]/div/h1/text()').extract_first()
        item['time'] = response.xpath("//div[@class=\"post_time\"]/p[1]/text()|//div[@class=\"artInfo h12\"]/span[2]/text()|/html/body/div[1]/div[2]/div[3]/div[1]/div/div[1]/p[1]/text()").extract_first()
        item['url'] = response.url
        item['content'] = response.xpath('//div[@class="h16"]/p/text()|//*[@id="zhw"]/p/text()|//*[@id="zhw"]/p/text()').extract()
        if item['content']:
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n','').replace('\u2002', '').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '舜网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['come_from'] = response.xpath('//div[1]/div/div[2]/p[2]/a/text()').extract_first()
            item['addr_province'] = '山东省'
            item['addr_city'] = '济南'
            yield item
