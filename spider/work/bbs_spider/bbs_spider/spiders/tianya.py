# -*- coding: utf-8 -*-
import scrapy
from bbs_spider.utils.common import get_md5
from bbs_spider.items import BbsSpiderItem
import datetime
import re

class TianyaSpider(scrapy.Spider):
    name = 'tianya'
    allowed_domains = ['bbs.tianya.cn']
    start_urls = ['http://bbs.tianya.cn/']

    def parse(self, response):
        block_list = response.xpath("//div[@class='nav_child_box'][position()<8]/ul/li/a/@href").extract()
        # block_list = response.xpath("//div[@class='nav_child_box'][position()<2]/ul/li/a/@href").extract()[:2]
        for block in block_list:
            url = response.urljoin(block)
            # print(url)
            yield scrapy.Request(url,callback=self.get_detail_url)

    def get_detail_url(self,response):
        # 获取帖子列表
        res = response.xpath("//div[@class='mt5']//tr/td[1]/a/@href").extract()
        if res:
            for url in res:
                url = response.urljoin(url)
                # print(url)
                yield scrapy.Request(url, callback=self.get_post)
            # 暂时不翻页,如果翻页会爬的很深,太深的地方都是一些很久远的信息,没有用
            # next_url = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
            # if next_url:
            #     yield scrapy.Request(response.urljoin(next_url),callback=self.get_detail_url)

    def get_post(self,response):
        item = BbsSpiderItem()
        item['title'] = response.xpath('//*[@id="post_head"]/h1/span[1]/span/text()').extract_first()
        # 问答的页面结构有变化,需要其他的提取方式
        if item['title']:
            # pass
            # 主贴
            main_content = response.xpath("//div[@class='bbs-content clearfix']//text()").extract()
            main_time = response.xpath('//*[@id="post_head"]/div[2]/div[2]/span[2]/text()').extract_first()

            # 跟帖
            follow_content = response.xpath("//div[@class='atl-item']//div[@class='bbs-content']//text()").extract()
            # 整合帖子内容
            content = main_content + follow_content
            item['content'] = ' '.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(
                '\u2002', '').replace('\r', ' ').replace('\t', ' ').replace('\n',' ').strip()
            # 某一页的最后一张帖子的时间
            update_time = response.xpath("//div[@class='atl-item'][last()]//div[@class='atl-info']/span[2]/text()").extract_first()
            if update_time:
                update_time = update_time.split('时间：')[1]
                item['time'] = update_time
            else:
                item['time'] = main_time.split('时间：')[1]
            # 只收录30天之内的信息
            last_time = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M")
            # 判断信息是否30天之内的,是布尔值
            if (item['time'] > last_time) and item['content']:
                item['url'] = response.url
                item['article_id'] = get_md5(item['url'])
                item['media'] = '天涯论坛'
                item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                read_num = response.xpath('//*[@id="post_head"]/div[2]/div[2]/span[3]/text()').extract_first()
                item['read_num'] = read_num.split('点击：')[1]
                comm_num = response.xpath('//*[@id="post_head"]/div[2]/div[2]/span[4]/text()').extract_first()
                item['comm_num'] = comm_num.split('回复：')[1]
                item['fav_num'] = '0'
                item['env_num'] = '0'
                item['media_type'] = '论坛'
                # item['come_from'] = ''
                item['addr_city'] = ''
                item['addr_province'] = '全国'
                # print(item)
                yield item
            next_url = response.xpath("//a[contains(text(),'下页')]/@href").extract_first()
            if next_url:
                next_url = response.urljoin(next_url)
                print(next_url,'*'*200)
                yield scrapy.Request(next_url,callback=self.get_post)
        # 提取问答页面数据
        elif response.xpath("//div[@class='q-title']"):
            item['title'] = response.xpath("//h1//text()").extract_first()
            # 主贴
            main_content = response.xpath("//div[@class='q-content atl-item']/div[@class='text']/text()").extract()
            top_str = response.xpath("//span[@class='ml5']/text()").extract()
            top_str_re = re.search("时间：(\d+-\d+-\d+ \d+:\d+:\d+)\xa0点击：(\d+)\xa0回复：(\d+)",top_str[1])
            item['read_num'] = 0
            item['comm_num'] = 0
            if top_str_re:
                item['time'] = top_str_re.group(1)
                item['read_num'] = top_str_re.group(2)
                item['comm_num'] = top_str_re.group(3)
            follow_content = response.xpath("//div[@class='answer-item atl-item']/div[@class='content']/text()").extract()
            content = main_content+follow_content
            item['content'] = ' '.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(
                '\u2002', '').replace('\r', ' ').replace('\t', ' ').replace('\n',' ').strip()
            update_time = response.xpath("//div[@class='answer-item atl-item'][last()]/div[@class='user']/text()").extract()[1]
            update_time = update_time.replace(u'\xa0', u'').replace('\r', '').replace('\n','').strip()
            if update_time:
                item['time'] = update_time
            # 只收录30天之内的信息
            last_time = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M")
            # 判断信息是否30天之内的,是布尔值
            if (item['time'] > last_time) and item['content']:
                item['url'] = response.url
                item['article_id'] = get_md5(item['url'])
                item['media'] = '天涯论坛'
                item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                item['fav_num'] = '0'
                item['env_num'] = '0'
                item['media_type'] = '论坛'
                # item['come_from'] = ''
                item['addr_city'] = ''
                item['addr_province'] = '全国'
                # print(item)
                yield item


