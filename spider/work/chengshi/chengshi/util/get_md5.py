import hashlib
import os ,requests
def get_md(str):
    md = hashlib.md5()#构造一个md5
    md.update(str.encode())
    res = md.hexdigest()
    print(res)
    return res


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
        f.close()


if __name__ == '__main__':
    str = 'http://www.chinacity.org.cn/csfz/csxw/382587.html'
    get_md(str)