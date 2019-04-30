# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime,json

class DezhouxinwenSpider(scrapy.Spider):
    # 兴义之窗
    name = 'xingyizhichuang'
    allowed_domains = ['xyzc.cn']
    start_urls =['http://www.xyzc.cn/xyzcedu/jyzx','http://www.xyzc.cn/kuaibao','http://www.xyzc.cn/news','http://www.xyzc.cn/news/xianshi','http://www.xyzc.cn/news/jinrixinwen','http://www.xyzc.cn/portal.php?mod=list&catid=60','http://www.xyzc.cn/portal.php?mod=list&catid=61','http://www.xyzc.cn/news/gonggao']

    def parse(self, response):
        res = response.xpath('//div[@class="news-list-content"]/dl/dt/a/@href').extract()
        for i in res:
            yield scrapy.Request(i, callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//div[@class=\"qc-title\"]/h2/text()").extract_first()
        item['time'] = response.xpath("//div[@class=\"news-content-tit\"]/dl/dt/text()[1]").extract_first()
        item['content'] = response.xpath('//div[@class="news-content-txt qc_news_attr_img"]/div/text()').extract()
        item['come_from'] = response.xpath('//div[@class="news-content-tit"]/dl/dt/text()[5]').extract_first()
        if item['content'] and item['time'] and item['title']:
            item['come_from'] = item['come_from'].split('\r\n')[1].strip()
            item['time'] = item['time'].split('更新：')[1]
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '兴义之窗'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '贵州'
            yield item


