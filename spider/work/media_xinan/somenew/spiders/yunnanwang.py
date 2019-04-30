# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 云南网
    name = 'yunnanwang'
    allowed_domains = ['yunnan.cn']
    start_urls =['http://nujiang.yunnan.cn/pdtt/','http://dali.yunnan.cn/pdtt/','http://xsbn.yunnan.cn/pdtt/',\
                 'http://honghe.yunnan.cn/pdtt/','http://chuxiong.yunnan.cn/pdtt/','http://puer.yunnan.cn/jjlc/',\
                 'http://lijiang.yunnan.cn/pdtt/','http://baoshan.yunnan.cn/pdtt/','http://yuxi.yunnan.cn/pdtt/',\
                 'http://qujing.yunnan.cn/lyjq/index.shtml','http://qujing.yunnan.cn/jjjkq/index.shtml',\
                 'http://qujing.yunnan.cn/xqdt/index.shtml','http://qujing.yunnan.cn/pdtt/','http://kunming.yunnan.cn/xyjj/',\
                 'http://kunming.yunnan.cn/msgz/','http://yn.yunnan.cn/sz/index.shtml','http://yn.yunnan.cn/sz/index.shtml',\
                 'http://yn.yunnan.cn/economic/index.shtml','http://yn.yunnan.cn/science/index.shtml',\
                 'http://yn.yunnan.cn/tour/index.shtml','http://yn.yunnan.cn/history/index.shtml']

    def parse(self, response):
        res = response.xpath('//span[@class="fs1"]/a/@href').extract()
        for url in res:
            url = 'http:'+url
            print(url)
            yield scrapy.Request(url,callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//*[@id=\"layer213\"]/text()").extract_first()
        item['time'] = response.xpath("//span[@class=\"xt2 yh fl\"]/span[1]/text()").extract_first()
        item['content'] = response.xpath('//*[@id="layer216"]/*//text()').extract()
        item['come_from'] = response.xpath('//span[@class="xt2 yh fl"]/span[2]/text()').extract_first()

        if item['content'] and item['time'] and item['title']:
            item['time'] = item['time'].replace('年','/').replace('月','/').replace('日',' ')
            item['come_from'] = item['come_from'].split('\r\n')[2]
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '云南网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '云南'
            print(item)
            yield item


