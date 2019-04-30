# -*- coding: utf-8 -*-
import scrapy
import datetime
import hashlib
from somenew.items import SomenewItem


# 第一财经爬虫
class YicaiSpider(scrapy.Spider):
    name = 'yicai'
    allowed_domains = ['yicai.com']
    url_list = []
    for i in range(10)[1:]:
        url = 'http://www.yicai.com/api/ajax/NsList/' + str(i) + '/77'
        url_list.append(url)
    start_urls = url_list

    def parse(self, response):
        cookies = 'yu_id=55ce0e7cbffe40adbda8f66105de219c; _ga=GA1.2.1005902933.1526714183; Hm_lvt_80b762a374ca9a39e4434713ecc02488=1526714183,1526881704; _gid=GA1.2.1939170741.1526881704; acw_tc=AQAAAI7PI2vrOwoARFaO2xDKmhf5+QSp; return_url=http%3A%2F%2Fwww.yicai.com%2Fnews%2F; Hm_lpvt_80b762a374ca9a39e4434713ecc02488=1526889929; _gat_gtag_UA_8382245_3=1; _gat_gtag_UA_106493205_1=1'
        # print("1"*200)
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse_detail,
                cookies={i.split("=")[0]: i.split("=")[-1] for i in cookies.split("; ")}
            )

    def parse_detail(self,response):
        # print("2"*200)
        page_href = response.xpath("//dl/dt/a/@href").extract()
        for href in page_href:
            yield scrapy.Request(href,callback=self.get_content)

    def get_content(self,response):
        item=SomenewItem()
        item['title'] = response.xpath("//div[@class='m-title f-pr']/h1/text()").extract_first()
        item['time'] = response.xpath("//h2/span[2]/text()").extract_first()
        item['media'] = '第一财经'
        item['url'] = response.url
        item['content'] = response.xpath("//div[@class='m-text']//p//text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
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









