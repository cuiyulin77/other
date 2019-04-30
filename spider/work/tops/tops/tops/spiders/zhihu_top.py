# -*- coding: utf-8 -*-
import scrapy
import re
import io
import sys
import json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码
# res=urllib.request.urlopen('http://www.baidu.com')
# htmlBytes=res.read()
# print(htmlBytes.decode('gb18030')


class ZhihuTopSpider(scrapy.Spider):
    name = 'zhihu_top'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/billboard']

    def parse(self, response):
        a_list = response.xpath("//div[@class='Card']/a")
        html = response.body.decode()
        content_list = re.search(",\"hotList\":(\[.*?}\])", html, re.S)
        # content_list = content_list.group(1).replace("&quot;",'"').replace('"hotList":','')
        # print(content_list)
        print("="*10)
        if content_list:
            content_list=content_list.group(1).replace("&quot;",'"').replace('"hotList":','')
            content_list = json.loads(content_list)
            # print(content_list)
            for content in content_list:
                item = {}
                item['top_num'] =content_list.index(content) + 1
                item['top_title'] = content['target']['titleArea']['text']
                hot_value = content['target']['metricsArea']['text']
                hot_value_re = re.search("\d+", hot_value)
                if ('万' in hot_value) and hot_value_re:
                    hot_value = hot_value_re.group()
                    item['hot_value'] = int(hot_value)*10000
                else:
                    item['hot_value'] = int(hot_value_re)
                item['media'] = '知乎'
                item['top_type'] = '知乎热榜'
                item['url'] = content['target']['link']['url']
                # item['summary'] = content['target']['excerptArea']['text']
                # print(item)
                yield item






