# coding=utf-8

import requests
import re
import json
import time
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}
# url_start = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=1&r=0.05740046813150901&callback=jQuery31106890680659763975_1524041524795&_=1524041524796'
url_list = []
#获取滚动新闻的url,页码暂定500页
for i in range(500):
    url = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page={}&r=0.014799634874140155&callback=jQuery31109703260530620725_1524042804995&_=1524042804996'.format(i)
    url_list.append(url)
for url in url_list:
    print('&'*30,url_list.index(url),'&'*30)
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
        # 将获取到的ctime转化为年月日格式的时间格式
        item['time'] = time.ctime(int(content['ctime']))
        # 获取新闻标题
        item['title'] = content['title']
        # 获取新闻的url
        item['url'] = content['url']
        # 获取新闻来自那个媒体
        item['media'] = content['media_name']
        print(item)

    





