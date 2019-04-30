#coding=utf-8
import requests
import re
import json
import time

url = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=1&r=0.42959029000157156&callback=jQuery311009973329501517303_1524114298258&_=1524114298259'
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

r = requests.get(url,headers=headers)
ret = r.content.decode()
#新浪滚动新闻获得的json数据使用正则表达式去除非不规范的json字符
print(ret)
# res = re.match('^try{\w*?(.*)}catch\(e\){};$',ret).group(1)
res = re.match('^try{\w*\((.*)\);}catch\(e\){};$',ret).group(1)
print(res)
# res2 = re.match('^j\w*\((.*)\);$',res).group(1)
# print(res.group())
dict = json.loads(res)
# print(dict)
# print(dict_res)
content_list = dict['result']['data']
# print(content_list)
for content in content_list:
	item = {}
	item['time'] = time.ctime(int(content['ctime']))
	item['title'] = content['title']
	item['url'] = content['url']
	item['media'] = content['media_name']
	print(item)



