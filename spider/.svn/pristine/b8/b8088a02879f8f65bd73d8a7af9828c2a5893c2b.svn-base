# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
import hashlib

# ============================================================
# 通过百度新闻的搜索,获取新闻列表,并在新闻列表页直接提取新闻简介,url等相关信息.
# 因为提取的并不是新闻全文,所以后期数据分析,词云等生成时并不精确
# ============================================================

class BaiSearchSpider(scrapy.Spider):
    name = 'bai_search'
    allowed_domains = ['news.baidu.com']
    # 现在把start_urls固定化,后期根据情况,调用关键词进行设置
    start_urls = ['http://news.baidu.com/ns?word=%E5%A7%90%E5%A4%AB%E7%9A%84%E5%B0%8F%E8%8F%9C&tn=news&from=news&cl=2&rn=20&ct=1']

    def parse(self, response):
        div_list = response.xpath("//div[@id='container']//div[@class='result']")
        for div in div_list:
            item = {}
            item['title'] = ''.join(div.xpath("./h3/a/text()").extract())
            item['title'] = item['title'].replace('\n','').replace(' ','').replace(u'\u2022','')
            item['url'] = div.xpath("./h3/a/@href").extract_first()
            content = div.xpath("./div[contains(@class,'c-summary')]/div/text()|./div[contains(@class,'c-summary')]/text()").extract()
            item['content'] = ''.join(content).replace('\n','').replace(' ','').replace('\t','').replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\u2022','')
            item['media'] = '百度新闻'
            time_text = div.xpath("./div[contains(@class,'c-summary')]//p/text()").extract()
            time_text = ''.join(time_text).replace('\n','').replace(' ','').replace('\t','').replace(u'\u3000', u' ').replace(u'\xa0', u' ').split()[1]
            if '分钟' in time_text:
                print("'分钟' in created_at:")
                re_time = re.match('(\d+)分钟前', time_text)
                if re_time is not None:
                    item['time'] = (
                    datetime.datetime.now() - datetime.timedelta(minutes=int(re_time.group(1)))).strftime(
                        "%Y-%m-%d %H:%M")
            if '小时' in time_text:
                print("'小时' in created_at:")
                re_time = re.match('(\d+)小时前', time_text)
                if re_time is not None:
                    item['time'] = (datetime.datetime.now() - datetime.timedelta(hours=int(re_time.group(1)))).strftime(
                        "%Y-%m-%d %H:%M")
            else:
                item['time'] = time_text.replace("年",'-').replace("月",'-').replace("日",' ')
            m = hashlib.md5()
            url = str(item['url'])
            m.update(str(url).encode('utf8'))
            article_id = str(m.hexdigest())
            item['article_id'] = article_id
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            try:
                print(item)
                # return item
            except:
                pass
        next_page = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        if next_page:
            next_url = response.urljoin(next_page)
            print("下一页"*10)
            yield scrapy.Request(next_url,callback=self.parse)
