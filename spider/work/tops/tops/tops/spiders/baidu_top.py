# -*- coding: utf-8 -*-
import scrapy
from tops.items import TopsItem


class BaiduTopSpider(scrapy.Spider):
    name = 'baidu_top'
    allowed_domains = ['baidu.com']
    # 其实总榜在这里http://top.baidu.com/boards?fr=topindex，涉及到各种类别，只是暂时不需要
    start_urls = ['http://top.baidu.com/buzz?b=1/']

    def parse(self, response):
        title_list = response.xpath("//div[@class='hblock']/ul/li")[1:]
        for title in title_list:
            href = title.xpath("./a/@href").extract_first()
            title = title.xpath('./a/@title').extract_first()
            if href:
                href = response.urljoin(href)
                print(href,title)
                yield scrapy.Request(href,callback=self.get_tops)

    def get_tops(self,response):
        print("3"*30)
        top_type = response.xpath("//h2/text()").extract_first()
        print(top_type)
        tr_list = response.xpath("//table[@class='list-table']/tr")[1:]
        # print(tr_list)
        # print(tr_list)
        for tr in tr_list:
            print(tr)
            print('4'*30)
            top_title = tr.xpath(".//a[@class='list-title']/text()").extract_first()
            if top_title:
                item = TopsItem()
                item['top_type'] = top_type
                item['top_title'] = top_title
                item['url'] = tr.xpath(".//a[@class='list-title']/@href").extract_first()
                item['hot_value'] = tr.xpath(".//td[@class='last']/span/text()").extract_first()
                item['media'] = '百度'
                if tr.xpath(".//span[@class='num-top']"):
                    item['top_num'] = tr.xpath(".//span[@class='num-top']/text()").extract_first()
                else:
                    item['top_num'] = tr.xpath(".//span[@class='num-normal']/text()").extract_first()
                # print(item)
                # item['summary'] = ''
                yield item


