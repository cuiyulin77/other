# -*- coding: utf-8 -*-
import scrapy
from gov_people.items import GovPeopleItem

class HeilongjiangSpider(scrapy.Spider):
    name = 'heilongjiang'
    allowed_domains = ['hlj.gov.cn']
    start_urls = ['http://www.hlj.gov.cn/szf/']

    def parse(self, response):
        sz_div = response.xpath("//div[@class='twolbta']/div[2]")                          # 省长信息
        if sz_div:
            item = GovPeopleItem()
            names = sz_div.xpath("./a/text()").extract_first().split("：")
            item['name'] = names[1]
            item['position'] = names[0]
            item['department'] = '省政府领导'
            item['people_url'] = sz_div.xpath("./a/@href").extract_first()
            item['province'] = '黑龙江省'
            item['city'] = ''
            # print(item)
            yield item
        fsz_li_list = response.xpath("//div[@class='twolbtb']/ul/li")     # 副省长信息
        for li in fsz_li_list:
            item = GovPeopleItem()
            item['name'] = li.xpath("./a/text()").extract_first()
            item['position'] = '副省长'
            item['department'] = '省政府领导'
            item['people_url'] = li.xpath("./a/@href").extract_first()
            item['province'] = '黑龙江省'
            item['city'] = ''
            # print(item)
            yield item
        other_url = response.xpath("//div[@class='twolbbot']/a/@href").extract_first()
        if other_url:
            yield scrapy.Request(other_url,callback=self.other_leader)

    def other_leader(self,response):
        div_list = response.xpath("//div[@class='f000 twolmain']")
        for div in div_list:
            item = GovPeopleItem()
            msg = div.xpath("./div[1]/text()").extract_first().split(' ')
            item['name'] = msg[1]
            item['position'] = msg[0]
            item['department'] = '省政府领导'
            item['people_url'] = ''
            item['province'] = '黑龙江省'
            item['city'] = ''
            # print(item)
            yield item






