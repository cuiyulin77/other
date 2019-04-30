#-*- coding:utf-8 -*-
import requests
from lxml import etree
import re
import pymysql

str = ''
c= []
b =[]
db = pymysql.connect("localhost", "root", "cyl494658565", "cui")
cursor = db.cursor()
cursor.execute('select name from province_city_county ')
data = cursor.fetchall()
print(data)
for i in data:
    i = i[0]
    print(i,'我是原来字符串')
    if '市辖区' not in i:
        if  '市' in i:
            str = i.split('市')[0]
            print(str,'22222222222222222222222')
        elif '区' in i:
            if len(i) != 2:
                if '开发' in i:
                    str = i
                elif '经济'in i:
                    str = i
                elif '园区'in i:
                    str = i
                elif '矿区'in i:
                    str = i
                elif '示范区'in i:
                    str = i
                else:
                    str = i.split('区')[0]
            else:
                str = i
            print(str, '22222222222222222222222')
        elif '县' in i:
            if len(i)!=2:
                if '自治县' in i:
                    str = i.split('自治县')[0]
                else:
                    str = i.split('县')[0]
                print(str,'4444444444444444444444')
            else:
                str = i
        if str:
            a = {i: str}
            c.append(a)
            b.append(str)
db.close()
print(b)
print(c)


# data =[]
# data1 =[]
# text1 = ''
# for i in res:
#     text = i.xpath('./*//@data-src')
#     # print(len(text),text)
#     if len(text)==0:
#         text1 = i.xpath('string(.)')
#         print(text1,'222222222222')
#     elif len(text)==1:
#         text1 = i.xpath('string(.)')+text[0]
#         print(text1,'111111111111111')
#     elif len(text)==3 or len(text)==2 or len(text)==4 or len(text)==5:
#         text2 = ''
#         for node in range(0,len(text)):
#             print(node)
#             text2 += text[node]+'\n'
#         text1 = text2+i.xpath('string(.)').strip()
#         print(text1,'333333333333333333333333333333')

    # print(text)
    # if text is None:
    #     text1 = i.xpath('string(.)')
    #     print(text1,'111111111111111')
    # else:
    #     print(i,text)
        # text1 = i.xpath('string(.)').extract()+text

    # print(text1)
    # if len(text) != 1:
    #     for i in text:
    #         node =text.xpath('./section')




