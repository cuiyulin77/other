# coding=utf-8

import hashlib
import requests
import os
import datetime
from PIL import Image
import time

def get_md5(url):
    if isinstance(url,str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

def down_pic(url,path,pic_name):
    # http://www.theping.cn/d/file/xinshidai/wenhua/guoxue/2019-01-11/e7e8a9624c4ab2e93341c9653725e167.jpg
    # E:\theping_local_server\d\file\yangsheng\2019-01-11\e7e8a9624c4ab2e93341c9653725e167.jpg
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    }
    response = requests.get(url,headers=headers)
    # 先判断路径是否存在
    isExists = os.path.exists(path)
    if isExists is not True:
        # 如果文件夹不存在,就创建文件夹
        os.makedirs(path)
    # 获取的文本实际上是图片的二进制文本
    img = response.content
    path_name = path + pic_name
    # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
    with open(path_name, 'wb') as f:
        f.write(img)
        time.sleep(0.01)
        # 以下是直接把图片保存为特定大小的方式,
        im = Image.open(path_name)
        (x, y) = im.size  # read image size
        x_s = 600  # define standard width
        y_s = int(y * x_s / x)  # calc height based on standard width
        out = im.resize((x_s, y_s), Image.ANTIALIAS)  # resize image with high-quality
        out.save(path_name)

if __name__ == '__main__':
    # print(get_md5('http://blog.jobbole.com/114473/'))
    url = 'http://www.ttys5.com/d/file/zhongyi/liangxing/2016-10-27/ec8445365ba1fe9f47e1ae4156aa8924.jpg'
    path = r'E:\\theping_local_server\\d\\file\\yangsheng\\'
    pic_name = 'e7e8a9624c4ab2e93341c9653725e167.jpg'
    down_pic(url,path,pic_name)

