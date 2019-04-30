# -*- coding: utf-8 -*-
import scrapy
from chengshi.items import ChengshiItem
from chengshi.util.get_md5 import get_md
import re,time


class Chengshi1Spider(scrapy.Spider):
    name = 'chengshi1'
    allowed_domains = ['chinacity.org.cn']
    start_urls = ['http://www.chinacity.org.cn/Column.aspx?ColId=128','http://www.chinacity.org.cn/csfz/cscx/Index.html'\
        ,'http://www.chinacity.org.cn/csfz/csjj/Index.html','http://www.chinacity.org.cn/csfz/csjs/Index.html'\
        ,'http://www.chinacity.org.cn/csfz/cshj/Index.html','http://www.chinacity.org.cn/csfz/csgl/Index.html'\
        ,'http://www.chinacity.org.cn/csfz/cswh/Index.html','http://www.chinacity.org.cn/csfz/fzzl/Index.html'\
        ,'http://www.chinacity.org.cn/cspp/csyx/Index.html','http://www.chinacity.org.cn/cspp/csch/Index.html'\
        ,'http://www.chinacity.org.cn/cspp/csal/Index.html','http://www.chinacity.org.cn/cspp/cspp/Index.html'\
        ,'http://www.chinacity.org.cn/cspp/csmy/Index.html','http://www.chinacity.org.cn/cspp/lypp/Index.html']


    def parse(self, response):
        print(response.url)
        res = response.xpath('//*[@id="contentList"]/li/span/a/@href').extract()
        for node in res:
            url ='http://www.chinacity.org.cn' + node
            yield scrapy.Request(url,callback=self.detail)

    def detail(self,response):
        item = ChengshiItem()
        item['title'] = response.xpath("//div[@style=\"TEXT-ALIGN: center\"]/div[1]/text()").extract_first()
        item['url'] = response.url
        item['article_id'] = get_md(response.url)
        item['keyid'] = ''
        item['media'] = response.xpath("//div[@style=\"FONT-SIZE: 12px\"]/text()").extract()[0].split('来源：')[1].split( )[0]
        item['classid'] ='168'
        item['writer'] = response.xpath("//div[@style=\"FONT-SIZE: 12px\"]/text()").extract()[0].split('来源：')[0].split('作者：')[1].replace('\xa0\xa0','  ')
        item['titlepic'] = ''
        item['newstime'] = response.xpath("//div[@style=\"FONT-SIZE: 12px\"]/text()").extract()[0].split('来源：')[1].split('添加日期：')[1].replace('19年','2019-').replace('月','-').replace('日','  ')+'00:00'
        timeArray = time.strptime(item['newstime'], "%Y-%m-%d %H:%M")
        item['newstime'] = int(time.mktime(timeArray))
        item['content'] = response.xpath("//div[@style=\"MARGIN-TOP: 20px; LINE-HEIGHT: 25px\"]/child::*").extract()
        t =''
        for i in item['content']:
            t += i.replace('\xa0','&nbsp;')
        item['content'] =t
        yield item
        print(t,111111111111111111111111111111111111111111111111111111111111111111)
        print(item)

