# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
import hashlib
from somenew.items import SomenewItem


class DizhenjuSpider(scrapy.Spider):
    name = 'dizhenju'
    allowed_domains = ['cea.gov.cn']
    start_urls = ['http://www.cea.gov.cn/publish/dizhenj/464/478/index.html',
                  'http://www.cea.gov.cn/publish/dizhenj/464/102620/index.html',
                  'http://www.cea.gov.cn/publish/dizhenj/464/495/index.html',
                  'http://www.cea.gov.cn/publish/dizhenj/464/102140/index.html',
                  'http://www.cea.gov.cn/publish/dizhenj/464/522/index.html',
                  'http://www.cea.gov.cn/publish/dizhenj/464/515/index.html',
                  'http://www.cea.gov.cn/publish/dizhenj/464/756/index.html',
                  'http://www.cea.gov.cn/publish/dizhenj/464/479/index.html',
                  'http://www.cea.gov.cn/publish/dizhenj/467/490/index.html']

    def parse(self, response):
        href_list = response.xpath("//div[@class='list_main_right_conbg_con']/ul/li/a/@href").extract()
        for href in href_list:
            url = response.urljoin(href)  # response.urljoin(url)
            yield scrapy.Request(url, callback=self.get_content)
        next_href = response.xpath("//span[@class='page_left']/a[text()='下一页']/@href").extract_first()
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
        item['title'] = response.xpath("//div[@class='detail_main_right_conbg_tit']/div[1]/text()").extract_first()
        time_text = response.xpath("//div[@class='detail_main_right_conbg_tit']/div[3]/text()").extract_first()
        item['time'] = re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", time_text)
        item['media'] = '中国地震局'
        item['content'] = response.xpath("//div[@class='detail_main_right_conbg_con']/div/p").extract()
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        yield item