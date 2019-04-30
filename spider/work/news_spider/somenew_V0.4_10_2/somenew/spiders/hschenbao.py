# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
import time
import datetime
from urllib import parse
from somenew.items import SomenewItem

class HschenbaoSpider(scrapy.Spider):
    name = 'hschenbao' # 华商晨报,每日凌晨一点左右更新
    allowed_domains = ['hsxiang.com']
    start_urls = ['http://www.hsxiang.com/html/']

    def parse(self, response):
        # 获取月份节点
        node_list = response.xpath("//tr/td[2]/a/@href").extract()
        # now_date = time.strftime('%Y/%m/%d',time.localtime(time.time()))
        for node in node_list:
            try:
                use_node = re.match(r'^\d+-\d+\/',node).group()

            except Exception:
                use_node = None
            if use_node is not None:
                node_href = 'http://e.hsxiang.com/html/'+use_node
                yield scrapy.Request(node_href,callback=self.parse_get_node)
    def parse_get_node(self,response):
        # 获取每日报刊文件夹节点
        day_list = response.xpath("//tr/td[2]/a/text()").extract()
        for day in day_list:
            try:
                day_url = re.match(r'\d+\/',day).group()
            except Exception:
                day_url = None
            if day_url is not None:
                day_href = parse.urljoin(response.url,day_url)
                # 匹配url地址，获取日期，过滤掉100天之前的内容（http://e.hsxiang.com/html/2018-05/07/）
                try:
                    get_date = re.match("^h.*?\/(\d+-\d+\/\d+)\/", day_href).group(1)

                except Exception:
                    get_date = None
                if get_date is not None:
                    # 将‘-’替换为'/'  2018-05/07--》2018/05/07
                    start_date = re.sub(r"\-", '/', get_date)
                    # 获取当前日期
                    end_date = time.strftime("%Y/%m/%d")
                    # 将报纸日期转化为秒
                    start_sec = time.mktime(time.strptime(start_date, '%Y/%m/%d'))
                    # 将爬取时间转化为秒
                    end_sec = time.mktime(time.strptime(end_date, '%Y/%m/%d'))
                    # 计算时间差
                    work_days = int((end_sec - start_sec)/(24 * 60 * 60))
                    # 时间差小于100天，获得这个信息
                    if work_days<100:
                        yield scrapy.Request(day_href,callback=self.parse_get_content_href)

    def parse_get_content_href(self,response):
        content_list = response.xpath("//tr/td[2]/a/text()").extract()
        for content in content_list:
            try:
                content_url = re.match("^c.*",content).group()
            except Exception:
                content_url = None
            if content_url is not None:
                content_href = parse.urljoin(response.url,content_url)
                yield scrapy.Request(content_href,callback=self.get_content)

    def get_content(self,response):
        # 获取页面信息
        # 获取标题
        title = response.xpath("//tr[1]/td/table/tbody/tr/td/strong/text()").extract_first()
        if title is not None:
            item = SomenewItem()
            item['title'] = response.xpath("//tr[1]/td/table/tbody/tr/td/strong/text()").extract_first()
            item['content'] = str(response.xpath("//div[@id='ozoom']//p//text()").extract())
            item['content'] = ''.join(item["content"]).replace(u'\\u3000', u' ').replace(u'\\xa0', u' ')
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['url'] = response.url
            try:
                s = re.match("^h.*?\/(\d+-\d+\/\d+)\/.*", item['url']).group(1)
            except Exception:
                s = item['create_time']
            s.replace('-', '/')
            s = re.sub(r"\-", '/', s)
            item['time'] = s
            item['media'] = '华商晨报'
            m = hashlib.md5()
            url = str(item['url'])
            m.update(str(url).encode('utf8'))
            article_id = str(m.hexdigest())
            # m.update(str(item['url'])).encode('utf-8')
            item['article_id'] = article_id
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            yield item
