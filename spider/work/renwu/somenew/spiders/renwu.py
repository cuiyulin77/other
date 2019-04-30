# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
from w3lib.html import remove_tags
import re
import hashlib
import datetime,time
import pymysql
from time import sleep
import random
from somenew.utils.common import get_md5,down_pic
from somenew.utils.baidu import baidu


class WeixingongzhonghaoFabu1Spider(scrapy.Spider):
    name = 'renwu'
    allowed_domains = ['hqrw.com.cn']
    start_urls = ['http://www.hqrw.com.cn/culture/culturex/19.shtml']
    custom_settings = {'DOWNLOAD_DELAY': random.uniform(0.7,1.1)}
    def parse(self, response):
         for i in range(1,21):
             url ='http://www.hqrw.com.cn/culture/culturex/{}.shtml'.format(i)
        # url ='http://www.hqrw.com.cn/culture/culturex/19.shtml'
             yield scrapy.Request(url,callback=self.get_detail_url)

    def get_detail_url(self,response):
         res = response.xpath('/html/body/div[3]/div/div[2]/ul/li/a/@href').extract()
         item = SomenewItem()
         for url in res:
              item['titlepic'] = response.xpath('/html/body/div[3]/div/div[2]/ul/li[1]/a/div/div[1]/div/img/@src').extract_first()
              yield scrapy.Request(url, callback=self.get_detail,meta={'item':item})
    def get_detail(self,response):
          print(response.url)
          item = response.meta['item']
          today = datetime.date.today()
          # E:\\inetpub\\wwwroot\\www.theping.cn\\d\\file\\yangsheng\\ #服务器
          path = 'E:\\inetpub\\wwwroot\\www.theping.cn\\d\\file\\renwu\\{}\\'.format(today) + 'titlepic' + '\\'
          # 以图片的路径的MD5加密为文件名
          pic_name = get_md5(item['titlepic']) + '.jpg'
          url = response.urljoin(item['titlepic'])
          # 下载图片到指定路径,
          down_pic(url, path, pic_name)
          # theping_img = 'http://' + '192.168.3.15/' + 'd/file/renwu/{}/titlepic/{}'.format(today, pic_name) 3.16服务器
          theping_img = 'http://www.theping.cn' + '/d/file/renwu/{}/titlepic/{}'.format(today, pic_name)
          item['titlepic'] = item['titlepic'].replace(item['titlepic'], theping_img)
          item['title'] =response.xpath('//div[1]/div[2]/h3/text()').extract_first().replace('\xa0',' ')
          item['url'] = response.url
          item['content'] = response.xpath("/html/body/div[3]/div/div[1]/div/div[2]/div[1]/div[1]/p[1]/following-sibling::* [not(@class=\"state\")]").extract()
          data = ''
          for i in item['content']:
              data += i
          item['content'] = data
          item['article_id'] = get_md5(item['url'])
          item['media'] = response.xpath('/html/body/div[3]/div/div[1]/div/div[2]/div[1]/div[2]/div[2]/ul/li[3]/span/text()').extract_first()
          item['classid'] = '164'
          item['keyid'] = ''
          item['writer'] = response.xpath('/html/body/div[3]/div/div[1]/div/div[2]/div[1]/div[2]/div[2]/ul/li[2]/span/text()').extract_first()
          if item['writer'] is None:
               item['writer']= ''
          item['newstime'] = response.xpath('/html/body/div[3]/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/ul/li[1]/text()').extract_first()
          if item['newstime']:
               timeArray = time.strptime(item['newstime'], "%Y-%m-%d %H:%M")
               item['newstime'] = int(time.mktime(timeArray))
          else:
               item['newstime'] = int(time.time())
          if item['titlepic'] and item['content']:
               pic_url = response.xpath('//div[@class="passage-content  contenth article-content fontSizeSmall BSHARE_POP"]/*/img/@src').extract()
               print(pic_url,'11111111111111111111111111111111111111111111111')
               for img in pic_url:
                    # path = r'E:\\theping_local_server\\d\\file\\renwu\\' #3.15服务器
                    path = r'E:\\inetpub\\wwwroot\\www.theping.cn\\d\\file\\renwu\\'
                    path = path + str(today) + r"\\"
                    # 以图片的路径的MD5加密为文件名
                    pic_name = get_md5(img) + '.jpg'
                    url = response.urljoin(img)
                    # 下载图片到指定路径,
                    down_pic(url, path, pic_name)
                    # /d/file/wenhua/guoxue/2018-05-11/1526014180928023.jpg
                    # titlepic1 = '/d/file/renwu/{today}/{pic_name}'.format(today=today, pic_name=pic_name) #3.15服务器
                    titlepic1 = '/d/file/renwu/{today}/{pic_name}'.format(today=today, pic_name=pic_name)
                    titlepic = 'http://www.theping.cn' + titlepic1
                    # titlepic = 'http://' + '192.168.3.15' + titlepic1 #3.15服务器
                    print(img, titlepic)
                    item['content'] = item['content'].replace(img, titlepic)
                    print(item)
                    yield item






