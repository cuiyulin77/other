# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import datetime
import hashlib

class HuanqiuSpider(scrapy.Spider):
    name = 'huanqiu'
    allowed_domains = ['huanqiu.com']
    # http://china.huanqiu.com/article/国内； http://world.huanqiu.com/article/index.html,国际; http://taiwan.huanqiu.com/article/,台海;
    # http://mil.huanqiu.com/world/index.html,军事；
    start_urls = ['http://china.huanqiu.com/article/','http://world.huanqiu.com/article/index.html','http://taiwan.huanqiu.com/article/','http://mil.huanqiu.com/world/index.html',]

    def parse(self, response):
        # h获得此页所有新闻的链接
        href_list = response.xpath("//div[@class='fallsFlow']/ul/li/h3/a/@href").extract()
        for href in href_list:
            yield scrapy.Request(href,callback=self.get_content)
        # 获取下一页url
        next_url = response.xpath("//div[@id='pages']/a[text()='下一页']/@href").extract_first()
        # 获取当前页的页码，因为最多只能获取30页内容，30页以上只显示第30页。超过第30页停止获取
        now_page = response.url
        now_page_num = re.match(r".*?(\d+)\.html$",now_page).group(1)
        if int(now_page_num) < 10:
            yield scrapy.Request(next_url,callback=self.parse)




    def get_content(self,response):
        item=SomenewItem()
        item['title'] = response.xpath("//div[@class='l_a']/h1/text()").extract_first()
        item['time'] = response.xpath("//div[@class='la_tool']/span/text()").extract_first()
        item['url'] = response.url
        item['content'] = response.xpath("//div[@class='la_con']/p/text()").extract()
        item['media'] = '环球网'
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        yield item
