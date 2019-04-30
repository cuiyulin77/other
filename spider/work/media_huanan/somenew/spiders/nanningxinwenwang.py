import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 南宁新闻网
    name = 'nanningxinwenwang'
    allowed_domains = ['nnnews.net']
    # custom_settings = {'DOWNLOAD_DELAY': 0.8}
    start_urls = ['http://www.nnnews.net/hotline/','http://www.nnnews.net/news/','http://www.nnnews.net/politics/','http://www.nnnews.net/gnnews/','http://www.nnnews.net/gxnews/','http://www.nnnews.net/specialtopic/','http://www.nnnews.net/channel/']
    # start_urls = ['http://www.nnnews.net/politics/']
    def parse(self, response):
        res = response.xpath('//*[@id="lists"]/ul/li/a/@href').extract()
        print(res)
        for url in res:
            if 'net' not in url:
                url = response.url+url.split('.')[1]+'.html'
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("//*[@id=\"title\"]/h1/text()").extract_first()
        item['time'] = response.xpath("//*[@id=\"inf\"]/text()").extract()[0]
        item['content'] = response.xpath('//*[@id="dochtml"]/*//p/text()').extract()
        item['come_from'] =response.xpath("//*[@id=\"inf\"]/text()").extract()[0]
        item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                          '').replace(
            '\u2002', '').replace('\r', '').replace('\r\n', '').strip()
        # print(item)
        if item['content'] and item['title']:
            item['time'] = item['time'].split('来源：')[0].strip()
            item['come_from'] = item['come_from'].split('来源：')[1].split()[0]
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '南宁新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '广西'
            # yield item
            print(item)
