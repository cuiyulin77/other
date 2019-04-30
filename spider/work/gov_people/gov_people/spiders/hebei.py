# -*- coding: utf-8 -*-
import scrapy
from gov_people.items import GovPeopleItem


class HebeiSpider(scrapy.Spider):
    name = 'hebei'
    allowed_domains = ['www.hebei.gov.cn']
    start_urls = ['http://www.hebei.gov.cn/hebei/11937442/10756074/13769863/index.html']

    def parse(self, response):
        li_list = response.xpath("//div[@class='left_zhong']/ul/li")
        for li in li_list:
            names = li.xpath("./a/text()").extract_first().split(' ')
            item = GovPeopleItem()
            item['name'] = names[1]
            item['position'] = names[0]
            item['department'] = '省政府领导'
            item['province'] = '河北省'
            item['city'] = ''
            item['people_url'] = response.urljoin(li.xpath("/a/@href").extract_first())
            # print(item)
            yield item
