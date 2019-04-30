# -*- coding: utf-8 -*-
import scrapy
from gov_people.items import GovPeopleItem

class TianjinSpider(scrapy.Spider):
    name = 'tianjin'
    allowed_domains = ['www.tj.gov.cn/szf']
    start_urls = ['http://www.tj.gov.cn/szf/']

    def parse(self, response):
        dl_list = response.xpath("//div[@class='sld_con']/dl")
        for dl in dl_list:
            position = dl.xpath("./dt[1]/text()").extract_first()
            if position:
                position = position.replace(" ","")
                dl_part_list = dl.xpath("./dd/dl")
                print(dl_part_list)
                if dl_part_list:
                    for dl_part in dl_part_list:
                        item = {}
                        item['position'] = position
                        item['department'] = '市政府领导'
                        item['name'] = dl_part.xpath("./dd/a/text()").extract_first()
                        item['people_url'] = dl_part.xpath("./dd/a/@href").extract_first()
                        if item['people_url']:
                            item['people_url'] = response.urljoin(item['people_url'])
                        item['province'] = '天津'
                        item['city'] = '天津'
                        # print(item)
                        yield item
                else:
                    names = dl.xpath("./dd/text()").extract_first()
                    names_list = names.strip().split('　　')
                    for name in names_list:
                        item = GovPeopleItem
                        item['position'] = position
                        item['department'] = '市政府领导'
                        item['name'] = name.replace(u'\u3000','').replace(' ','')
                        item['people_url'] = ''
                        item['province'] = '天津'
                        item['city'] = '天津'
                        # print(item['name'])
                        # print(item)
                        yield item


