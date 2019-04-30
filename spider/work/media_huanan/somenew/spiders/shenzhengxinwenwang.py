import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 深圳新闻网
    name = 'shenzhengxinwenwang'
    allowed_domains = ['sznews.com']
    custom_settings = {'DOWNLOAD_DELAY': 0.8}
    start_urls = ['http://www.sznews.com/culture/node_192827.htm','http://sznews.com/education/node_204675.htm',\
                  'http://www.sznews.com/eating/node_11101.htm','http://travel.sznews.com/node_38943.htm',\
                  'http://auto.sznews.com/node_204626.htm','http://www.sznews.com/tech/node_231089.htm',\
                  'http://www.sznews.com/tech/node_231090.htm','http://www.sznews.com/banking/node_124672.htm',\
                  'http://www.sznews.com/banking/node_124667.htm','http://dc.sznews.com/node_204507.htm',\
                  'http://www.sznews.com/stock/node_240149.htm','http://news.sznews.com/node_239021.htm',\
                  'http://www.sznews.com/banking/node_124667.htm','http://news.sznews.com/node_237739.htm',
                  'http://news.sznews.com/node_237741.htm','http://news.sznews.com/node_237743.htm',\
                  'http://www.sznews.com/photo/node_150829.htm','http://news.sznews.com/node_18029.htm',\
                  'http://news.sznews.com/node_18236.htm','http://news.sznews.com/node_150128.htm',\
                  'http://news.sznews.com/node_18029.htm','http://www.sznews.com/news/node_150507.htm',\
                  'http://www.sznews.com/news/node_180787.htm','http://www.sznews.com/news/node_31180.htm',\
                  'http://www.sznews.com/news/node_150507.htm','http://www.sznews.com/news/node_227703.htm',\
                  'http://www.sznews.com/news/node_109926.htm','http://www.sznews.com/news/node_141128.htm']
    def parse(self, response):
        res = response.xpath('//li[@class="list-pt-li cf"]/a/@href').extract()
        print(res)
        for url in res:
            print(url)
            if 'htm'  in url:
                yield scrapy.Request(url, callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("/html/body/div[2]/h1/text()//h1[@class=\"con_title\"]/text()|//h1[@class=\"h1-news\"]/text()|//h1[@class=\"con_title\"]/text()").extract()
        try:
            item['time'] = response.xpath("/html/body/div[2]/div[6]/div[1]/div/text()|//div[@class=\"fs18 share-date l\"]/text()|/html/body/div[4]/div[1]/div[2]/text()|/html/body/div[2]/div[6]/div[2]/text()|/html/body/div[4]/div[1]/div[2]/div[1]/div[1]/text()").extract()[0]
        except:
            item['time'] = ''

        item['content'] = response.xpath('//div[@class="article-content cf new_txt"]/p/text()|//div[@class="article-content cf new_txt"]/p/span/text()|//*[@id="con_arc_content"]/p[3]/text()').extract()
        try:
            item['come_from'] = response.xpath("//span[@class=\"ml10\"]/text()").extract()[0]
        except:
            item['come_from'] = ''
        item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                          '').replace(
            '\u2002', '').replace('\r', '').replace('\r\n', '').strip()
        if item['content'] and item['title']:
            if len(item['title']) == 2:
                item['title'] = item['title'][1].strip().strip('\r\n').replace('\u200b','')
            else:
                try:
                    item['title'] = item['title'][0].split('\r\n')[1].strip()
                except:
                    item['title'] = item['title'][0]
            item['come_from'] = item['come_from'].split('来源：')[1]
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '深圳新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '广东'
            yield item