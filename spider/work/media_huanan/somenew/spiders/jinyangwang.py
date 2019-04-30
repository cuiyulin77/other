import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 金羊网
    name = 'jinyangwang'
    allowed_domains = ['ycwb.com']
    custom_settings = {'DOWNLOAD_DELAY': 0.8}
    start_urls = ['http://yuqing.ycwb.com/node_21439.htm','http://yuqing.ycwb.com/node_21440.htm',\
                  'http://yuqing.ycwb.com/node_21436.htm','http://news.ycwb.com/node_83422.htm',\
                  'http://3c.ycwb.com/it_txdt.htm','http://3c.ycwb.com/digital.htm',\
                  'http://3c.ycwb.com/mobile.htm','http://money.ycwb.com/jycj_11.htm',\
                  'http://money.ycwb.com/jycj_6.htm','http://money.ycwb.com/jycj_1.htm',\
                  'http://news.ycwb.com/n_gn.htm','http://news.ycwb.com/n_gd_ms.htm',\
                  'http://news.ycwb.com/n_gd_sd.htm','http://news.ycwb.com/n_bd_ms.htm',\
                  'http://news.ycwb.com/n_gd_gc.htm','http://news.ycwb.com/n_gd_sd.htm',\
                  'http://news.ycwb.com/n_gd_rx.htm','http://news.ycwb.com/n_gd_ht.htm',\
                  'http://news.ycwb.com/n_bd_dx.htm','http://news.ycwb.com/n_bd_gs.htm',\
                  'http://news.ycwb.com/n_bd_gz.htm','http://news.ycwb.com/n_gj.htm',\
                  'http://news.ycwb.com/n_bd_zsj.htm','http://news.ycwb.com/n_gn.htm',\
                  'http://news.ycwb.com/news_yw.htm','http://sp.ycwb.com/sp_6.htm',\
                  'http://culture.ycwb.com/culture_jianggu.htm','http://sports.ycwb.com/yaguan.htm',\
                  'http://sports.ycwb.com/zhongchao.htm','http://news.ycwb.com/gundong.htm',\
                  'http://news.ycwb.com/n_gd_jd.htm','http://sp.ycwb.com/sp_1.htm',\
                  'http://news.ycwb.com/node_79309.htm','http://news.ycwb.com/node_79308.htm',\
                  'http://news.ycwb.com/node_79307.htm','http://ent.ycwb.com/movic.htm',
                  'http://news.ycwb.com/node_83401.htm','http://ent.ycwb.com/audition.htm']
    def parse(self, response):
        res = response.xpath('//ul[@class="lists"]/li/a/@href|//div/ul/li/a/@href').extract()
        print(res)
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("//*[@id=\"tiwj\"]/text()").extract()
        item['time'] = response.xpath("//*[@id=\"pubtime_baidu\"]/text()").extract()[0]
        item['content'] = response.xpath('//div[@class="main_article"]/p/text()').extract()
        item['come_from'] = response.xpath("//*[@id=\"source_baidu\"]/text()").extract()[0]
        item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n',                                                                                   '').replace(
            '\u2002', '').replace('\r', '').replace('\r\n', '').strip()
        # print(item)
        if item['content'] and item['title']:
            item['title'] = item['title'][0].split('\r\n\t')[1].strip()
            item['come_from'] = item['come_from'].split('来源：')[1]
            item['time'] =item['time'].split('发表时间：')[1]
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '金羊网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '广东'
            # print(item)
            yield item