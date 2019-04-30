# -*- coding: utf-8 -*-
import scrapy
from gov_people.items import GovPeopleItem

class LiaoningSpider(scrapy.Spider):
    name = 'liaoning'
    allowed_domains = ['ln.gov.cn']
    start_urls = ['http://www.ln.gov.cn/zfxx/zfld/tyj01/']

    def parse(self, response):
        li_list = response.xpath("//div[@class='l-box-right']/ul/li")
        for li in li_list:
            names = li.xpath("./a/text()").extract_first().split(" ")
            item = GovPeopleItem()
            item['position'] = names[1].replace(u'\u3000','')
            item['department'] = '省政府领导'
            item['name'] = names[0].replace(u'\u3000','')
            item['people_url'] = response.urljoin(li.xpath("./a/@href").extract_first())
            item['province'] = '辽宁省'
            item['city'] = ''
            # print(item)
            yield item
