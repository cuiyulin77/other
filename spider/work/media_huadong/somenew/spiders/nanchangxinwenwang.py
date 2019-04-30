# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime



class DezhouxinwenSpider(scrapy.Spider):
    # 南昌新闻网
    name = 'nanchangxinwenwang'
    allowed_domains = ['ncnews.com.cn']
    start_urls = ['http://www.ncnews.com.cn/xwzx/ncxw/jrnc/','http://www.ncnews.com.cn/xwzx/ncxw/kpsh/','http://www.ncnews.com.cn/xwzx/ncxw/wtxw/','http://www.ncnews.com.cn/xwzx/ncxw/fzjj/','http://www.ncnews.com.cn/xwzx/ncxw/xqxw/','http://www.ncnews.com.cn/xwzx/ncxw/shxw/','http://www.ncnews.com.cn/xwzx/ncxw/snxw/','http://www.ncnews.com.cn/xwzx/ncxw/szxw/','http://www.ncnews.com.cn/xwzx/ncxw/zhxw/','http://www.ncnews.com.cn/xwzx/ncxw/bwzg_rd/','http://www.ncnews.com.cn/xwzx/ncxw/ncsp/']
    def parse(self, response):
        res = response.xpath('//h3/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("//div[@class=\"read\"]/h3/text()").extract_first()
        item['time'] = response.xpath("//div[@class=\"newsinfo\"]/text()").extract()
        item['content'] = response.xpath('//*[@id="newsread"]/div[1]/p/text()').extract()
        item['come_from'] = response.xpath("//div[@class=\"newsinfo\"]/text()").extract()
        item['content']= ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n', '').replace( '\u2002', '').replace( '\r', '').replace( '\r\n', '').strip()
        if item['content'] and item['title']:
            item['url'] = response.url
            item['time'] = item['time'][1].split('日期：')[1].split()[0]
            item['come_from'] =item['come_from'][1].split('来源：')[1].split('\n\t\t\t')[0]
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '南昌新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '江苏'
            yield item

