# coding=utf-8
# 这个是获取芝麻代理ip的小程序，通过requests.get 访API 接口，获取json数据，数据选型的时候勾选过期时间
# 。此api设定为每次获取任意个ip，ip存活时间为5-25分钟不等。放到redis中
# 启动blog爬虫之前，先启动此proxies.py 让redis的代理ip实时更新着
import requests
from time import sleep
import json
from redis import *
import time
import datetime


def get_ip():
    html_get = requests.get(
        'http://webapi.http.zhimacangku.com/getip?num=4&type=2&pro=&city=0&yys=0&port=1&pack=21479&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=')
    get_json = json.loads(html_get.content.decode())
    # print(type(get_json['success']))
    if get_json['success']:
        ip_list = get_json['data']
        # print(ip_list)
        return ip_list
    else:
        return


ip_list = get_ip()
# # 使用redis的db14 数据库
pool = ConnectionPool(host='127.0.0.1', port=6379, db=14)
r = StrictRedis(connection_pool=pool)
# 1.确定redis中的key,将ip地址放到redis里，key分别为ip*
# 获取地址数量
nums = len(ip_list)
# 生成key列表
ip_key_name = []
for i in range(nums):
    ip_key_name.append('ip'+str(i))

for i in range(nums):
    # ip从列表中拼接出ip地址
    ip = ip_list[i]['ip'] + ':' + str(ip_list[i]['port'])
    print(ip)
    #获取失效时间的时间戳
    ip_time = time.strptime(ip_list[i]['expire_time'], "%Y-%m-%d %H:%M:%S")
    ip_time = int(time.mktime(ip_time))
    now = int(time.time())
    ip_left = int(ip_time) - now
    # 2.设置ip的过期时间
    a = r.setex(ip_key_name[i], ip_left, ip)
    print(a)
# 3.查询
PROXIES = []
for key in ip_key_name:
    ip_str = r.get(key).decode()
    PROXIES.append(ip_str)
print(PROXIES)

# 3.不停的查看ip是否为空,就请求api再获得ip，存入redis中失效的建中。继续2-3的步骤
while True:
    for key in ip_key_name:
        if r.get(key) is None:
            print(key,'为空，即将补充ip地址')
            ip_get = get_ip()
            print(ip_get)
            if ip_get is not None:
                i = ip_key_name.index(key)
                ip = ip_get[i]['ip'] + ':' + str(ip_get[i]['port'])
                ip_time = time.strptime(ip_get[i]['expire_time'], "%Y-%m-%d %H:%M:%S")
                ip_time = int(time.mktime(ip_time))
                now = int(time.time())
                ip_left = int(ip_time) - now
                r.setex(key, ip_left, ip)
            else:
                sleep(5)
            get_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            print(get_time)
            PROXIES = []
            for ip_key in ip_key_name:
                ip_str = r.get(ip_key)
                if ip_str is not None:
                    ip_str = ip_str.decode()
                    PROXIES.append(ip_str)
            print(PROXIES)
