# -*- coding: utf-8 -*-
import scrapy
import re

# 39健康网
class SanjiuSpider(scrapy.Spider):
    name = 'sanjiu'
    urls_list = []
    allowed_domains = ['39.net']
    start_urls = ['http://care.39.net/sjbj/djbj/fblx', 'http://care.39.net/sjbj/djbj/ysyd', 'http://care.39.net/sjbj/djbj/sthl', 'http://care.39.net/sjbj/djbj/dljb', 'http://care.39.net/sjbj/qjbj/qjys', 'http://care.39.net/sjbj/qjbj/qgqz', 'http://care.39.net/sjbj/qjbj/qfqb', 'http://care.39.net/sjbj/qjbj/qjhf', 'http://care.39.net/sjbj/xjbj/xrys', 'http://care.39.net/sjbj/xjbj/jblx', 'http://care.39.net/sjbj/xjbj/fsmf', 'http://care.39.net/sjbj/xjbj/jkts', 'http://care.39.net/sjbj/cjbj/yfjb', 'http://care.39.net/sjbj/cjbj/ysmf', 'http://care.39.net/sjbj/cjbj/stwl', 'http://care.39.net/sjbj/cjbj/qjbj', 'http://care.39.net/tsrq/xsbj/', 'http://care.39.net/tsrq/qsnbj/', 'http://care.39.net/tsrq/zyrs/', 'http://care.39.net/tsrq/blbj/', 'http://care.39.net/ys/jj/', 'http://care.39.net/ys/yswq/', 'http://care.39.net/ys/shxg/', 'http://care.39.net/ys/shcs/', 'http://care.39.net/yjk/jkzc/', 'http://care.39.net/yjk/tjgs/sm', 'http://care.39.net/yjk/tjgs/pl', 'http://care.39.net/yjk/tjgs/yjkzhz',
'http://care.39.net/yjk/yfcs/sm', 'http://care.39.net/yjk/yfcs/pl', 'http://care.39.net/yjk/yfcs/yjkzhz','http://care.39.net/jbyf/jbhl/', 'http://care.39.net/dzbj/baby/', 'http://care.39.net/dzbj/oldman/', 'http://care.39.net/dzbj/man/', 'http://care.39.net/dzbj/woman/', 'http://care.39.net/jbyf/jzb/', 'http://care.39.net/jbyf/crb/', 'http://care.39.net/jbyf/xxg/', 'http://care.39.net/jbyf/az/', 'http://care.39.net/jbyf/qt/', 'http://care.39.net/yjk/zzyf/sm', 'http://care.39.net/yjk/zzyf/sy', 'http://care.39.net/yjk/zzyf/pl', 'http://care.39.net/yjk/zzyf/xljk', 'http://care.39.net/yjk/zzyf/zhz',
'http://care.39.net/ys/jkjj/','http://care.39.net/ys/jkdsy/','http://care.39.net/ys/dzs/'
 ]

    def parse(self, response):
        a_list = response.xpath("//div[@class='listbox']/ul/li//a/@href").extract()
        for a in a_list:
            url = response.urljoin(a)
            yield scrapy.Request(url,callback=self.get_detail_list)
        next_url = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url),callback=self.parse)

    def get_detail_list(self,response):
        item = {}
        item['title'] = response.xpath("//h1/text()").extract_first()
        if item['title']:
            item['time'] = response.xpath("//div[@class='date']/em[1]/text()").extract_first()
            item['come_from'] = '39健康网'
            item['classfy'] = '养生'
            item['url'] = response.url
            p_list = response.xpath("//div[@id='contentText']/p")
            content = []
            for p in p_list:
                con = p.xpath(".//text()").extract()
                if not con:
                    con = p.xpath("./img/@src").extract_first()
                    if con:
                        con = ['<img src="{}">'.format(con)]
                # if con[0] and re.search(r".*?jpg$",con[0]):
                #     "<img src='{}'>".format(con[0])
                if con:
                    content = content+con
            content = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
            item['content'] = content
            print(item)
        elif response.xpath("//*[@id='N1']/text()|//*[@id='L1']/text()"):
            title = response.xpath("//*[@id='N1']/text()|//*[@id='L1']/text()").extract_first()
            if title:
                item['title'] = title.replace(u"\u3000",' ')
            content = response.xpath("//*[@id='L10']//text()|//*[@id='N10']//text()").extract()
            content = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
            item['content'] = content
            item['come_from'] = '39健康网'
            item['classfy'] = '养生'
            html = response.text
            t = re.search(r"时间：(\d{4}.\d{2}.\d{2})", html)
            if t:
                item['time'] = t.group(1)
            item['url'] =  response.url
            print(item)
        else:
            print("提取不到数据的网页为: {}".format(response.url))

        # if response.xpath("//*[@id='L1']/text()").extract_first():
        #     item['title'] = response.xpath("//*[@id='L1']/text()").extract_first()



