# -*- coding: utf-8 -*-
# ====================================================================================================================
# 搜狐爬虫
# 放到线上注意的问题:img图片 路径path,(if 和else各有一处),封面图片路径titlepic(else中有一处),要改成服务器的路径,
# pipeline.py中数据库的配置也要改成服务器的配置
# 需要修改classid,不同的爬虫classid是不一样的,
# ====================================================================================================================

import scrapy
from lvyou.items import LvyouItem
from lvyou.utils.common import get_md5
from lvyou.utils.common import down_pic
import datetime
import time
import json

class SohuFoodSpider(scrapy.Spider):
    name = 'sohu_food'
    allowed_domains = ['sohu.com']
    start_urls = ['http://sohu.com/']

    def start_requests(self):
        # 美食:http://chihe.sohu.com/
        for i in range(1,21):
            # 3.15服务器美食是:美食(167),
            # 166.26美食的classid是(171)
            classid = 167
            # 栏目分类
            classfy = 'meishi'
            # classid = 171
            food_url_json = 'http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=28&page={}&size=20'.format(i)
            yield scrapy.Request(food_url_json,callback=self.parse,meta={'classid':classid,"classfy":classfy})
        # 旅游 http://travel.sohu.com/
        for i in range(1,21):
            # 3.15服务器旅游是:美食(165),
            # 166.26旅游的classid是(52)
            classid = 52
            classfy = "lvyou"
            travel_url_json = 'http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=29&page={}&size=20'.format(i)
            yield scrapy.Request(travel_url_json, callback=self.parse, meta={'classid': classid, "classfy": classfy})

    def parse(self, response):
        classid = response.meta.get('classid')
        classfy = response.meta.get('classfy')
        html = response.body.decode()
        html_json = json.loads(html)
        for pro in html_json:
            item = LvyouItem()
            titlepic_url = response.urljoin(pro.get('focus'))
            # 存放路径:本地服务器是E:\\theping_local_server\\d\\file\\yangsheng\\
            # 服务器是:E:\\inetpub\\wwwroot\\www.theping.cn\\d\\file\\yangsheng\\
            # path = r'E:\\inetpub\\wwwroot\\www.theping.cn\\d\\file\\yangsheng\\'   # 166.26的路径
            path = r'E:\\theping_local_server\\d\\file\\{}\\'.format(classfy)
            today = datetime.date.today()
            path = path + str(today) + r"\\"
            # 以图片的路径的MD5加密为文件名
            pic_name = get_md5(titlepic_url) + '.jpg'
            # 下载图片到指定路径,
            down_pic(titlepic_url, path, pic_name)
            # /d/file/wenhua/guoxue/2018-05-11/1526014180928023.jpg
            theping_img = '/d/file/{classfy}/{today}/{pic_name}'.format(classfy=classfy,today=today, pic_name=pic_name)
            # titlepic = 'http://www.theping.cn' + theping_img                 # 线上服务器使用这个路径
            titlepic = 'http://192.168.3.15' + theping_img                     # 3.15服务器使用这个路径
            item['titlepic'] = titlepic
            item['title'] = pro.get('title')
            item['classid'] = classid
            publishtime = pro.get('publicTime')
            item['newstime'] = int(publishtime/1000)
            item['writer'] = pro.get("authorName")
            article_id = pro.get('id')
            authorId = pro.get('authorId')
            article_url = "http://www.sohu.com/a/{}_{}".format(article_id, authorId)
            yield scrapy.Request(article_url,callback=self.get_content,meta={'item':item,"classfy":classfy})

    def get_content(self,response):
        item = response.meta['item']
        classfy = response.meta.get('classfy')
        content= response.xpath("//article[@class='article']").extract()
        content = ''.join(content)
        drop_strs = response.xpath("//article[@class='article']//a|//article[@class='article']//p[@data-role='editor-name']").extract()
        for drop_str in drop_strs:
            # drop_str = drop_str.replace(u'\u3000', u'&nbsp;').replace(u'\xa0', u'&nbsp;')
            content = content.replace(drop_str, '')
        img_list =response.xpath("//article[@class='article']//img/@src").extract()
        if img_list:
            print(img_list)
            # 遍历图片url,下载并替换为新评的链接
            for img in img_list:
                print("img---" * 30)
                # 存放路径:本地服务器是E:\\theping_local_server\\d\\file\\meishi\\
                # 服务器是:E:\\inetpub\\wwwroot\\www.theping.cn\\d\\file\\meishi\\
                # path = r'E:\\inetpub\\wwwroot\\www.theping.cn\\d\\file\\{}\\'.format(classfy)   # 166.26的路径
                path = r'E:\\theping_local_server\\d\\file\\{}\\'.format(classfy)
                today = datetime.date.today()
                path = path + str(today) + r"\\"
                # 以图片的路径的MD5加密为文件名
                pic_name = get_md5(img) + '.jpg'
                url = response.urljoin(img)
                # 下载图片到指定路径,
                down_pic(url, path, pic_name)
                # /d/file/wenhua/guoxue/2018-05-11/1526014180928023.jpg
                theping_img = '/d/file/{classfy}/{today}/{pic_name}'.format(classfy=classfy,today=today, pic_name=pic_name)
                content = content.replace(img, theping_img)
        item['content'] = content
        item['url'] = response.url
        item['article_id'] = get_md5(item['url'])
        item['keyid'] = ' '
        item['media'] = '搜狐'
        print(item)
        # yield item




