from aip import AipNlp
def baidu(key1,key2):
    APP_ID = '11678620'
    API_KEY = '3NutK9nnuIFNaHWo99DBFQPO'
    SECRET_KEY = 'wOEplSNzrgFyyjTrqHxPQA0kVPnNh7Lr'
    # 百度api链接
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    a = ['国际', '体育', '娱乐', '社会', '科技', '情感', '汽车', '教育', '时尚', '游戏', '军事', '旅游', '美食', '文化', '健康养生', '搞笑', '家居', '动漫',
         '宠物', '母婴育儿', '星座运势', '历史', '音乐', '综合']
    if key1 and key2:
        res = client.topic(key1,key2)
        classify = res['item']['lv1_tag_list'][0]['tag']
        if classify in a:
            print(True)
            return True
if __name__ == '__main__':
    key1 = '瓦房店政治'
    key2= '高的目标需要拿出更硬的举措，在全面落实《中央》意见基础上，《实施意见》紧密结合我省实际，在以下几方面进行了创新和细化。\n'
    print(baidu(key1,key1))

