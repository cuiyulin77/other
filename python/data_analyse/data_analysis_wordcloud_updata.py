# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import importlib
import sys
from elasticsearch_dsl import Search
import time
import pymysql
import datetime
from word_cloud.word_cloud import get_words_weight
import json

importlib.reload(sys)

es = Elasticsearch(hosts=['localhost'])

# company_popular_feelings添加了flag字段，默认为0，如果为1，则进行更新数据表，此脚本专门进行关键字更改之后的数据更新
# ======================================================================================================================
# 发现分析结果和舆情检测数据不符，检查后知道company_popular_feelings表中的'include1：部分匹配， include2：全部匹配',在查询的时候高反了，所以数据出错

# if filler == '{"include":"2"}'进行判断的时候，总是出错，使用json格式化{"include":"2"}，取include键的值2进行判断，
# 将遍历media_list进行es查询的方式,改为直接通过es的聚合查询,速度会更快,更直观和准确
# ======================================================================================================================

media_list = ['微信公众号','微博','百度贴吧','今日头条','新浪网', '中国新闻网', '澎湃', '新华网', '腾讯新闻', '北京青年报', '环球网', '中国证券报中证网', '中国经济网', '人民日报', '华商晨报', '经济日报', '中国地震局',
              '新京报', '央视经济', '国际金融报', '证券日报', '手机中国', '劳动报', '北京新浪乐居', '乐居财经', '中国网地产', '地产k线', 'BTV第一房产', '地产小蜜书',
              '新浪房产', '每日经济新闻', '云者云居', 'Test888', '北京日报', '中国经济时报', '钨丝科技', '房企情报站', '乐居', '山西新闻网-山西日报', 'None',
              '中新经纬', '央视', '新浪乐居', '喵眼看楼市', '中国经营报', '法制晚报', '21世纪经济报道', 'hot rain man', '工人日报', '中国房地产报', '华夏时报',
              '第一财经日报']

paper_news = ['人民日报', '华商晨报', '经济日报', '新京报', '国际金融报', '证券日报', '北京日报', '中国经济时报', '山西新闻网-山西日报', '中国经营报', '法制晚报', '工人日报',
              '中国房地产报', '华夏时报', '第一财经日报']

media_type = ['网媒', '报纸','微博','百度贴吧','微信公众号']

qinggan_list = ["中性","正面","敏感"]


def search_and_update(company_id, title_id, this_day, s_type, key_name, key_value):
    create_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    # print(key_name*20)
    try:
        # 通过hisdate,key_name,title_id查询对应数据的id
        cs1.execute("select id from analyse_count_number where hisdate =%s and key_name=%s and title_id = %s and summary_type=%s" ,
                    (this_day, key_name, title_id,s_type))
        result3 = cs1.fetchall()
        id = 0
        try:
            # print('id  test')
            id = result3[0]
        except Exception as e:
            print('此条数据id 不存在')
            # print(e)
        if s_type != 'wordcloud':
            print('in search_and_update函数中')
            print(id, "+" * 30, key_name, s_type)

        if id != 0:
            # print(id2)
            # 如果不等于0,更新行应id的res_num,create_time
            cs1.execute(
                "UPDATE analyse_count_number set key_value=%s,update_time=%s where id = %s",
                (key_value, create_time, str(id[0])))
            conn.commit()
        else:
            print("此id不存在，创建并插入数据" * 5)
            # 如果id=0，说明此id不存在，创建并插入数据
            cs1.execute(
                "INSERT INTO analyse_count_number (id,company_id,title_id,hisdate,summary_type,key_name,key_value,update_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                ('0', company_id, str(title_id), this_day, s_type, key_name, str(key_value), create_time))
            conn.commit()
    except Exception as e:
        print("search_and_update 函数运行中有错误")
        print(e)

def dateRange(beginDate, endDate):
    dates = []
    beginDate = str(beginDate)
    endDate = str(endDate)
    dt = datetime.datetime.strptime(str(beginDate), "%Y-%m-%d")
    date = str(beginDate)[:]
    print(date)
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates

def es_terms(key_list,this_today,tomorrow_day,summary_type):
    query = {
        "bool": {
            "must": [
                {"terms": {
                    "content": key_list
                }}
            ]
        }
    }

    aggs = {
        "summary_terms": {
            "filter": {"range": {
                "publish_time": {
                    "gte": this_today,
                    "lt": tomorrow_day
                }
            }}, "aggs": {
                "summary_count": {
                    "terms": {
                        "field": summary_type
                        , "size": 100,
                        "order": {"_count": "desc"}
                    }
                }
            }
        }
    }

    body = {"query": query, "aggs": aggs, "size": 0}
    return body

def es_must(key_list,this_today,tomorrow_day,summary_type):
    must_list = []
    for key in key_list:
        key_term = {"term": {"content": key}}
        must_list.append(key_term)

    query = {
        "bool": {
            "must": must_list
        }
    }

    aggs = {
        "summary_terms": {
            "filter": {"range": {
                "publish_time": {
                    "gte": this_today,
                    "lt": tomorrow_day
                }
            }}, "aggs": {
                "summary_count": {
                    "terms": {
                        "field": summary_type
                        , "size": 100,
                        "order": {"_count": "desc"}
                    }
                }
            }
        }
    }

    body = {"query": query, "aggs": aggs, "size": 0}
    return body

def data_analyse(this_day,this_today,tomorrow_day,cs1,id1,company_id,filler,es,paper_news,qinggan_list):

    # 通过关键词id获取关键词,添加is_del查询条件
    cs1.execute("SELECT title from company_keywords where popular_feelings_id=%s and is_del=0", id1)
    result2 = cs1.fetchall()
    # 提取关键词
    key_list = []
    for key in result2:
        key_list.append(key[0])
    # key_word = ' '.join(key_list)
    print(key_list, "1" * 10)

    # tomorrow_day = '2018-07-16' + 'T00:00:00'

    # 生成查询语句
    # {"include":"2"} 是全部匹配,使用must
    if filler == '2':
        print('filler 2')
        body = es_must(key_list, this_today, tomorrow_day, "media")
    else:
        print('filler 1')
        body = es_terms(key_list, this_today, tomorrow_day, "media")

    # 获取总数["hits"]["total"]
    res = es.search(index="spider", doc_type='article', body=body)
    # 获取统计列表
    buckets = res['aggregations']['summary_terms']['summary_count']['buckets']
    for buk in buckets:
        # 把数据插入到mysql中
        search_and_update(company_id, id1, this_day, "hotmedia", buk['key'], buk['doc_count'])

    # 插入完毕之后统计媒体信息
    cs1.execute(
        "select key_value,key_name from analyse_count_number where hisdate =%s  and title_id = %s and summary_type='hotmedia'",
        (str(this_day), id1))
    result4 = cs1.fetchall()
    # count_num = 0
    paper_news_num = 0  # 纸媒总数量
    inter_news_num = 0  # 网媒总数量
    weibo_num = 0
    weixin_num = 0
    tieba_num = 0
    for resp in result4:
        repose_num, media_message = resp
        # 如果media_message 在paper_news列表里，paper_news_num+repose_num
        if media_message in paper_news:
            paper_news_num += repose_num
            continue
        elif media_message in ['微博']:
            weibo_num = repose_num
            continue
        elif media_message in ['百度贴吧']:
            tieba_num = repose_num
            continue
        elif media_message in ['微信公众号']:
            weixin_num = repose_num
            continue
        else:
            inter_news_num += repose_num
    #     count_num += repose_num
    # if count_num!=(paper_news_num+inter_news_num+weibo_num+weixin_num+tieba_num):
    #     print("*"*100)
    #     print("数据异常,异常title",id1,key_list)
    #     print("*" * 100)

    # print(paper_news_num, "paper_news_num")
    # print(inter_news_num, 'inter_news_num')
    search_and_update(company_id, id1, this_day, "meiti", '报纸', paper_news_num)
    search_and_update(company_id, id1, this_day, "meiti", '微博', weibo_num)
    search_and_update(company_id, id1, this_day, "meiti", '百度贴吧', tieba_num)
    search_and_update(company_id, id1, this_day, "meiti", '微信公众号', weixin_num)
    search_and_update(company_id, id1, this_day, "meiti", '网媒', inter_news_num)

    """进行
    """
    # 生成情感查询语句
    if filler == '2':
        body = es_must(key_list, this_today, tomorrow_day, "qinggan",)
    else:
        body = es_terms(key_list, this_today, tomorrow_day, "qinggan",)
    # 获取总数["hits"]["total"]
    res = es.search(index="spider", doc_type='article', body=body)
    buckets = res['aggregations']['summary_terms']['summary_count']['buckets']

    # 以下代码是为了是结果中没有某个情感类型的值设置为0
    dic_qinggan = [{'key': 0, 'doc_count': 0}, {'key': 1, 'doc_count': 0}, {'key': 2, 'doc_count': 0}]
    # 更新dic_qinggan数据
    for buk in buckets:
        dic_qinggan[buk['key']]['doc_count'] = buk['doc_count']
    for dic in dic_qinggan:
        # print(res_num,id1,company_id,media)
        search_and_update(company_id, id1, this_day, "qinggan", qinggan_list[dic['key']], dic['doc_count'])

    word_list = get_words_weight(this_today, tomorrow_day, es, key_list,filler)
    for v, n in word_list:
        search_and_update(company_id, id1, this_day, "wordcloud", v, str(int(n * 10000)))
#  =====================================================================================================================

while True:
    # 连接云服务器mysql
    # conn = pymysql.connect(host='47.92.77.18', port=3306, user='root', database='xuanyuqing', password='root7718',
    conn = pymysql.connect(host='47.92.166.26', port=3306, user='root', database='xuanyuqing', password='admin8152',
                           charset='utf8')
    cs1 = conn.cursor()
    print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    print("现在开始数据提取")

    cs1.execute('select  id,company_id,fillter from company_popular_feelings where is_del=0 and flag=1')
    # 获取查询的结果关键词id,公司id,和更新时间
    result1 = cs1.fetchall()
    print(type(result1))
    print(result1)
    if result1:
        # print("2"*10)
        for res in result1:
            # 获取查询的结果关键词id,公司id,和更新时间
            try:
                id1, company_id, filler = res
                filler = json.loads(filler)
                # print(filler, 1)
                filler = filler['include']
                # print(filler, 2)
                # print(type(filler))
                print("補全* *"*10)
                today = datetime.date.today()
                before_week = today - datetime.timedelta(days=30)
                day_list = dateRange(before_week,today)
                for day in day_list:
                    this_day = datetime.datetime.strptime(day,"%Y-%m-%d")
                    # 转换为elasticsearch可以识别的带T的时间格式
                    this_today = str(this_day).replace(" ",'T')     # + 'T00:00:00'
                    print(this_today)
                    # this_today = '2018-07-05' + 'T00:00:00'
                    # 查询结束时间
                    tomorrow = this_day + datetime.timedelta(days=1)
                    # 转换为elasticsearch可以识别的带T的时间格式
                    tomorrow_day = str(tomorrow).replace(" ",'T')    #  + 'T00:00:00'
                    data_analyse(this_day, this_today, tomorrow_day, cs1, id1, company_id, filler, es, paper_news,
                                 qinggan_list)
                try:
                    cs1.execute(
                        "UPDATE company_popular_feelings set flag=%s where id = %s",
                        ('0', id1))
                    conn.commit()
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)

    conn.close()
    print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    print("开始休眠")
    time.sleep(60)

