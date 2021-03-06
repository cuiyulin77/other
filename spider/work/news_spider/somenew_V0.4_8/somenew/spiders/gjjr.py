# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
import hashlib
from somenew.items import SomenewItem

# 人民网旗下国际金融报爬虫http://www.ifnews.com/
class GjjrSpider(scrapy.Spider):
    name = 'gjjr'
    allowed_domains = ['ifnews.com']
    start_urls = ['http://ifnews.com/']

    def parse(self, response):
        url_list = response.xpath("//div[@class='left']/div/dl/a/@href").extract()
        for url in url_list:
            yield scrapy.Request(url,callback=self.get_content)
        next_url = response.xpath("//span[@class='down']/a/@href").extract_first()
        next_page_num = int(re.match(r'.*?(\d+$)',next_url).group(1))
        if next_page_num <= 10:
            yield scrapy.Request(next_url,callback=self.parse)

    def get_content(self,response):
        item = SomenewItem()
        src_url = response.xpath("//meta[@name='wx:image']/@content").extract_first()
        date = re.match(r".*?\/(\d+)\/.*",src_url).group(1)[:4]
        item['title'] = response.xpath("//h2/text()").extract_first()
        item['media'] = '国际金融报'
        item['url'] = response.url
        time_node = response.xpath("//h2/span/i/em/text()").extract_first()
        day_node = response.xpath("//h2/span/i/text()").extract_first()
        item['time'] = str(date)+'-'+str(day_node)+' '+str(time_node)
        item['content'] = response.xpath("//div[@class='left bgf']/p//text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        # content = response.xpath("//div[@class='left bgf']").extract()
        # item['content'] = content[0].xpath('string(.)').extract()[0].replace('\n', '').replace('\t', ' ')
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
        yield item