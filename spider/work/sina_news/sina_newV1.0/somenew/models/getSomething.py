# -*- coding: utf-8 -*-
# 今日头条
#原本为获得as, cp, sin三个加密参数使用，后使用搜索功能不再需要

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import time
import json
import requests
from urllib.parse import urlencode


def getUrls(page, keyWord):
    url = 'https://www.toutiao.com/api/search/content/'
    returnUrls = []
    for num in range(page):
        data = {'offset': str(num * 20), 'format': 'json', 'keyword': keyWord, 'autoload': 'true', 'count': '20',
                'cur_tab': '1', 'from': 'search_tab'}
        returnUrls.append(url + '?' + urlencode(data))
    return returnUrls




#下面为之前的函数，不用的
# def getUrl():
#     dic = getKey()
#     hot_time = int(time.time())
#     url = 'https://www.toutiao.com/api/pc/feed/?min_behot_time=0&category=__all__&utm_source=toutiao&widen=1&tadrequire=true&as='+str(dic['as'])+'&cp='+str(dic['cp'])+'&_signature='+str(dic['sin'])
#     # url = "https://www.toutiao.com/api/pc/feed/?category=news_tech&" \
#     #       "utm_source=toutiao&widen=1&max_behot_time="+str(hot_time)+"&max_behot_time_tmp="+str(hot_time)+"&" \
#     #       "tadrequire=true&as="+str(dic['as'])+"&cp="+str(dic['cp'])+"1&_signature="+str(dic['sin'])
#     # with open('filee.txt', 'wb') as f:
#     #     f.write(bytes(url, encoding='utf-8'))
#     print(url)
#     return url
#
# def getKey():
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     web = webdriver.Chrome(chrome_options=chrome_options)
#     # web = webdriver.Chrome()
#     web.get('https://www.toutiao.com/ch/news_game/')
#     ascp = web.execute_script('return ascp.getHoney()')
#     strSin = web.execute_script('return TAC.sign(0)')
#     web.quit()
#     strAs = ascp['as']
#     strCp = ascp['cp']
#     dic = {'as': strAs, 'cp': strCp, 'sin': strSin}
#     print(dic)
#     return dic

if __name__ == '__main__':
    getUrl()

