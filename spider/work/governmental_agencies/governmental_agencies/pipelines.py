# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class GovernmentalAgenciesPipeline(object):
    def process_item(self, item, spider):
        print('进入管道')
        db = pymysql.connect("localhost", "root", "cyl494658565", "mysql")
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO institutional_units (id, organizations_name, province,city,county,town,url,update_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",('0',item['organizations_name'],item['province'],item['city'],item['county'],item['town'],item['url'],item['update_time']))
            db.commit()
            data = cursor.fetchall()
            print('存入数据', data)
        except Exception as e:
            print('数据存入错误:%s'%e)
        db.close()

# CREATE TABLE `institutional_units` (
#   `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
#   `organizations_name` varchar(200) DEFAULT NULL COMMENT '机构名字',
#   `province` varchar(50) DEFAULT NULL COMMENT '省',
#   `city` varchar(50) DEFAULT NULL COMMENT '地级市',
#   `county` varchar(50) DEFAULT NULL COMMENT '区或县同级单位',
#   `town` varchar(50) DEFAULT NULL COMMENT '街道或镇等同级单位',
#   `url` varchar(50) DEFAULT NULL COMMENT '政府单位网址',
#   `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


