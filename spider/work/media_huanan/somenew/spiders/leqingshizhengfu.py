import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime,re

class DezhouxinwenSpider(scrapy.Spider):
    # 乐清市政府
    name = 'leqingshizhengfu'
    allowed_domains = ['yueqing.gov.cn']
    custom_settings = {'DOWNLOAD_DELAY': 0.8}
    start_urls = ['http://www.yueqing.gov.cn/col/col1322069/index.html','http://www.yueqing.gov.cn/col/col1322071/index.html','http://www.yueqing.gov.cn/col/col1322072/index.html','http://www.yueqing.gov.cn/col/col1322073/index.html']
    def parse(self, response):
        res = re.findall('><a href=\'(.*)\' title',response.text)
        for url in res:
            url ='http://www.yueqing.gov.cn'+url
            print(url)
            if 'htm' in url:
                yield scrapy.Request(url, callback=self.get_detail)
        for i in range(2,151):
            url = 'http://www.yueqing.gov.cn/col/col1322069/index.html?uid=4308386&pageNum={}'.format(i)
            # print(url)
            yield scrapy.Request(url, callback=self.get_detail_url)
    def get_detail_url(self,response):
        res = re.findall('><a href=\'(.*)\' title',response.text)
        for url in res:
            url ='http://www.yueqing.gov.cn'+url
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("//*[@id='c']/tr[1]/td/text()").extract()[0]
        item['time'] = response.xpath("//*[@id='c']/tr[2]/td/div/table/tr/td[1]/text()").extract()[0]
        item['content'] = response.xpath('//*[@id="zoom"]/p/text()').extract()
        item['come_from'] = response.xpath("//*[@id='c']/tr[2]/td/div/table/tr/td[3]/text()").extract()[0]
        item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                          '').replace(
            '\u2002', '').replace('\r', '').replace('\r\n', '').strip()
        if item['content'] and item['title']:
            item['title'] = item['title'].split('\r\n')[0]
            item['time']= item['time'].split('发布日期：')[1]
            item['come_from'] = item['come_from'].split('来源：')[1]
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '乐清市政府'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '浙江'
            # yield item