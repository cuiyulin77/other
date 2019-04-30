# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class ZhejiangzaixianSpider(scrapy.Spider):
    name = 'zhejiangzaixian'
    allowed_domains = ['zjol.com.cn']
    start_urls = [
                  'http://china.zjol.com.cn/gjxw/','http://china.zjol.com.cn/gat/','http://china.zjol.com.cn/gnxw/','http://green.zjol.com.cn/','http://society.zjol.com.cn/','http://fin.zjol.com.cn/'
    ]

    def parse(self, response):
        page_list = response.xpath("//span[@class='fenye']/div/a[contains(text(),'下一页')]/@href").extract()
        page_list.append(response.url)
        for url in page_list:
            url = response.urljoin(url)
            yield scrapy.Request(url,callback=self.get_url)

    def get_url(self,response):
        url_list = response.xpath("//ul[@class='listUl']/li/a/@href").extract()
        for url in url_list:
            yield scrapy.Request(url,callback=self.get_content)

    def get_content(self,response):
        item = SomenewItem()
        item['title'] = response.xpath("//div[@class='contTit']/text()").extract_first()
        time = response.xpath("//span[@id='pubtime_baidu']/text()").extract_first()
        if time is None:
            time = response.xpath("//div[@class='time']/span[1]/text()").extract_first()
        item['time'] = time.replace('年','/').replace('月','/').replace('日','')
        item['url'] = response.url
        content = response.xpath("//div[@class='contTxt']/p//text()").extract()
        item['content'] = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        come_from = response.xpath("//span[@id='source_baidu']/text()").extract_first()
        if come_from:
            item['come_from'] = come_from.replace('来源：','')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['comm_num'] = "0"
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['env_num'] = '0'
        item['media'] = '浙江在线'
        item['media_type'] = '网媒'
        item['addr_province'] = '浙江'
        item['addr_city'] = '杭州'
        # print(item)
        yield item














