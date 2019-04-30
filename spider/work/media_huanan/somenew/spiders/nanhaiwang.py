import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime,json
import re
class DezhouxinwenSpider(scrapy.Spider):
    # 南海网
    name = 'nanhaiwang'
    allowed_domains = ['hinews.cn']
    start_urls = ['http://www.hinews.cn/news/hainan/zt12345/','http://www.hinews.cn/news/hainan/quanwfb/',\
                  'http://www.hinews.cn/news/tianxia/','http://haikou.hinews.cn/',\
                  'http://www.hinews.cn/news/shiping/wenypp/index.shtml',\
                  'http://www.hinews.cn/news/shiping/mtjj/index.shtml','http://www.hinews.cn/news/shiping/shehcj/index.shtml0',\
                  'http://www.hinews.cn/news/hainan/','http://www.hinews.cn/news/shiping/toujpl/index.shtml',\
                  'http://www.hinews.cn/news/shiping/djpl/','http://www.hinews.cn/news/shiping/jianyhn/index.shtml',\
                  'http://www.hinews.cn/news/shiping/shizlw/index.shtml']
    def parse(self, response):
            res = response.xpath('//li[@class="mb42"]/div/a/@href').extract()
            if len(res) ==0:
                url = re.findall('href=\'(.*)\';</script>', response.text)[0]
                yield scrapy.Request(url, callback=self.get_detail_url)
            for i in res:
                print(i)
                yield scrapy.Request(i, callback=self.get_detail)
    def get_detail_url(self,response):
        res = response.xpath('//li[@class="mb42"]/div/a/@href').extract()
        for i in res:
            yield scrapy.Request(i, callback=self.get_detail)

    def get_detail(self,response):
        if len(response.text)<200:
            url = re.findall('href=\'(.*)\';</script>', response.text)[0]
            yield scrapy.Request(url, callback=self.get_detail_url2)
        else:
            item = SomenewItem()
            item['title'] = response.xpath('/html/body/div[7]/div[1]/h2/text()').extract_first()
            item['time'] = response.xpath('/html/body/div[7]/div[1]/ul/li[3]/text()').extract_first()
            item['content'] = response.xpath('//*[@id="bs_content"]/p/text()').extract()
            item['come_from'] = response.xpath('/html/body/div[7]/div[1]/ul/li[1]/a/text()').extract_first()
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                          '').replace(
                '\u2002', '').replace('\r', '').replace('\r\n', '').strip()
            if item['content'] and item['title']:
                item['url'] = response.url
                m = hashlib.md5()
                m.update(str(item['url']).encode('utf8'))
                item['article_id'] = m.hexdigest()
                item['time'] = item['time'].split('时间：')[1]
                item['media'] = '南海网'
                item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                item['comm_num'] = "0"
                item['fav_num'] = '0'
                item['read_num'] = '0'
                item['env_num'] = '0'
                item['media_type'] = '网媒'
                item['addr_province'] = '海南'
                print(item)

    def get_detail_url2(self,response):
        print(response.url,'响应的urlget_detail_url2')
        item = SomenewItem()
        item['title'] = response.xpath('/html/body/div[7]/div[1]/h2/text()').extract_first()
        item['time'] = response.xpath('/html/body/div[7]/div[1]/ul/li[3]/text()').extract_first()
        item['content'] = response.xpath('//*[@id="bs_content"]/p/text()').extract()
        item['come_from'] = response.xpath('/html/body/div[7]/div[1]/ul/li[1]/a/text()').extract_first()
        item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                          '').replace(
            '\u2002', '').replace('\r', '').replace('\r\n', '').strip()
        if item['content'] and item['title']:
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['time'] = item['time'].split('时间：')[1]
            item['media'] = '南海网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '海南'
            print(item)
