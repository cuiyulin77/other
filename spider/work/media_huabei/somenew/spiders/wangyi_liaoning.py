# -*- coding: utf-8 -*-
import scrapy
import re
import json
from copy import deepcopy
import datetime
# from somenew.utils.common import get_md5
from somenew.items import SomenewItem
import hashlib

# =============================================================================
# 网易内蒙古爬虫 首页:liaoning.news.163.com
# =============================================================================
class WangyiLiaoningSpider(scrapy.Spider):
    name = 'wangyi_neimenggu'
    allowed_domains = ['news.163.com']
    json_url_list = ['http://bendi.news.163.com/neimengu/special/04138EHT/nmgxxl.js',
                     ]

    for j in range(len(json_url_list)):
        for i in range(4)[2:]:
            format_str = '_0{}.js'.format(i)
            print(format_str)
            url_new = json_url_list[j].replace('.js', format_str)
            print(url_new)
            json_url_list.append(url_new)
    start_urls = json_url_list

    def parse(self, response):
        html = response.body.decode('gbk')
        html = html.replace('\n','').replace(' ','')
        html_re = re.match(r'^data_callback\((.*)?\)$', html, re.S)
        if html_re:
            html_str = html_re.group(1)
            html_list = json.loads(html_str)
            for dic in html_list:
                item = SomenewItem()
                url = dic['docurl']
                if url:
                    item['comm_num'] = dic['tienum']
                    item['title'] = dic['title']
                    try:
                        item['time'] = datetime.datetime.strptime(dic['time'],'%m/%d/%Y%H:%M:%S')
                        item['time'] = dt = datetime.datetime.strftime(item['time'], "%Y-%m-%d %H:%M:%S")
                        yield scrapy.Request(url, callback=self.parse_detail, meta={'item': item})
                    except Exception as e:
                        print('时间格式解析错误',e)

    def parse_detail(self,response):
        item = deepcopy(response.meta['item'])
        item['come_from'] = response.xpath("//a[@id='ne_article_source']//text()").extract_first()    # 文章来源,es和items.py中暂时没有这个字段
        content = response.xpath("//div[@class='post_text']//p//text()").extract()
        item['content'] = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        item['url'] = response.url
        m = hashlib.md5()
        m.update(str(item['url']).encode('utf8'))
        item['article_id'] = m.hexdigest()
        item['media'] = '网易内蒙古'
        item['media_type'] = '网媒'
        item['addr_province'] = '内蒙古自治区'
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['fav_num'] = 0
        item['env_num'] = 0
        item['read_num'] = 0
        yield item
