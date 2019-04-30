# -*- coding: utf-8 -*-
import scrapy
from gov_people.items import GovPeopleItem

class NeimengSpider(scrapy.Spider):
    name = 'neimeng'
    allowed_domains = ['www.nmg.gov.cn']
    start_urls = ['http://www.nmg.gov.cn/col/col4191/index.html']

    def parse(self, response):
        left_position = response.xpath("//div[@class='zwgk_ldjl_zx_detail left']/div/span/text()").extract_first()  # 左侧职位名称
        if left_position:
            left_position = left_position.replace(":","")
            item = GovPeopleItem()
            item['position'] = left_position
            item['name'] = response.xpath("//div[@class='zwgk_ldjl_zx_detail left']/div/a/text()").extract_first()
            item['people_url'] = response.urljoin(response.xpath("//div[@class='zwgk_ldjl_zx_detail left']/div/a/@href").extract_first())
            item['department'] = '自治区政府'
            item['province'] = '内蒙古'
            item['city'] = ''
            # print(item)
            yield item
        right_div_list = response.xpath("//div[@class='zwgk_ldjl_zx_right left']/div[position()<=2]")
        for div in right_div_list:
            position = div.xpath("./div[1]/text()").extract_first().replace("：","")
            li_list = div.xpath("./div[2]//li")
            if li_list:
                for li in li_list:
                    item = GovPeopleItem()
                    item['position'] = position
                    item['name'] = li.xpath("./a/text()").extract_first()
                    item['people_url'] = response.urljoin(li.xpath("./a/@href").extract_first())
                    item['department'] = '自治区政府'
                    item['province'] = '内蒙古'
                    item['city'] = ''
                    # print(item)
                    yield item
            else:
                item = GovPeopleItem()
                item['position'] = position
                item['name'] = div.xpath("./a/text()").extract_first()
                item['people_url'] = response.urljoin(div.xpath("./a/@href").extract_first())
                item['department'] = '自治区政府'
                item['province'] = '内蒙古'
                item['city'] = ''
                # print(item)
                yield item

