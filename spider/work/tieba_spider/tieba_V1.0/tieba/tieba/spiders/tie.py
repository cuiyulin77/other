# -*- coding: utf-8 -*-
import scrapy
from tieba.items import TiebaItem
from urllib import parse
from copy import deepcopy
import json
import re
import hashlib
import datetime
import pymysql
from time import  sleep

class TieSpider(scrapy.Spider):
    name = 'tie'
    allowed_domains = ['tieba.baidu.com','baidu.com']
    url_list = []
    kw_list = ['上海','深圳','丰台','海淀','通州','昌平',"东城区","西城区","朝阳区","丰台区","石景山区","海淀区","门头沟区","房山区","通州区","顺义区","昌平区","大兴区","怀柔区","平谷区","密云县","延庆县","黃浦区","南市区","卢湾区","徐汇区","长宁区","静安区","普陀区","闸北区","虹口区","杨浦区","闵行区","宝山区","嘉定区","浦东新区","金山区","松江区","青浦","奉贤","南汇","崇明","和平区","河东区","南开区","河西区","河北区","红桥区","塘沽区","汉沽区","大港区","东丽区","西青区","津南区","北辰区","武清","宝坻","蓟县","静海","宁河","福田区","罗湖区","南山区","盐田区","宝安区","龙岗区","龙华区","坪山区","光明区","功能区","大鹏新区","杭州","宁波","温州","嘉兴","湖州","绍兴","金华","衢州","舟山","台州","丽水","鹿城区","龙湾区","瓯海区","瑞安市","乐清市","永嘉县","平阳县","苍南县","泰顺县","文成县","洞头县"]
    # 连接云服务器mysql
    conn = pymysql.connect(host='47.92.166.26', port=3306, user='root', password='admin8152', database='xuanyuqing',
                           charset='utf8')
    cs1 = conn.cursor()
    # 查询company_popular_feelings中设定的关键字
    cs1.execute('select  title from company_popular_feelings where is_del=0')
    result = cs1.fetchall()
    for res in result:
        # print(res)
        # 把关键字添加到ke_list中
        kw_list.append(res[0])

    for kw in kw_list:
        url = 'http://tieba.baidu.com/f?kw={kw}&ie=utf-8&pn=0'.format(kw=kw)
        url_list.append(url)
    start_urls = url_list

    def parse(self, response):
        print("1"*10)
        li_list = response.xpath("//li[contains(@class,'j_thread_list clearfix')]")
        print("2"*10,li_list)
        for li in li_list:
            item = TiebaItem()
            print("3" * 10)
            item["comm_num"] = li.xpath(".//div[@class='col2_left j_threadlist_li_left']/span/text()").extract_first()
            item['title'] = li.xpath(".//div[contains(@class,'threadlist_title pull_left j_th_tit')]/a/text()").extract_first()
            href = li.xpath(".//div[contains(@class,'threadlist_title pull_left j_th_tit')]/a/@href").extract_first()
            print(href)
            href = response.urljoin(href)
            # print(item)
            yield scrapy.Request(href, callback=self.parse_detail, meta={"item": item})
        # next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        next_url = response.xpath("//a[@class='next pagination-item ']/@href").extract_first()
        # 上边是两种直接提取url的方法，也可以使用url和数字组合的方法
        if next_url is not None:
            num = re.match(".*?&pn=(\d+)$", next_url)
            if num is not None:
                num = num.group(1)
                # 只获取前20页
                if int(num) <= 10:
                    # next_url = parse.urljoin(response.url,next_url)
                    next_url = response.urljoin(next_url)
                    yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail(self, response):
        item = deepcopy(response.meta["item"])
        # print(item)
        div_list = response.xpath("//div[contains(@class,'l_post j_l_post l_post_bright')]")
        content = ' '
        time = ' '
        update_time = ' '
        for i in range(len(div_list)):
            time_part = div_list[i].xpath("./@data-field").extract_first()
            # print('time_part',time_part)
            time_part = json.loads(time_part.replace('&quot;', '"').replace('null', '"" '))
            time_part = time_part['content']['date']
            update_time = time_part
            # 只收录30天之内的信息
            last_time = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M")
            # 判断信息是否30天之内的
            date_bool = update_time > last_time
            if i == 0:
                time = time_part
            content_part = div_list[i].xpath(
                ".//div[@class='d_post_content j_d_post_content  clearfix']/text()").extract()
            content_part = ''.join(content_part)
            # 如果此信息时间是30天之内的，保存
            if date_bool:
                content = content + content_part + '\n'
        # print(content,updata_time,time)
        item['content'] = content
        item['time'] = time
        item['update_time'] = update_time
        item['url'] = response.url
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['read_num'] = 0
        item['fav_num'] = 0  # 点赞，喜欢数量
        item['env_num'] = 0  # 转发量
        # print('item',item)
        content_test = content.replace("\n", '').replace(" ", '')
        # 判断content是否为空，为空，不存
        if len(content_test) > 1:
            yield item
        next_url = response.xpath("(//ul[@class='l_posts_num'])[1]/li/a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            next_url = response.urljoin(next_url)
            title = item['title']
            comm_num = item['comm_num']
            item = TiebaItem()
            item['title'] = title
            item['comm_num'] = comm_num
            yield scrapy.Request(next_url, callback=self.parse_detail, meta={"item": item})
