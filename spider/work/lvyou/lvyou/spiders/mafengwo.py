# -*- coding: utf-8 -*-
import scrapy
import json
import re
from lxml import etree

class MafengwoSpider(scrapy.Spider):
    name = 'mafengwo'
    allowed_domains = ['www.mafengwo.cn']
    start_urls = ['https://www.mafengwo.cn']

    def start_requests(self):
        # 最新游记,"type":0是最热游记
        for n in range(1, 3):
            next = 'http://pagelet.mafengwo.cn/note/pagelet/recommendNoteApi?&params={"type":3,"objid":0,"page":%s,"ajax":1,"retina":1}' % n
            yield scrapy.Request(url=next, callback=self.parse)
        # 推荐攻略
        # for i in range(3)[1:]:
        #     yield scrapy.Request('https://www.mafengwo.cn/gonglve/', method="POST", body=json.dumps({"page":i}), headers={'Content-Type': 'application/json'},
        #               callback=self.parse_detail)

    def parse(self, response):
        html = json.loads(response.text)
        html = str(html)
        a_list = re.findall(r'<a href="(/i/.*?.html)"', html)
        a_list = set(a_list)
        for a in a_list:
            # 没法用response.urljoin,因为url头是http://pagelet.mafengwo.cn
            url = 'http://www.mafengwo.cn' + a
            yield scrapy.Request(url,callback=self.get_content)

    # def parse_detail(self, response):
    #     url_list = response.xpath("//div[@class='feed-item _j_feed_item']/a/@href").extract()
    #     print(url_list)

    def get_content(self,response):
        item = {}
        url = response.url
        title = response.xpath('//h1/text()').extract_first()
        if not title:
            title = response.xpath('//h1/text()').extract()
        item['title'] = title
        content = response.xpath("//div[@class='va_con _j_master_content']//p//text()").extract()
        item['url'] = url
        item['content'] =  ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n','').replace(' ','')
        item['pic_url'] = re.findall(r'data-rt-src="(.*?)"', response.text)  # 第一分页所有的图片链接在一个列表里
        # 是否有下一页,has_more值为True,False
        has_str =  re.findall(r'"has_more":(\w+),"pv_workkey"', response.text)
        has_more = None
        if has_str:
            has_str = has_str[0]
            if has_str == 'true':
                has_more = True
            else:
                has_more = False
        # 获取组成下一页url的关键参数
        seq_last = re.findall(r'data-seq="(.*?)"', response.text)
        new_url = url.split('/')[-1]
        idnum = new_url.replace('.html', '')  # 每一篇文章的id参数的值

        if (seq_last != []) and has_more:
            seq_last = seq_last[-1]
            detail_url = 'http://www.mafengwo.cn/note/ajax.php?act=getNoteDetailContentChunk&id=%s&seq=%s' % (
            idnum, seq_last)
            # 下一页的数据
            yield scrapy.Request(url=detail_url, callback=self.long_text,meta={'item':item,"idnum":idnum})
        else:
            # yield item
            print(item)

    def long_text(self,response):
        item = response.meta['item']
        idnum = response.meta['idnum']
        html_json =  response.text
        html_json = html_json.replace('\r','').replace('\n','')
        text = json.loads(html_json)
        # 生成etree对象,以便使用xpath
        html = text['data']['html']
        html_etree = etree.HTML(html)
        # 第二页的内容
        content = html_etree.xpath("//p//text()")
        content = ''.join(content).replace(u'\u3000', u' ').replace('\n', '').replace(" ", '')
        img_list = html_etree.xpath("//img/@data-rt-src")
        item['pic_url'] = item['pic_url'] + img_list
        item['content'] = item['content'] + content
        # 是否还有下一页,Ture 或者False
        has_more = text['data']['has_more']
        seq_last = re.findall(r'data-seq="(.*?)"', html)
        if (seq_last != []) and has_more:
            seq_last = seq_last[-1]
            detail_url = 'http://www.mafengwo.cn/note/ajax.php?act=getNoteDetailContentChunk&id=%s&seq=%s' % (
                idnum, seq_last)
            # 下一页的数据
            yield scrapy.Request(url=detail_url, callback=self.long_text, meta={'item': item,"idnum":idnum})

        else:
            # yield item
            print(item)

