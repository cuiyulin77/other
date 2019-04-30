# -*- coding: utf-8 -*-
import scrapy


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.com']
    # start_urls = ['http://weibo.com/']
    #
    # def parse(self, response):
    #     fensi_num = response.xpath('(//a[@class=\"t_link S_txt1\"])[2]/strong/text()').extract_first()
    #     # 粉丝数量 ： response.xpath("(//a[@class='t_link S_txt1'])[2]/strong/text()").extract_first()
    #     pass

    def start_requests(self):
        url = 'http://www.renren.com/PLogin.do'

        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url = url,
            formdata = {"email" : "xxx", "password" : "xxxxx"},
            callback = self.parse
        )
    def parse(self, response):
        # do something
        pass