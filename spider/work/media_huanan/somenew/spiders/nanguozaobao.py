import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime,json

class DezhouxinwenSpider(scrapy.Spider):
    # 南国早报
    name = 'nanguozaobao'
    allowed_domains = ['ngzb.com.cn']
    # custom_settings = {'DOWNLOAD_DELAY': 0.8}
    start_urls = ['http://www.ngzb.com.cn/cms/document/get_list/id/4.html?page=2','http://www.ngzb.com.cn/cms/document/get_list/id/18.html?page=2','http://www.ngzb.com.cn/cms/document/get_list/id/3.html?page=2','/http://www.ngzb.com.cn/cms/document/get_list/id/13.html?page=2','http://www.ngzb.com.cn/cms/document/get_list/id/0.html?page=1','http://www.ngzb.com.cn/cms/document/get_list/id/16.html?page=2','http://www.ngzb.com.cn/channel/13.html?page=1','http://www.ngzb.com.cn/cms/document/get_list/id/1.html?page=5']
    def parse(self, response):
        if 'get_list' in response.url:
            for i in range(1,20):
                url = response.url.split('=')[0]+'='+str(i)
                yield scrapy.Request(url, callback=self.get_detail_url)
        else:
            res = response.xpath('//a[@class="text-primary-dark"]/@href').extract()
            # print(res)
            for i in res:
                url = 'http://www.ngzb.com.cn'+i
                yield scrapy.Request(url, callback=self.get_detail)


    def get_detail_url(self,response):
        try:
            res = json.loads(response.text)['data']
            for i in res:
                url = 'http://www.ngzb.com.cn' + i['href']
                # print(type(i),item['href'])
                yield scrapy.Request(url, callback=self.get_detail)
        except:
            pass

    def get_detail(self,response):
        item = SomenewItem()
        try:
            item['title'] = response.xpath('//h2[@class="newspage-main-title"]/text()').extract()[0]
        except:
            pass
        try:
            item['come_from'] = response.xpath('//span[@class="newspage-main-info-meta-item4"]/text()').extract()[1].split('来源:')[1]
        except:
            pass
        item['content'] = response.xpath('//div[@class="newspage-main-content"]/p/text()').extract()
        item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                          '').replace(
            '\u2002', '').replace('\r', '').replace('\r\n', '').strip()
        if item['content'] and item['title']:
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '南国早报'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['time'] =item['create_time']
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '广东'
            print(item)

            # yield item