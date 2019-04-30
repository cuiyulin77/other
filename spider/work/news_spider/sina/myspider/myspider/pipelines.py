# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging
logger = logging.getLogger(__name__)

class MyspiderPipeline(object):
    def process_item(self, item, spider):
        # logging.info(item)
        logger.info(item)

        # with open("itcast.txt","a") as f:
        #     f.write(json.dumps(item))
        # print(item)
        # item["hello"] = "******"
        return item

class MyspiderPipeline1(object):
    def process_item(self, item, spider):
        # print(item)
        return item