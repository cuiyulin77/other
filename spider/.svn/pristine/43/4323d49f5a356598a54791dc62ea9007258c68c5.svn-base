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
print(c)
print(b)

# db = pymysql.connect("localhost", "root", "cyl494658565", "cui")
# cursor = db.cursor()
# cursor.execute('SELECT * FROM province_city_county WHERE name LIKE \'{}%\''.format(key))
# data = cursor.fetchall()
# # print(data, i)
# id = data[0][3]
# if stu == 'e':
#      if id == 3:
#           addr_county = data[0][1]
#           print(addr_county, '444444444444444444444444444')
#           cursor.execute('SELECT name,pid FROM province_city_county where id={}'.format(data[0][2]))
#           data1 = cursor.fetchall()
#           print(data1, '33333333333333333333333333333333333333333333333333333')
#           addr_city = data1[0][0]
#           addr_province_id = data1[0][1]
#           cursor.execute('SELECT name FROM province_city_county where id={}'.format(addr_province_id))
#           data2 = cursor.fetchall()
#           addr_province = data2[0][0]
#           print(addr_province, addr_city, addr_county)
#           return addr_province, addr_city, addr_county
#      elif id == 1:
#           m = data[0][1]
#           if '市' in m:
#                addr_province = data[0][1]
#                addr_county = None
#                addr_city = data[0][1]
#           else:
#                addr_province = data[0][1]
#                addr_county = None
#                addr_city = None
#           print(addr_province, addr_city, addr_county)
#           return addr_province, addr_city, addr_county
#      else:
#           addr_city = data[0][1]
#           addr_county = None
#           cursor.execute('SELECT name,pid FROM province_city_county where id={}'.format(data[0][2]))
#           data1 = cursor.fetchall()
#           print(data1, '22222222222222222222222')
#           addr_province = data1[0][0]
#           print(addr_province, addr_city, addr_county)
#           return addr_province, addr_city, addr_county
# if stu == 'f':
#      addr_county = data[0][1]
#      print(addr_county, '444444444444444444444444444')
#      cursor.execute('SELECT name,pid FROM province_city_county where id={}'.format(data[0][2]))
#      data1 = cursor.fetchall()
#      print(data1, '33333333333333333333333333333333333333333333333333333')
#      addr_city = data1[0][0]
#      addr_province_id = data1[0][1]
#      cursor.execute('SELECT name FROM province_city_county where id={}'.format(addr_province_id))
#      data2 = cursor.fetchall()
#      addr_city = data2[0][0]
#      addr_province = addr_city
#      print(addr_province, addr_city, addr_county)
# db.close()




