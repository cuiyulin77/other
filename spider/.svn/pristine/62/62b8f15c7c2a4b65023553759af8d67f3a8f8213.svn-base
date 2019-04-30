# coding = utf8
import hashlib

def get_md5(url):
    if isinstance(url,str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == '__main__':
    a = get_md5('http://blog.jobbole.com/114448/')
    print(a)
