import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime ,json

class DezhouxinwenSpider(scrapy.Spider):
    # 广西新闻网
    name = 'jinyangwang'
    allowed_domains = ['gxnews.com.cn']
    custom_settings = {'DOWNLOAD_DELAY': 0.8}
    start_urls = ['https://v.gxnews.com.cn/index.php?c=www&a=getArticles&sortids=21337']
    def parse(self, response):
        for i in range(0,200,20):
            url ='https://v.gxnews.com.cn/index.php?c=www&a=getArticles&sortids=21337&start={}'.format(i)
            yield scrapy.Request(url, callback=self.get_detail_url)
    def get_detail_url(self,response):
        res = json.loads(response.text)
        # item = SomenewItem()
        for i in res:
            item = SomenewItem()
            item['title'] = i['title']
            item['come_from'] = i['source']
            item['url'] = i['url']
            # print(res)
            item['time'] = i['date_ymdhis']
            yield scrapy.Request(i['url'], callback=self.get_detail,meta={'item':item})
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = response.meta['item']
        item['content'] =response.xpath('//div[@class="article-content"]/p/text()|//*[@id="artContent"]/p/text()').extract()
        item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n',                                                                                   '').replace(
            '\u2002', '').replace('\r', '').replace('\r\n', '').strip()
        # print(item)
        if item['content'] and item['title']:
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '广西新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '广西'
            # print(item)
            yield item