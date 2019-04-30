import datetime
from elasticsearch import Elasticsearch
def count_media():
    es = Elasticsearch(hosts=['127.0.0.1'])
    # 查询结束时间
    this_day = datetime.date.today()
    tomorrow = this_day + datetime.timedelta(days=1)
    end_day = str(tomorrow) + 'T00:00:00'
    print('end_day', end_day)
    # 查询起始时间
    start = this_day - datetime.timedelta(days=6)
    start_day = str(start) + 'T00:00:00'
    print('start_day', start_day)
    aggs = {
        "summary_terms": {
            "filter": {"range": {
                "create_time": {
                    "gte": start_day,
                    "lt": end_day
                }
            }}, "aggs": {
                "summary_count": {
                    "terms": {
                        "field": "addr_province",
                        "size": 100,
                        "order": {"_count": "desc"}
                    }
                }
            }
        }
    }
    res = es.search(index="spider", doc_type='article', body={"aggs": aggs, "size": 0})
    # buckets = res['aggregations']['summary_terms']['summary_count']['buckets']
    # print(buckets, this_day)
    # return buckets, this_day
count_media()