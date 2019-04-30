# -*- coding: utf-8 -*-
# =============================================
# 所属省市:西藏
# 所属网站: 西藏日报电子版爬虫
# =============================================
import scrapy
import datetime
from somenew.items import SomenewItem
from somenew.utils.common import get_md5
import re

class XizangRibaoSpider(scrapy.Spider):
    name = 'xizang_ribao'
    allowed_domains = ['epaper.chinatibetnews.com']
    # urls = []
    # today = datetime.date.today()
    # for i in range(3):
    #     dt = today - datetime.timedelta(days=i)
    #     # 2019-02/25
    #     dat = dt.strftime("%Y-%m/%d")
    #     # print(dat)
    #     url = 'http://epaper.chinatibetnews.com/xzrb/html/'+dat+'/node_4.htm'
    #     urls.append(url)
    #     print(url)
    # start_urls = urls
    start_urls = ['http://epaper.chinatibetnews.com/xzrb/html/2019-03/24/node_4.htm']

    def start_requests(self):
        today = datetime.date.today()
        for i in range(3):
            dt = today - datetime.timedelta(days=i)
            # 2019-02/25
            dat = dt.strftime("%Y-%m/%d")
            # url = 'http://epaper.chinatibetnews.com/xzrb/html/{}/node_4.htm'.format(dat)
            url = 'http://epaper.chinatibetnews.com/xzrb/html/' + dat + '/node_4.htm'
            print(url)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        print('-1-'*30)
        td_list = response.xpath("//td[@class='default']/a[@id='pageLink']/@href").extract()
        for td in td_list:
            url = response.urljoin(td)
            print('-2-' * 30)
            yield scrapy.Request(url,callback=self.parse_detail)

    def parse_detail(self,response):
        content_urls = response.xpath("//td[@class='default'][@valign='top']/a/@href").extract()
        for url in content_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.get_content)

    def get_content(self,response):
        item = SomenewItem()
        item['url'] = response.url
        data_str = re.search('\d{4}-\d{2}/\d{2}',item['url'])
        if data_str:
            item['time'] = data_str.group().replace('/','-')
        else:
            item['time'] = datetime.date.today()
        title = response.xpath("(//td[@class='font02']|//td[@class='font01'])/text()").extract()
        title = ''.join(title)
        item['title'] = title
        content = response.xpath("//div[@id='ozoom']//p/text()").extract()
        item['content'] = ' '.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['article_id'] = get_md5(item['url'])
        item['media'] = "西藏日报"
        item['comm_num'] = "0"
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['env_num'] = '0'
        item['media_type'] = '报纸'
        item['addr_province'] = '西藏'
        print(item)




