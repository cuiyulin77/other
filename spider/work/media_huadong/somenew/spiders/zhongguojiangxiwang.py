# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 中国江西网
    name = 'zhongguojiangxiwang'
    allowed_domains = ['jxnews.com.cn']
    start_urls = ['http://www.jxnews.com.cn/']
    # start_urls = ['http://fc.jxnews.com.cn/system/2019/03/14/017417180.shtml']
    custom_settings = {'DOWNLOAD_DELAY': 0.8}
    def parse(self, response):
        # print(response.url)
        xp = '//*[@id="Cen_Ri_R"]/div/table/tr/td/a/@href|//*[@id="PageOneRighLine"]/div[16]/ul/table/tr/td/a/@href|/html/body/div[32]/div[4]/div[1]/div/table/tr/td/@href|/html/body/div[32]/div[4]/div[2]/div/ul/li/a/@href|//*[@id="jsbbs"]/div/ul/li/a/@href|//div/div/ul/li/a/@href'
        res = response.xpath(xp).extract()
        print(res)
        for url in res:
            if '#' not in url and 'jiangxi' not in url and 'wenz'not in url and 'bbs' not in url:
                yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//h1/a/text()|//div[@class=\"biaoti\"]/*/text()|//h1/text()|//div[@class=\"BiaoTi\"]/text()").extract_first()
        item['time'] = response.xpath("/html/body/div[5]/div[1]/div[1]/h5/text()|//*[@id=\"pubtime_baidu\"]/text()|//div[@class=\"xbt\"]/span[1]/text()|//div[@class=\"text1t\"]/h5/text()").extract_first()
        item['content'] = response.xpath('//*[@id="content"]/p/text()|//p/text()').extract()
        item['come_from'] ='中国江西网'
        item['content']= ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').replace( '\r', '').replace( '\r\n', '').strip()
        if item['content'] and item['title']:
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '中国江西网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '江西'
            print(item)
            yield item


