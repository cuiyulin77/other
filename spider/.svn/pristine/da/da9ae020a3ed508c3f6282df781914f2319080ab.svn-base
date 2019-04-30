# -*- coding: utf-8 -*-
import scrapy
import hashlib
import datetime
from somenew.items import SomenewItem


class LiaochengxinwenSpider(scrapy.Spider):
    name = 'liaochengxinwen'
    allowed_domains = ['lcxw.cn']
    start_urls = ['http://www.lcxw.cn/','http://news.lcxw.cn/','http://news.lcxw.cn/liaocheng/','http://news.lcxw.cn/liaocheng/xianyu/','http://news.lcxw.cn/liaocheng/yc/','http://tsxz.lcxw.cn/']

    def parse(self, response):
        # 主页
        if 'www' in response.url:
            res = response.xpath('//ul/li/a/@href|//div[@class="tuwen-show"]/h3/a/@href').extract()
            for url in res:
                if '/zt/' not in url and 'ilc' not in url and 'forum.php?'not in url and '//zp'not in url and '//tv' not in url  and 'ztc' not in url:
                    yield scrapy.Request(url, callback=self.get_detail)
        # 新闻页面
        if 'news' in response.url:
            res = response.xpath('//div[not(@id="nav")]/ul[not(@class="clearfix")]/li/a/@href').extract()
            for url in res:
                print(url)
                yield scrapy.Request(url, callback=self.get_detail)
        # # 新闻页面下面的聊城，原创，县域
        if len(response.url)>29:
            url = response.xpath('//*[@id="newsList"]/ul/li/a/@href').extract()
            for url_list in url:
                yield scrapy.Request(url_list, callback=self.get_detail)
            for i in range(2,20):
                url = response.url+'index_{}.html'.format(i)
                yield scrapy.Request(url, callback=self.get_detail_url)
        # # 新闻页面下面的聊城的特色小镇
        if 'tsxz' in response.url:
            res = response.xpath('//td[not(@align="center") and not(@align="right")]/a/@href').extract()
            for url in res:
                yield scrapy.Request(url, callback=self.get_detail)



    def get_detail_url(self,response):
        url_list= response.xpath('//*[@id="newsList"]/ul/li/a/@href').extract()
        for url in url_list:
            print(url,'我是详情页的30个url')
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url)
        item = SomenewItem()

        title  = response.xpath("//div/h1/text()|//div[@class=\"title\"]/div/text()").extract()

        try:
            time  = response.xpath('//div[@class="info"]/span[2]/text()|//div[@class="box_l"]/div[2]/text()|//div[@class="content_info"]/text()').extract_first()
            if len(time) == 23:
                item['time'] = time.split('时间：')[1]
            item['time'] = time.split('\u3000')[0].strip()
        except:
            item['time'] = None

        content = response.xpath('//*[@id="divcontent"]/p/text()|//*[@id="divcontent"]/p/span/span/text()|//div[@class="brief"]/p/text()|//*[@id="divcontent"]/p/span/text()|//*[@id="divcontent"]/div/text()|//*[@id="endText"]/p/text()').extract()
        #
        if content and item['time'] and title:
            item['url'] = response.url
            item['title'] = ''.join(title).strip()
            item['content'] = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                           '').replace(
            '\u2002', '').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '聊城新闻'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['come_from'] =response.xpath("//div/div[@class=\"box_l\"]/div[2]/a/text()").extract_first()
            item['addr_province'] = '山东省'
            item['addr_city'] = '济宁'
            yield item
