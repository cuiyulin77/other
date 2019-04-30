import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 南方网
    name = 'nanfangwang'
    allowed_domains = ['southcn.com']
    custom_settings = {'DOWNLOAD_DELAY': 0.8}
    start_urls = ['http://it.southcn.com/9/node_152391.htm','http://tech.southcn.com/t/node_103955.htm',\
                  'http://car.southcn.com/7/node_365678.htm','http://tech.southcn.com/t/node_104011.htm',\
                  'http://life.southcn.com/g/node_273396.htm','http://it.southcn.com/9/node_346492.htm',\
                  'http://sports.southcn.com/s/node_135151.htm','http://edu.southcn.com/yczt/node_254052.htm',\
                  'http://finance.southcn.com/f/node_335082.htm','http://finance.southcn.com/f/node_335074.htm',\
                  'http://finance.southcn.com/f/node_335071.htm','http://news.southcn.com/nfplus/gdhz/node_383470.htm',\
                  'http://news.southcn.com/nfplus/qjwl/node_383455.htm','http://news.southcn.com/nfplus/qjwl/node_383455.htm',\
                  'http://news.southcn.com/nfplus/nfh/node_378292.htm','http://news.southcn.com/nfplus/yyl/node_383485.htm',\
                  'http://news.southcn.com/n/node_383599.htm','http://news.southcn.com/n/node_383600.htm',\
                  'http://news.southcn.com/nfdsb/node_384172.htm','http://news.southcn.com/nfplus/nfzbc/node_383484.htm',\
                  'http://news.southcn.com/21sjjjbd/node_384175.htm','http://opinion.southcn.com/o/node_363172.htm',\
                  'http://opinion.southcn.com/o/node_386432.htm','http://gz.southcn.com/node_351636.htm',\
                  'http://gz.southcn.com/node_351635.htm','http://gz.southcn.com/g/node_291331.htm','http://gz.southcn.com/g/node_287602.htm',\
                  'http://gz.southcn.com/g/node_287606.htm','http://kb.southcn.com/default.htm','http://news.southcn.com/community/',\
                  'http://economy.southcn.com/node_321243.htm','http://www.southcn.com/pc2018/yw/node_384370.htm',\
                  'http://news.southcn.com/gd/','http://news.southcn.com/china/default.htm','http://economy.southcn.com/e/node_321237.htm']
    def parse(self, response):
        res = response.xpath('//div/h3/a/@href|//ul/li/a/@href').extract()
        print(res)
        for url in res:
            if 'htm' in url:
                yield scrapy.Request(url, callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("//*[@id=\"article_title\"]/text()").extract()[0]
        item['time'] = response.xpath("//*[@id=\"pubtime_baidu\"]/text()").extract()[0]
        item['content'] = response.xpath('//*[@id="content"]/p/text()').extract()
        item['come_from'] = response.xpath("//*[@id=\"source_baidu\"]/text()").extract()[0]
        item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                          '').replace(
            '\u2002', '').replace('\r', '').replace('\r\n', '').strip()
        if item['content'] and item['title']:
            # print(len(item['title']),item['title'])
            item['title'] = item['title'].split('\r\n')[1]
            item['come_from'] = item['come_from'].split('来源：')[1]
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '南方网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '广东'
            # print(item)
            yield item