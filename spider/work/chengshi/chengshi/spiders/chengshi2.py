# -*- coding: utf-8 -*-
import scrapy
from chengshi.items import ChengshiItem
from chengshi.util.get_md5 import get_md,down_pic
import re,time,datetime


class Chengshi2Spider(scrapy.Spider):
    name = 'chengshi2'
    allowed_domains = ['china.com.cn']
    start_urls = ['http://city.china.com.cn/index.php?m=content&c=index&a=lists&catid=9']

    def parse(self, response):
        res = response.xpath('//h4/a/@href').extract()
        for node in res:
            yield scrapy.Request(node, callback=self.detail)
    def detail(self,response):
        item = ChengshiItem()
        item['title'] = response.xpath("//*[@id=\"main\"]/div[1]/h1/text()").extract_first()
        item['url'] = response.url
        item['article_id'] = get_md(response.url)
        item['keyid'] = ''
        item['media'] = response.xpath('//*[@id="main"]/div/div/p[last()]/text()').extract_first().split('来源：')[1]
        item['classid'] ='168'
        item['writer'] = ''
        item['newstime'] = response.xpath("//*[@id=\"main\"]/div[1]/div[3]/span[2]/text()").extract()[0].split('时间：')[1][:-3]
        timeArray = time.strptime(item['newstime'], "%Y-%m-%d %H:%M")
        item['newstime'] = int(time.mktime(timeArray))
        item['content'] = response.xpath("//div[@class=\"content\"]/child::*").extract()
        t =''
        for i in item['content']:
            t += i
        item['titlepic'] = response.xpath('//div[@class="content"]/*//@src').extract()[0]
        pic_list = response.xpath('//div[@class="content"]/*//@src').extract()
        # url,path,pic_name
        path = r'E:\\theping_local_server\\d\\file\\chengshi\\'
        down_pic(item['url'],path,)
        for pic in pic_list:
            path = r'E:\\theping_local_server\\d\\file\\yangsheng\\'
            today = datetime.date.today()
            path = path + str(today) + r"\\"
            # 以图片的路径的MD5加密为文件名
            pic_name = get_md(pic) + '.jpg'
            # 下载图片到指定路径,
            down_pic(pic, path, pic_name)
            theping_img = '/d/file/chengshi/{today}/{pic_name}'.format(today=today, pic_name=pic_name)
            content = t.replace(pic, theping_img)
            if  not item['titlepic']:
                item['titlepic'] = ' '
            elif item['titlepic'] == pic:
                # http://www.theping.cn/d/file/renwu/2019-01-12/ae65d3040930bc7ae373d425a0cc6b01.jpg
                # titlepic = 'http://www.theping.cn' + theping_img                 # 线上服务器使用这个路径
                titlepic = 'http://192.168.3.15' + theping_img  # 本地服务器使用这个路径
                item['titlepic'] = titlepic







