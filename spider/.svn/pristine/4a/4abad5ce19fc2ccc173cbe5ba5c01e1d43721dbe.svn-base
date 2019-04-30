# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
import hashlib
from somenew.items import SomenewItem

class JingjiribaoSpider(scrapy.Spider):
    name = 'jingjiribao'
    allowed_domains = ['paper.ce.cn']
    today = datetime.date.today()
    # print('*****', today)
    url_list = []
    for i in range(2):
        date = today - datetime.timedelta(days=i)
        date = date.strftime("%Y-%m/%d")
        # http://paper.ce.cn/jjrb/html/2018-05/21/node_2.htm
        url = 'http://paper.ce.cn/jjrb/html/' + str(date) + '/node_2.htm'
        url_list.append(url)
    start_urls = url_list

    def parse(self, response):
        page_urls= response.xpath("(//tbody)[1]//a[@id='pageLink']/@href").extract()
        for page in page_urls:
            url=response.urljoin(page)
            yield scrapy.Request(url,callback=self.parse_detail)

    def parse_detail(self,response):
        content_url = response.xpath("//td[@valign='top']/a/@href").extract()
        for url in content_url:
            url = response.urljoin(url)
            yield scrapy.Request(url,callback=self.get_content)

    def get_content(self,response):
        item=SomenewItem()
        item['url'] = response.url
        item['time'] =re.search("(\d{4})-(\d{2})/(\d{2})", item['url']).group().replace("-",'/')
        first_title =response.xpath("//td[@class='STYLE32']//tr[1]/td/text()").extract_first()
        second_title= response.xpath("//td[@class='STYLE32']//tr[2]/td/text()").extract_first()
        third_title = response.xpath("//td[@class='STYLE32']//tr[3]/td/text()").extract_first()
        title_list = [first_title,second_title,third_title]
        for title in title_list:
            if title is None:
                title_list.remove(title)
        item['title'] = ','.join(title_list)
        item['content'] = response.xpath("//founder-content/p/text()").extract()
        item['media'] = '经济日报'
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        yield item