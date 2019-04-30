# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import datetime
import hashlib

# 澎湃爬虫
class PengpaiSpider(scrapy.Spider):
    name = 'pengpai'
    allowed_domains = ['thepaper.cn']
    '''
    https://www.thepaper.cn/load_index.jsp?nodeids=25462,25488,25489,25490,25423,25426,25424,25463,25491,25428,27604,25464,25425,25429,25481,25430,25678,25427,25422,25487,25634,25635,25600,&topCids=2139767,2139727,2139403&pageidx=1,澎湃时事
    https://www.thepaper.cn/load_chosen.jsp?nodeids=25949&topCids=2139821,2139825,2139767,2139344,&pageidx=1,首页
    https://www.thepaper.cn/load_index.jsp?nodeids=25434,25436,25433,25438,25435,25437,27234,25485,25432,&topCids=2139821,2139856,2139485&pageidx=1， 财经
    https://www.thepaper.cn/load_index.jsp?nodeids=25448,26609,25942,26015,25599,25842,26862,25769,25990,26173,26202,26404,26490,&topCids=2139654,2134591&pageidx=1， 生活
    https://www.thepaper.cn/load_more_gov.jsp?nodeids=&topCids=2139501,2139459,2139582,2139892,2139265&pageidx=1&govType=publish， 问政
    https://www.thepaper.cn/load_index.jsp?nodeids=25444,27224,26525,26878,25483,25457,25574,25455,26937,25450,25482,25445,25456,25446,25536,26506,&topCids=2139475&pageidx=1， 思想
    https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&pageidx=1， 视频
    '''
    url_list = []
    node_list = ['https://www.thepaper.cn/load_index.jsp?nodeids=25462,25488,25489,25490,25423,25426,25424,25463,25491,25428,27604,25464,25425,25429,25481,25430,25678,25427,25422,25487,25634,25635,25600,&topCids=2139767,2139727,2139403&pageidx={}','https://www.thepaper.cn/load_chosen.jsp?nodeids=25949&topCids=2139821,2139825,2139767,2139344,&pageidx={}','https://www.thepaper.cn/load_index.jsp?nodeids=25434,25436,25433,25438,25435,25437,27234,25485,25432,&topCids=2139821,2139856,2139485&pageidx={}','https://www.thepaper.cn/load_index.jsp?nodeids=25448,26609,25942,26015,25599,25842,26862,25769,25990,26173,26202,26404,26490,&topCids=2139654,2134591&pageidx={}','https://www.thepaper.cn/load_more_gov.jsp?nodeids=&topCids=2139501,2139459,2139582,2139892,2139265&pageidx={}&govType=publish','https://www.thepaper.cn/load_index.jsp?nodeids=25444,27224,26525,26878,25483,25457,25574,25455,26937,25450,25482,25445,25456,25446,25536,26506,&topCids=2139475&pageidx={}']
    for node in node_list:
        for i in range(26)[1:]:
            url = node.format(i)
            url_list.append(url)
    start_urls = url_list

    def parse(self, response):
        href_list = response.xpath("//body/div/h2/a/@href").extract()
        for href in href_list:
            url = response.urljoin(href)
            yield scrapy.Request(url,callback=self.get_content)

    def get_content(self,response):
        item = SomenewItem()
        item['title'] = response.xpath("//h1[@class='news_title']/text()").extract_first()
        time_ = response.xpath("//div[@class='news_about']/p[2]/text()").extract_first()
        item['time'] = re.search(r".*?(\d+-\d+-\d+ \d+\:\d+)",time_).group(1)
        item['url'] = response.url
        item['content'] = response.xpath("//div[@class='news_txt']//text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        item['media'] = '澎湃'
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        print(item)
        yield item

