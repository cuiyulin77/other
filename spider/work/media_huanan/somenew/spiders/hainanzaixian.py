import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 海南在线
    name = 'hainanzaixian'
    allowed_domains = ['hainan.net']
    custom_settings = {'DOWNLOAD_DELAY': 0.8}
    start_urls = ['http://news.hainan.net/shzx/list_1.shtml','http://news.hainan.net/caijing/list_1.shtml',\
                 'http://news.hainan.net/kejiao/list_1.shtml','http://news.hainan.net/wenti/list_1.shtml','http://news.hainan.net/hainan/yaowen/list_1.shtml','http://news.hainan.net/shehui/list_1.shtml','http://news.hainan.net/hainan/shixian/list_1.shtml','http://news.hainan.net/guonei/list_1.shtml','http://news.hainan.net/guoji/list_1.shtml']
    def parse(self, response):
        res = response.xpath('//div[@class="tui-text-list f14 li-dot cf newsList                            li-1"]/ul/li/h3/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("//*[@id=\"subject\"]/text()").extract()[0]
        item['time'] = response.xpath("//*[@id=\"cms_fragment_235_bd\"]/div/div[2]/div/text()|//*[@id=\"cms_control_365\"]/div/div[2]/div/ul/li[3]/text()|//div[1]/span/text()[2]|//*[@id=\"cms_fragment_639_bd\"]/*//text()[2]").extract()
        item['content'] = response.xpath('//div[@class="main_article"]/p/text()|//*[@id="cms_fragment_235_bd"]/*//p/text()|//*[@id="cms_control_395"]/*//p/text()').extract()
        try:
           item['come_from'] = response.xpath("//*[@id=\"cms_control_365\"]/*//ul/li[1]/text()|//*[@id=\"cms_fragment_235_bd\"]/*//a/text()|//*[@id=\"cms_fragment_396_bd\"]/*//a/text()").extract()[0]
        except:
            item['come_from'] = ''
        item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n',                                                                                   '').replace(
            '\u2002', '').replace('\r', '').replace('\r\n', '').replace('\t', '').strip()
        if item['content'] and item['title']:
            print(item['time'])
            if len(item['time']) == 1:
                item['time'] =item['time'][0]
            else:
                item['time'] = ''.join(item['time']).replace('\n','').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '海南在线'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '海南'
            print(item)
            # yield item