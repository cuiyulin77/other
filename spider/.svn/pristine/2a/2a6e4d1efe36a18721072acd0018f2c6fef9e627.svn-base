# -*- coding: utf-8 -*-
import scrapy
from gov_people.items import GovPeopleItem

class JilinSpider(scrapy.Spider):
    name = 'jilin'
    allowed_domains = ['jl.gov.cn']
    start_urls = ['http://www.jl.gov.cn/szf/']

    def parse(self, response):
        dl_1 = response.xpath("//div[@class='province_list ld_ys_inherit']/dl[1]")
        if dl_1:
            item = GovPeopleItem()
            item['position'] = dl_1.xpath("./dt/text()").extract_first()
            item['name'] = response.xpath("//div[@class='province_list ld_ys_inherit']/div[1]//h2/a/text()").extract_first()
            item['people_url'] = response.urljoin(response.xpath("//div[@class='province_list ld_ys_inherit']/div[1]//h2/a/@href").extract_first())
            item['department'] = '省政府领导'
            item['province'] = '吉林省'
            item['city'] = ''
            # print(1,item)
            yield item
        dl_2 = response.xpath("//div[@class='province_list ld_ys_inherit']/dl[position()=2]")
        if dl_2:
            position = "副省长"
            li_list = response.xpath("//div[@class='province_list ld_ys_inherit']/ul[position()<=2]/li")
            for li in li_list:
                item = GovPeopleItem()
                item['name'] = li.xpath("./a/p/text()").extract_first()
                item['position'] = position
                item['people_url'] = response.urljoin(li.xpath("./a/@href").extract_first())
                item['department'] = '省政府领导'
                item['province'] = '吉林省'
                item['city'] = ''
                # print(2,item)
                yield item
        dl_3 = response.xpath("//div[@class='province_list ld_ys_inherit']/dl[position()=4]")
        if dl_3:
            position = "秘书长"
            li_list = response.xpath("//div[@class='province_list ld_ys_inherit']/ul[position()=3]/li")
            for li in li_list:
                item = GovPeopleItem()
                item['name'] = li.xpath("./a/p/text()").extract_first()
                item['position'] = position
                item['people_url'] = response.urljoin(li.xpath("./a/@href").extract_first())
                item['department'] = '省政府领导'
                item['province'] = '吉林省'
                item['city'] = ''
                # print(3,item)
                yield item
