# coding:utf-8

import scrapy, re, urllib, os, time, sys, random, csv, json, random
from baidu_search.items import BaiduSearchItem
from scrapy import Request
# import MySQLdb as mdb
# import StringIO, pycurl
import importlib

importlib.reload(sys)
# sys.setdefaultencoding('utf-8')

blockSize = 3  # 设置分块
DBUG = 0


def search(req, html, n):
    text = re.search(req, html)
    if text:
        data = text.group(n)
    else:
        data = 'no'
    return data


def font_number(newcontent):
    text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，:：。？、~@#￥%……&*（）“”《》]+".decode("utf8"), "".decode("utf8"),
                  newcontent)  # 去除中英文标点符号
    text2 = re.sub('<[^>]*?>', '', text)  # 去除所有标签
    words_number = len(text2)
    return words_number


def date(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime


current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))


def img_src():
    n = random.randint(1, 312)
    img = "/static/bq_imgs/%s.jpg" % n
    return img


class BDXspider(scrapy.Spider):
    name = "bdx"
    start_urls = []
    l = ['中国','台湾']
    for word in l:
        url = "http://news.baidu.com/ns?word=%s&tn=newstitle&from=news&cl=2&rn=20&ct=0" % word
        start_urls.append(url)

    def parse(self, response):
        html = response.body

        page_div = search(r'<p id="page">([\s\S]*?)</div>', html, 1)
        for page in re.findall(r'href="(.*?)"', page_div):
            if 'rsv_page=1' in page:
                page_url = "http://news.baidu.com%s" % page
                yield Request(url=page_url, callback=self.parse)

        for i in re.findall(r'<h3 class="c-title">([\s\S]*?)</h3>', html):
            key_url = search(r'href="(.*?)"', i, 1)
            host = search('^([^/]*?)/', re.sub(r'(https|http)://', '', key_url), 1)
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, sdch",
                "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Host": host,
                "Pragma": "no-cache",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
            }
            yield Request(url=key_url, headers=headers, callback=self.parse_key)

    def parse_key(self, response):

        charset = search('charset=(.*)', response.headers["Content-Type"], 1).lower()
        if charset == "utf-8":
            body = response.body
        else:
            try:
                body = response.body.decode("gbk").encode("utf-8")
            except:
                body = response.body

        body = search(r'<body.*?>([\s\S]*?)<\/body>', body, 1)
        body = re.sub(r'<script.*?>[\s\S]*?<\/script>', "", body)
        body = re.sub(r'<style.*?>([\s\S]*?)</style>', "", body)
        body = re.sub(r'{[\s\S]*}', "", body)
        body = re.sub(r'<!--.*?-->', "", body)
        body = re.sub(r'<p[^>]*?>', '<p>', body)
        body = re.sub(r'[\t\r\f\v]', '', body)

        try:

            ctexts = body.split("\n")
            textLens = [len(text) for text in ctexts]

            cblocks = [0] * (len(ctexts) - blockSize - 1)
            lines = len(ctexts)
            for i in range(blockSize):
                cblocks = list(map(lambda x, y: x + y, textLens[i: lines - 1 - blockSize + i], cblocks))

            maxTextLen = max(cblocks)

            if DBUG: print(maxTextLen)

            start = end = cblocks.index(maxTextLen)
            while start > 0 and cblocks[start] > min(textLens):
                start -= 1
            while end < lines - blockSize and cblocks[end] > min(textLens):
                end += 1

            content = "".join(ctexts[start:end])
            a = re.sub(r'<(?!p|/p|br)[^<>]*?>', '', content).strip()
            b = re.sub(r'<p[^>]*?>', '<p>', a)
            img = '<img src="%s"/><br/>' % img_src()

            b = img + b

            title = re.sub('(-|_).*', '', search(r'<title>([\s\S]*?)</title>', response.body, 1).strip())

            if font_number(title) >= 5 and font_number(b) >= 50:
                item = BaiduSearchItem()

                item['title'] = title
                item['content'] = b
                item['url'] = response.url
                item['date'] = current_date
                item['cid'] = 25
                print(item)
                # yield item

        except:
            pass