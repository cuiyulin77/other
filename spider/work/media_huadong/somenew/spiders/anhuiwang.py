import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 安徽网
    name = 'anhuiwang'
    allowed_domains = ['ahwang.cn']
    start_urls= ['http://www.ahwang.cn/anhui/','http://www.ahwang.cn/life/','http://lvyou.ahwang.cn/','http://www.ahwang.cn/sports/','http://www.ahwang.cn/hefei/','http://www.ahwang.cn/baoliao/','http://www.ahwang.cn/china/','http://www.ahwang.cn/world/','http://www.ahwang.cn/lvyou/','http://www.ahwang.cn/ent/','http://www.ahwang.cn/zbah/']
    def parse(self, response):
        res = response.xpath('//*[@id="category"]/div/h3/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)
    def get_detail_url(self,response):
        res = response.xpath('//*[@id="content"]/ul/li/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("//*[@id=\"article\"]/h1/text()").extract_first()
        item['time'] = response.xpath("//span[@class=\"date\"]/text()").extract()[0]
        item['content'] = response.xpath('//div[@class="article-content fontSizeBig clearfix"]/p/text()').extract()
        item['come_from'] = response.xpath("//div[2]/div/span[2]/a/text()").extract()[0]
        item['content']= ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n', '').replace( '\u2002', '').replace( '\r', '').replace( '\r\n', '').strip()
        # print(item)
        if item['content'] and item['title']:
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '安徽网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '安徽'
            print(item)
            yield item