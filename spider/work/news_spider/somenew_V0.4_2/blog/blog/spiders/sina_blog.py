# -*- coding: utf-8 -*-
import scrapy
import re
from copy import deepcopy
import datetime
import time
import hashlib
from blog.items import BlogItem
from retrying import retry

class SinaBlogSpider(scrapy.Spider):
    name = 'sina_blog'
    allowed_domains = ['sina.com.cn']
    bang_list = []
    for i in range(11)[1:]:
        # 'http://blog.sina.com.cn/lm/iframe/top/alltop_more_new_2.html'
        url = 'http://blog.sina.com.cn/lm/iframe/top/alltop_more_new_'+str(i)+'.html'
        bang_list.append(url)
    start_urls = bang_list

    @retry(stop_max_attempt_number=3)
    def parse(self, response):
        # cookies = 'SINAGLOBAL=172.16.118.86_1515748454.289468; SCF=ApzIBQQKtU23e_2oHJqgw3Rt4bbgTMu9OFvdgEi4uaubdjFtho2JHHK7O1YTG1sqOH0jz7AOZFsvsv5ppSEJbFc.; UOR=,www.sina.com.cn,; SGUID=1517375958816_30575870; U_TRS1=00000043.19092682.5a7151db.62e6b414; vjuids=8e7565c31.162a31c054f.0.bc05568fecf7a; bdshare_firstime=1526348962753; lxlrtst=1526373620_o; _s_loginStatus=1178130382; lxlrttp=1526753611; Apache=219.142.86.68_1527038417.517043; U_TRS2=00000044.2bf32366.5b04c1d2.5de1fade; BLOGUSERNNNNAME=undefined; ULV=1527038417389:30:14:4:219.142.86.68_1527038417.517043:1527038412153; sinaGlobalRotator_http%3A//blog.sina.com=485; SessionID=k1k4fhj6fp68kl99sp6ba16a57; IDC_LOGIN=BJ%3A1527038482; blogAppAd_blog7index=1; _s_loginuid=1178130382; vjlast=1523154945.1527054561.11; rotatecount=4; BLOG_TITLE=Ymer%E7%9A%84%E5%8D%9A%E5%AE%A2; mblog_userinfo=uid%3D1250705634%26nick%3DYmer; hqEtagMode=0; SUB=_2AkMsWYKCdcPxrAJQn_AUz2vhZI9H-jyfjOt0An7tJhMyAhh87lUIqSVutBF-XAogAH8-5XD4W0eM-_naR8wAXc0L; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WWzDWhRLCccpMlhR_xwOpLl5JpV8GDydJUoIs8V9c8VBGSDdJ2Vqcv_'
        print("1"*100)
        # 获取博客排行榜里的单页博客人员列表
        class_list = response.xpath("//table//tr/td[2]/a/@href").extract()
        for cls in class_list:
            print("2" * 100)
            yield scrapy.Request(cls,callback=self.get_blog_url)
                                 # cookies={i.split("=")[0]: i.split("=")[-1] for i in cookies.split("; ")})

    # 获取博文目录链接
    def get_blog_url(self,response):
        print("3" * 100)
        item = BlogItem()
        catelog_url = response.xpath("//*[@id='blognav']/div[2]/span[2]/a/@href").extract_first()  # 博文目录链接
        item['blogger_name'] = response.xpath("//strong[@id='ownernick']/text()").extract_first()  # 博主名字
        yield scrapy.Request(catelog_url, callback=self.get_detail, meta={"item": item})

    # 获取每一页博文目录里的博文链接
    def get_detail(self,response):
        print("5" * 100)
        item = deepcopy(response.meta['item'])
        blog_url_list = response.xpath("//div[@class='articleList']/div/p/span[2]/a/@href").extract()
        for blog_url in blog_url_list:
            item['url'] = blog_url
            yield scrapy.Request(blog_url,callback=self.get_content,meta={'item':item})

        next_url = response.xpath("//li[@class='SG_pgnext']/a/@href").extract_first()
        if next_url is not None:
            print("6" * 100)
            yield scrapy.Request(next_url,callback=self.get_detail,meta={'item':item})

    # 获取文章内容
    @retry(stop_max_attempt_number=3)
    def get_content(self,response):
        print("7" * 100)
        item = deepcopy(response.meta['item'])
        item['title'] = response.xpath("//h2/text()").extract_first()
        item['publish_time'] = response.xpath("//span[@class='time SG_txtc']/text()").extract_first()
        item['publish_time'] = item['publish_time'].replace("(",'').replace(')','').replace('-','/')
        # sina_keyword_ad_area2
        content = response.xpath("//div[@id='sina_keyword_ad_area2']")
        # item['content'] = response.xpath("//")
        item['content'] = content[0].xpath('string(.)').extract()[0].replace('\n', '').replace('\t', ' ')
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['media'] = '新浪博客'

        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        print(item)
        yield item






