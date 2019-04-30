# coding=utf-8
import pymysql
import requests
import re
import json
import time
import hashlib
from lxml import etree

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}
# url_start = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=1&r=0.05740046813150901&callback=jQuery31106890680659763975_1524041524795&_=1524041524796'





url_list = []
#获取滚动新闻的url,页码暂定500页
for i in range(3000):
    url = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page={}&r=0.014799634874140155&callback=jQuery31109703260530620725_1524042804995&_=1524042804996'.format(i)
    url_list.append(url)
for url in url_list:
    # print('&'*30,url_list.index(url),'&'*30)
    response = requests.get(url,headers=headers)
    ret = response.content.decode()
    # 新浪滚动新闻获得的json数据使用正则表达式去除非不规范的json字符
    # print(ret)
    # res = re.match('^try{\w*?(.*)}catch\(e\){};$',ret).group(1)
    res = re.match('^try{\w*\((.*)\);}catch\(e\){};$', ret).group(1)
    # print(res)
    # 将json转化为字典形式
    dict = json.loads(res)
    content_list = dict['result']['data']
    for content in content_list:
        item = {}
        # 获取新闻标题
        item['title'] = content['title']
        # 获取新闻的url
        item['url'] = content['url']
        item['time'] = int(content['ctime'])
        response_detail = requests.get(content['url'], headers=headers)
        html_str = etree.HTML(response_detail.content)
        item['content'] = html_str.xpath("//div[@id='article']/p/text()")
        if len(item['content']) == 0:
            item['content'] = html_str.xpath("//div[@id='artibody']/p/span/text()")
        if len(item['content']) == 0:
            item['content'] = html_str.xpath("//div[@id='artibody']/p/text()")
        # 获取新闻来自那个媒体
        item['media'] = content['media_name']
        # print(item['content'], item['url'])
        title = str(item['title'])
        # keywords = str(item['keywords'][0])
        content = item['content']
        content = str(content).replace('\n', '').replace(" ","")
        print(item)
        try:
            conn = pymysql.connect(host="127.0.0.1", user="root", passwd="mysql", db="news_spider", charset='utf8')
            cursor = conn.cursor()

            url = str(item['url'])
            time = str(item['time'])
            media = str(item['media'])
            m = hashlib.md5()
            m.update(str(url).encode('utf8'))
            article_id = str(m.hexdigest())
            flag = cursor.execute(
                'INSERT INTO article (article_id,title,content,url,media,publish_time) VALUES (%s,%s,%s,%s,%s,%s)',
                (article_id, title,  content, url, media, time))
            conn.commit()
            if flag == 1:
                print('文章---' + title + '保存成功！')
                print(str(article_id) + '-----' + str(time))
            else:
                print('文章---' + title + '保存失败！')
        except Exception as e:
            print(e)

        finally:
            # 关闭Connection对象
            conn.close()




