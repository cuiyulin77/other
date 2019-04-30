# -*- coding: utf-8 -*-

# ====================================================================================================================
# 天天养生爬虫
# 放到线上注意的问题:img图片 路径path,(if 和else各有一处),封面图片路径titlepic(else中有一处),要改成服务器的路径,
# pipeline.py中数据库的配置也要改成服务器的配置
# 不同的爬虫classid是不一样的
# ====================================================================================================================
import scrapy
import re
from lvyou.items import LvyouItem
from lvyou.utils.common import get_md5
from lvyou.utils.common import down_pic
import time
import datetime

# 天天养生http://www.ttys5.com/
class TtysSpider(scrapy.Spider):
    name = 'ttys'
    allowed_domains = ['ttys5.com']
    start_urls = ['http://www.ttys5.com/']

    # def start_requests(self):
    #     url = 'http://www.ttys5.com/xinwen/xinwenhangye/2018-01-30/149711_2.html'
    #     yield scrapy.Request(url,callback=self.get_content)

    def parse(self, response):
        url_list = response.xpath("//ul[@class='menu clearfix']/li/ul/li/a/@href").extract()
        for url in url_list:
            # print(url)
            yield scrapy.Request(url,callback=self.get_detail)

    def get_detail(self,response):
        url_list =response.xpath("//ul[@class='con']/li/a/@href").extract()
        for url in url_list:
            yield scrapy.Request(url,callback=self.get_content)
        next_url = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url,callback=self.get_detail)

    def get_content(self,response):
        # 如果有meta参数,仅提取content
        if response.meta.get('item'):
            item = response.meta.get('item')
            content = response.xpath("//div[@class='ad_580']/following-sibling::p").extract()
            img_list = []
            if content:
                content = ''.join(content).replace(u'\u3000', u'&nbsp;').replace(u'\xa0', u'&nbsp;')
                img_list = response.xpath("//div[@class='ad_580']/following-sibling::p//img/@src").extract()
            elif response.xpath("//p[@class='p_time']/following-sibling::p"):
                content = response.xpath("//p[@class='p_time']/following-sibling::p").extract()
                content = ''.join(content).replace(u'\u3000', u'&nbsp;').replace(u'\xa0', u'&nbsp;')
                img_list = response.xpath("//p[@class='p_time']/following-sibling::p//img/@src").extract()
            if img_list:
                # 遍历图片url,下载并替换为新评的链接
                for img in img_list:
                    # 存放路径:本地服务器是E:\\theping_local_server\\d\\file\\yangsheng\\
                    # 服务器是:E:\\inetpub\\wwwroot\\www.theping.cn\\d\\file\\yangsheng\\
                    # path = r'E:\\inetpub\\wwwroot\\www.theping.cn\\d\\file\\yangsheng\\'   # 166.26的路径
                    path = r'E:\\theping_local_server\\d\\file\\yangsheng\\'
                    today = datetime.date.today()
                    path = path + str(today) + r"\\"
                    # 以图片的路径的MD5加密为文件名
                    pic_name = get_md5(img) + '.jpg'
                    url = response.urljoin(img)
                    # 下载图片到指定路径,
                    down_pic(url, path, pic_name)
                    theping_img = '/d/file/yangsheng/{today}/{pic_name}'.format(today=today, pic_name=pic_name)
                    content = content.replace(img, theping_img)
            item['content'] = item['content'] + content
        else:
            item = LvyouItem()
            item['titlepic'] = response.xpath("//div[@class='content']//img/@src").extract_first()
            if not item['titlepic']:
                item['titlepic'] = ' '
            item['title'] = response.xpath("//h1/text()").extract_first()
            time_str = response.xpath("//p[@class='p_time']/text()").extract_first()
            time_re = re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",time_str)
            if time_re:
                item['time'] = time_re.group()
            # class='ad_580'的div标签之后的p标签
            content = response.xpath("//div[@class='ad_580']/following-sibling::p").extract()
            img_list = []
            if content:
                content = ''.join(content).replace(u'\u3000', u'&nbsp;').replace(u'\xa0', u'&nbsp;')
                img_list = response.xpath("//div[@class='ad_580']/following-sibling::p//img/@src").extract()
            elif response.xpath("//p[@class='p_time']/following-sibling::p"):
                content = response.xpath("//p[@class='p_time']/following-sibling::p").extract()
                content = ''.join(content).replace(u'\u3000', u'&nbsp;').replace(u'\xa0', u'&nbsp;')
                img_list = response.xpath("//p[@class='p_time']/following-sibling::p//img/@src").extract()
            # 不需要的垃圾链接
            drop_strs = response.xpath("//div[@class='content']//p/strong/..|//div[@class='content']//p/a/..").extract()
            print(drop_strs)
            # 把内容里的不需要的垃圾链接替换掉
            for drop_str in drop_strs:
                drop_str = drop_str.replace(u'\u3000', u'&nbsp;').replace(u'\xa0', u'&nbsp;')
                content = content.replace(drop_str,'')
            if img_list:
                print(img_list)
                # 遍历图片url,下载并替换为新评的链接
                for img in img_list:
                    print("img---"*30)
                    # 存放路径:本地服务器是E:\\theping_local_server\\d\\file\\yangsheng\\
                    # 服务器是:E:\\inetpub\\wwwroot\\www.theping.cn\\d\\file\\yangsheng\\
                    # path = r'E:\\inetpub\\wwwroot\\www.theping.cn\\d\\file\\yangsheng\\'   # 166.26的路径
                    path = r'E:\\theping_local_server\\d\\file\\yangsheng\\'
                    today = datetime.date.today()
                    path = path + str(today) + r"\\"
                    # 以图片的路径的MD5加密为文件名
                    pic_name = get_md5(img) + '.jpg'
                    url = response.urljoin(img)
                    # 下载图片到指定路径,
                    down_pic(url, path, pic_name)
                    # /d/file/wenhua/guoxue/2018-05-11/1526014180928023.jpg
                    theping_img = '/d/file/yangsheng/{today}/{pic_name}'.format(today=today, pic_name=pic_name)
                    content = content.replace(img, theping_img)
                    if not item['titlepic']:
                        item['titlepic'] = ' '
                    elif item['titlepic'] == img:
                        # http://www.theping.cn/d/file/renwu/2019-01-12/ae65d3040930bc7ae373d425a0cc6b01.jpg
                        # titlepic = 'http://www.theping.cn' + theping_img                 # 线上服务器使用这个路径
                        titlepic = 'http://192.168.3.15' + theping_img                 # 本地服务器使用这个路径
                        item['titlepic'] = titlepic

            item['content'] = content
            item['media'] = '天天养生网'
            item['classid'] = '166'
            item['url'] = response.url
            item['writer'] = ' '
            item['article_id'] = get_md5(item['url'])
            item['keyid'] = ' '

            if item['time']:
                timeArray = time.strptime(item['time'], "%Y-%m-%d %H:%M:%S")
                item['newstime'] = int(time.mktime(timeArray))
            else:
                item['newstime'] = int(time.time())
        next_url = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        if next_url:
            print("-文章有下一页" * 10)
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.get_content, meta={'item': item})
        else:
            # print('='*30)
            # print(type(item['content']))
            # print(item)
            yield item


        # p_list = response.xpath("//div[@class='ad_580']/following-sibling::p")
        # if p_list:
        #     for p in p_list:
        #         con = p.xpath("./text()").extract()
        #         if not con:
        #             con = p.xpath("./a/img/@src").extract_first()
        #             if con:
        #                 con = ['<img src="{}">'.format(con)]
        #         if con:
        #             content = content + con
        #     content = ''.join(content).replace(u'\u3000', u'&nbsp;').replace(u'\xa0', u'&nbsp;')

        # elif response.xpath("//p[@class='p_time']/following-sibling::p"):
        #     p_list = response.xpath("//p[@class='p_time']/following-sibling::p")
        #     for p in p_list:
        #         con = p.xpath("./text()").extract()
        #         if not con:
        #             con = p.xpath(".//img/@src").extract_first()
        #             if con:
        #                 con = ['<img src="{}">'.format(con)]
        #         if con:
        #             content = content + con
        #     content = ''.join(content).replace(u'\u3000', u'&nbsp;').replace(u'\xa0', u'&nbsp;')
        #     item['content'] = content
        #     item['come_from'] = '天天养生网'
        #     item['classfy'] = '养生'
        #     item['url'] = response.url
        #     print(item)