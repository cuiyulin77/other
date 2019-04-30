# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
import hashlib
from somenew.items import SomenewItem


class DizhenjuSpider(scrapy.Spider):
    name = 'dizhenju'
    allowed_domains = ['cea.gov.cn']
    # start_urls = ['https://www.cea.gov.cn/',]
    start_urls = ['https://www.cea.gov.cn/cea/xwzx/fzjzyw/index.html',      # 防震减灾要闻
                  'https://www.cea.gov.cn/cea/xwzx/xydt/index.html',        #  行业动态
                  'https://www.cea.gov.cn/cea/xwzx/sxgz/index.html',        # 市县工作
                  'https://www.cea.gov.cn/cea/xwzx/mtbb/index.html',        # 媒体播报
                  'https://www.cea.gov.cn/cea/xwzx/rdbd/index.html',         # 热点报道
                  'https://www.cea.gov.cn/cea/xwzx/zyzt/index.html',         # 重要专题
                  'https://www.cea.gov.cn/cea/zwgk/tzgg/index.html',         # 通知公告
                  'https://www.cea.gov.cn/cea/zwgk/zcjd/index.html',         # 政策解读
                  'https://www.cea.gov.cn/cea/zwgk/rsxx/index.html',         # 人士信息
                  'https://www.cea.gov.cn/cea/zwgk/zbcg/index.html',         # 招标采购
                  'https://www.cea.gov.cn/cea/zwgk/czzj/index.html',         # 财政资金
                  'https://www.cea.gov.cn/cea/zwgk/ghjh/index.html',         # 规划计划
                  'https://www.cea.gov.cn/cea/zwgk/yjzq/index.html',         # 意见征求
                  ]


    def parse(self, response):
        href_list = response.xpath("//div[contains(@class,'listNews')]/ul/li/a/@href").extract()
        for href in href_list:
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.get_content)
        next_href = response.xpath("//a[text()='下一页']/@tagname").extract_first()
        next_url = response.urljoin(next_href)
        try:
            next_url_num = int(re.match(r'.*?(\d+).html$', next_url).group(1))
        except Exception as e:
            next_url_num = 1
            print(e)
        if (next_url != response.url) and (next_url_num <= 10):
            yield scrapy.Request(next_url, callback=self.parse)

    def get_content(self, response):
        item = SomenewItem()
        item['url'] = response.url
        item['title'] = response.xpath("//h1[@id='title']/text()").extract_first()
        time_text = response.xpath("//div[@class='pages-date']/span[1]/text()").extract_first()
        item['time'] = re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", time_text)[0]
        come_from = response.xpath("//div[@class='pages-date']/span[2]/span/text()").extract_first()
        item['come_from'] = come_from.replace('\xa0','').replace('\n','').strip()
        item['media'] = '中国地震局'
        item['content'] = response.xpath("//div[@id='news_content']/p/text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\\u3000', u' ').replace(u'\\xa0', u' ').replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace("\n",' ')
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        item['comm_num'] = "0"
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['env_num'] = '0'
        item['media_type'] = '网媒'
        item['addr_province'] = '全国'
        yield item
        # print(item)
