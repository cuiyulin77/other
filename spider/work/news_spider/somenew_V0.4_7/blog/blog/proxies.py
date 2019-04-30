# coding=utf-8
# 这个是获取芝麻代理ip的小程序，通过requests.get 访API 接口，获取json数据。此api设定为每次获取2个ip，ip存活时间为5-25分钟不等。后期可以放到redis中
# 启动blog爬虫之前哎俺，先启动此proxies.py 让redis的代理ip实时更新着
import requests
from time import sleep
import json
from redis import *
import time


def get_ip():
    html_get = requests.get(
        'http://webapi.http.zhimacangku.com/getip?num=2&type=2&pro=&city=0&yys=0&port=1&pack=21479&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=')
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
# 1.将ip地址放到redis里，key分别为ip1，ip2
ip1 = ip_list[0]['ip'] + ':' + str(ip_list[0]['port'])
ip2 = ip_list[1]['ip'] + ':' + str(ip_list[1]['port'])
# ip1_time = ip_list[0]['expire_time']
# 获取失效时间的时间戳
ip1_time = time.strptime(ip_list[0]['expire_time'], "%Y-%m-%d %H:%M:%S")
ip2_time = time.strptime(ip_list[1]['expire_time'], "%Y-%m-%d %H:%M:%S")
ip1_time = int(time.mktime(ip1_time))
ip2_time = int(time.mktime(ip2_time))
# print(ip1_time)
# 获取现在的时间戳
now = int(time.time())
# 获取剩余时间
ip1_left = int(ip1_time) - now
ip2_left = int(ip2_time) - now

# 2.设置ip1,ip2的过期时间
r.setex('ip1', ip1_left, ip1)
r.setex('ip2', ip2_left, ip2)
# a = r.keys('*')
# print(a)
ip1_str = r.get('ip1').decode()
ip2_str = r.get('ip2').decode()
PROXIES = [ip1_str, ip2_str]
print(PROXIES)

# 3.不停的查看ip是否为空,就请求api再获得ip，存入redis中失效的建中。继续2-3的步骤
# print(r.get('ip1')) # 如果为空，返回结果为none
while True:
    # print(2)
    if (r.get('ip1')==None) or (r.get('ip2') == None):
        # print(r.get('ip1'),r.get('ip2'))
        # print(r.get('ip3'))
        # 如果ip1空，获取ip，填入ip1位置
        if r.get('ip1') is None:
            print('ip1')
            ip1_get = get_ip()
            print(ip1_get)
            if ip1_get is not None:
                ip1 = ip1_get[0]['ip'] + ':' + str(ip1_get[0]['port'])
                ip1_time = time.strptime(ip1_get[0]['expire_time'], "%Y-%m-%d %H:%M:%S")
                ip1_time = int(time.mktime(ip1_time))
                now = int(time.time())
                ip1_left = int(ip1_time) - now
                r.setex('ip1', ip1_left, ip1)
        if r.get('ip2') is None:
            print('ip2')
            ip2_get = get_ip()
            print(ip2_get)
            if ip2_get is not None:
                ip2 = ip2_get[1]['ip'] + ':' + str(ip2_get[1]['port'])
                ip2_time = time.strptime(ip2_get[1]['expire_time'], "%Y-%m-%d %H:%M:%S")
                ip2_time = int(time.mktime(ip2_time))
                now = int(time.time())
                ip2_left = int(ip2_time) - now
                r.setex('ip2', ip2_left, ip2)
                # PROXIES[1] = r.get('ip2').decode()
        # 打印更新后的ip地址
        ip1_str = r.get('ip1').decode()
        ip2_str = r.get('ip2').decode()
        PROXIES = [ip1_str, ip2_str]
        print(PROXIES)


