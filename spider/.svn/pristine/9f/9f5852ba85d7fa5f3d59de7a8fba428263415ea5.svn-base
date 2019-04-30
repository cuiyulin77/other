# coding=utf-8

from elasticsearch import Elasticsearch
import datetime
import importlib
import sys
importlib.reload(sys)


def get_urls(media_name):
    # es = Elasticsearch(hosts=['47.92.166.26'])
    es = Elasticsearch(hosts=['localhost'])
    # 查询结束时间
    this_day = datetime.date.today()
    tomorrow = this_day + datetime.timedelta(days=1)
    end_day = str(tomorrow) + 'T00:00:00'
    # 查询起始时间,即之前的时间
    start = this_day - datetime.timedelta(days=20)
    start_day = str(start) + 'T00:00:00'

    query_json = {
        "bool": {"must": [
            {"match": {
                "media": media_name
            }}
        ],
            "filter": {"range": {
                "publish_time": {
                    "gte": start_day,
                    "lt": end_day}
            }
            }
        }
    }

    # 获取总数["hits"]["total"]
    res = es.count(index="spider", doc_type='article', body={"query": query_json})
    res2 = es.search(index="spider", doc_type='article', body={"query": query_json, "size": res['count']})
    urls = []
    for i in res2['hits']['hits']:
        urls.append(i['_source']['url'])
    return urls

if __name__ == '__main__':
    l = get_urls('环球网')
    print(l)







