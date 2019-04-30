# -*- coding: utf-8 -*-
import scrapy
import re
from gov_people.items import GovPeopleItem


class BeijingSpider(scrapy.Spider):
    name = 'beijing'
    allowed_domains = ['shilingdao.beijing.gov.cn']
    start_urls = ['http://shilingdao.beijing.gov.cn/']

    def parse(self, response):
        div_list = response.xpath("//div[@class='main']")
        for div in div_list:
            department = div.xpath(".//h5/text()").extract_first()
            href_list = div.xpath(".//div[@class='ld_list clearfix']//a/@href").extract()
            for href in href_list:
                url = response.urljoin(href)
                if url:
                    yield scrapy.Request(url,callback=self.parse_detai,meta={"department":department})

    def parse_detai(self,response):
        department = response.meta['department']
        title = response.xpath("//title/text()").extract_first()
        name_and_position = title.replace("-领导-首都之窗-北京市政务门户网站","").split('-')
        item = GovPeopleItem()
        item['name'] = name_and_position[0]
        item['position'] = name_and_position[1]
        item['province'] = '北京'
        item['city'] = '北京'
        item['department'] = department
        item['people_url'] = response.url
        # print(item)
        yield item

