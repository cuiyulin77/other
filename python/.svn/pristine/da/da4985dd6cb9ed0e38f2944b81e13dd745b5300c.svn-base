# coding=utf-8
# 这个是获取蘑菇代理ip的小程序，通过requests.get 访API 接口，获取json数据，数据选型的时候勾选过期时间
# 。此api设定为每次获取任意个ip，ip存活时间为1-5分钟不等。放到redis中
# 启动blog爬虫之前，先启动此proxies.py 让redis的代理ip实时更新着
import requests
from time import sleep
import json
from redis import *
import time
import datetime
# from other_process.python_send_emil import let_send

pool = ConnectionPool(host='127.0.0.1', port=6379, db=14)
r = StrictRedis(connection_pool=pool)
ip_key_name = ['ip0','ip1']

def get_ip():
    # 一次提取1个
    html_get = requests.get(
        'http://mvip.piping.mogumiao.com/proxy/api/get_ip_bs?appKey=d6832a14e5024cc0b9384c53fdae32c3&count=1&expiryDate=0&format=1&newLine=2')
    get_json = json.loads(html_get.content.decode())
    # print(type(get_json['success']))
    if get_json['msg']:
        ip_list = get_json['msg']
        # print(ip_list)
        return ip_list
    else:
        return

# 3.每50s更换一次ip
while True:
    try:
        PROXIES = []
        get_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        print(get_time)
        ip_list = get_ip()
        # # 使用redis的db14 数据库
        # 1.确定redis中的key,将ip地址放到redis里，key分别为ip*
        # ip从列表中拼接出ip地址
        ip = ip_list[0]['ip'] + ':' + str(ip_list[0]['port'])
        print(ip)
        a = r.set(ip_key_name[0], ip)
        print(a)
        # 3.查询
        ip_str = r.get('ip0').decode()
        print(ip_str)
        sleep(50)
    except Exception as e:
        print(e)
        sleep(2)
