from selenium import webdriver


import requests

url = 'https://s.1688.com/youyuan/index.htm?tab=imageSearch&imageType=oss&imageAddress=cbuimgsearch/DHySC7ykD51556174744000.jpg'
res = requests.get(url)
print(res.content.decode('GBK'))