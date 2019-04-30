# -*- coding: utf-8 -*-
import scrapy
from gov_people.items import GovPeopleItem


# 山西政府官员爬虫

class ShanxiSpider(scrapy.Spider):
    name = 'shanxi'
    allowed_domains = ['shanxi.gov.cn/szf']
    start_urls = ['http://shanxi.gov.cn/szf/']

    def parse(self, response):
        li_list = response.xpath("//ul[@class='provincial-leaders-inner oflow-hd']/li")
        for li in li_list:
            position = li.xpath("./div/text()").extract_first()
            position = position.replace(u"\xa0","")
            dl_list = li.xpath("./dl")
            for dl in dl_list:
                item = GovPeopleItem()
                item['people_url'] = dl.xpath("./dd/a/@href").extract_first()
                item['people_url'] = response.urljoin(item['people_url'])
                item['name'] = dl.xpath("./dd/a/text()").extract_first().replace(u"\u3000","")
                item['province'] = '山西省'
                item['city'] = ''
                item['department'] = '省政府领导'
                item['position'] = position
                # print(item)
                yield item

