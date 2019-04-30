# coding=utf8
import jieba
import pandas as pd
from elasticsearch import Elasticsearch
import datetime
import jieba.analyse as ana
import os

def get_words_weight(this_today, tomorrow_day, es, key_list,filler):

    # 注意是filler,不是filter.filter是内置变量名
    if filler == '2':
        must_list = []
        for key in key_list:
            key_term = {"term": {"content": key}}
            must_list.append(key_term)

        query_json = {
            "bool": {
                "must": must_list, "filter": [{"range": {"publish_time": {
                    "gte": this_today,
                    "lt": tomorrow_day}}}]
            }
        }
    else:
        query_json = {
            "bool": {
                "must": [
                    {"terms": {
                        "content": key_list
                    }}
                ], "filter": [{"range": {"publish_time": {
                    "gte": this_today,
                    "lt": tomorrow_day}}}]
            }
        }

    res = es.search(index="spider", doc_type='article', body={"query": query_json, "size": 0})
    res_num = res["hits"]["total"]
    print('文章数量',res_num)
    txts = es.search(index='spider', doc_type='article', body={'query': query_json, 'size': res_num})
    hits = txts['hits']['hits']
    contents = []
    for hit in hits:
        # print(hit['_source']['content'],'\n')
        contents.append(hit['_source']['content'])
    # print(''.join(contents))

    words_str = ''.join(contents).replace("\n", '').replace(" ", '')

    txt_path = os.path.dirname(os.path.abspath(__file__))+'/停用词.txt'
    ana.set_stop_words(txt_path)
    words_list = ana.extract_tags(words_str, topK=20, withWeight=True)
    # print(len(words_list))
    print(words_list)

    return words_list

if __name__ == '__main__':
    txt_path = os.path.dirname(os.path.abspath(__file__))+'/停用词.txt'
    print(txt_path)


