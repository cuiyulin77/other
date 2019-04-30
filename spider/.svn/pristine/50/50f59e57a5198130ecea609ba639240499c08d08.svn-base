# -*- coding: utf-8 -*-
import scrapy
from gov_people.items import GovPeopleItem

# 上海政府领导爬虫,还有一些分支机构的领导没有爬取

class ShanghaiSpider(scrapy.Spider):
    name = 'shanghai'
    allowed_domains = ['shanghai.gov.cn']
    start_urls = ['http://www.shanghai.gov.cn/shanghai/ldmdjfg.html']

    def parse(self, response):
        p_list = response.xpath("//div[@id='Tab1-1']/p[position()<=3]")
        for p in p_list:
            position = p.xpath("./text()").extract_first().replace('：','').replace(' ','')
            # print(position)
            a_list = p.xpath("./a")
            for a in a_list:
                item = GovPeopleItem()
                item['name'] = a.xpath("./text()").extract_first().replace(u'\u3000','')
                item['people_url'] = a.xpath("./@href").extract_first()
                item['position'] = position
                item['department'] = "市政府领导"
                item['province'] = '上海'
                item['city'] = '上海'
                # print(item)
                yield item
        p_list2 = response.xpath("//div[@id='Tab1-1']/p[position()=4 or position()=5]")
        for p in p_list2:
            # \xa0 \u3000
            p_str = p.xpath("./text()").extract_first().split('：')
            position2 = p_str[0]
            name_list = p_str[1].replace(u'\u3000','').split(u"\xa0\xa0\xa0\xa0\xa0")
            for name in name_list:
                item = GovPeopleItem()
                item['name'] = name
                item['people_url'] = ''
                item['position'] = position2
                item['department'] = "市政府领导"
                item['province'] = '上海'
                item['city'] = '上海'
                # print(item)
                yield item



