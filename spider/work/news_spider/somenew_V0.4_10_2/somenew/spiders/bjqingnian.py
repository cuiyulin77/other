# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
import hashlib
from somenew.items import SomenewItem
from copy import deepcopy

# 北京青年报爬虫
class BjqingnianSpider(scrapy.Spider):
    name = 'bjqingnian'
    allowed_domains = ['ynet.com']
    start_urls = ['http://news.ynet.com/list/1700t76.html','http://news.ynet.com/list/990t76.html','http://zixun.ynet.com/web/list.html?cid=12&page=1','http://zixun.ynet.com/web/list.html?cid=18&page=1','http://zixun.ynet.com/web/list.html?cid=8&page=1','http://zixun.ynet.com/web/list.html?cid=26&page=1','http://zixun.ynet.com/web/list.html?cid=23&page=1','http://zixun.ynet.com/web/list.html?cid=13&page=1','http://zixun.ynet.com/web/list.html?cid=24&page=1','http://zixun.ynet.com/web/list.html?cid=25&page=1','http://zixun.ynet.com/web/list.html?cid=27&page=1','http://zixun.ynet.com/web/list.html?cid=29&page=1','http://zixun.ynet.com/web/list.html?cid=30&page=1','http://zixun.ynet.com/web/list.html?cid=11&page=1','http://zixun.ynet.com/web/list.html?cid=19&page=1','http://finance.ynet.com/1760t815.html','http://finance.ynet.com/383t815.html','http://finance.ynet.com/461t815.html','http://finance.ynet.com/464t815.html','http://finance.ynet.com/467t815.html','http://finance.ynet.com/2004t815.html','http://finance.ynet.com/1272t815.html','http://finance.ynet.com/470t815.html',]



    def parse(self, response):
        li_list = response.xpath("//ul[@class='cfix fin_newsList']/li")
        print('1'*100)
        for li in li_list:
            item = SomenewItem()
            item['title'] = li.xpath("./h2/a/text()").extract_first()
            item['time'] = li.xpath(".//em[@class='fRight']/text()").extract_first()
            href = li.xpath("./h2/a/@href").extract_first()
            print('2' * 100)
            yield scrapy.Request(href,callback=self.get_content,meta={'item':deepcopy(item)})
        next_href = response.xpath("//li[@class='active']/a[text()='下一页']/@href").extract_first()
        try:
            next_url_num = int(re.match(r'.*?_(\d+)\.html$', next_href).group(1))
        except:
            next_url_num = 1
        if next_href is not None and (next_url_num <= 5):
            # print('3' * 100)
            yield scrapy.Request(next_href,callback=self.parse)

    def get_content(self,response):
        # print('4' * 100)
        item = response.meta['item']
        item['url'] = response.url
        item['content'] = response.xpath("//div[@id='articleAll']/div/p//text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        item['media'] = '北京青年报'
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        item['comm_num'] = "0"
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['env_num'] = '0'
        yield item





