# -*- coding: utf-8 -*-
import scrapy
from gov_people.items import GovPeopleItem

class JiangsuSpider(scrapy.Spider):
    name = 'jiangsu'
    allowed_domains = ['jiangsu.gov.cn']
    start_urls = ['http://www.jiangsu.gov.cn/col/col31238/index.html']

    def parse(self, response):
        div_list = response.xpath("//div[@class='ld-205']")
        for div in div_list:
            position = div.xpath("./div[@class='ld-zw']/text()").extract_first()
            if position is None:
                position = '副省长'
            li_list = div.xpath("./div[@class='ld-xx']//li")
            for li in li_list:
                item = GovPeopleItem()
                item['name'] = li.xpath("./a/div[2]/text()").extract_first().replace(u"\xa0","")
                item['position'] = position.replace(u'\xa0','')
                item['department'] = '省政府领导'
                item['people_url'] = response.urljoin(li.xpath("./a/@href").extract_first())
                item['province'] = '江苏省'
                item['city'] = ''
                # print(item)
                yield item



