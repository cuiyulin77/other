# -*- coding=UTF-8 -*-

# =======================================================
# 自动生成分析报告
# ========================================================
import matplotlib.pyplot as plt
import matplotlib
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import pymysql
import pandas as pd
import re
import time
import os
from operator import itemgetter, attrgetter

# 设置显示中文
plt.rcParams['font.family'] = ['Arial Unicode MS', 'sans-serif']
# matplotlib.rcParams['axes.unicode_minus'] = False    # 解决保存图像是负号'-'显示为方块的问题
while True:
    connect = pymysql.connect(
        host='47.92.166.26',
        db='xuanyuqing',
        user='root',
        password='admin8152',
        port=3306,
        charset='utf8'
    )
    cursor = connect.cursor()
    # print(cursor)
    # =========================================================================
    # 获取生成报告的相关信息
    cursor.execute('select id,company_id,from_date,end_date from gen_report where flag=1')
    report_msg = cursor.fetchall()
    print(report_msg)
    if report_msg:
        for msg in report_msg:
            id, company_id, from_date, end_date = msg

            doc = Document()
            doc_title = doc.add_heading("舆情分析报告", level=0)
            doc_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # =========================================================================
            # 监测数据汇总
            # 后期监测周期的时间设为变量
            # print('cursor',cursor)
            cursor.execute(
                "SELECT key_name,sum(key_value) AS counts FROM  analyse_count_number where company_id=%s and hisdate>=%s and hisdate<=%s and summary_type='meiti' GROUP BY key_name",
                (company_id, from_date, end_date))
            # time.sleep(1)
            meiti_count_list = cursor.fetchall()
            print('meiti_count_list', meiti_count_list)
            meiti_name_count_list = []
            meiti_value_count_list = []
            for meiti in meiti_count_list:
                meiti_name_count_list.append(meiti[0])
                meiti_value_count_list.append(meiti[1])

            #  监测情感数据汇总
            cursor.execute(
                "SELECT key_name,sum(key_value) AS counts FROM  analyse_count_number where company_id=%s and hisdate>=%s and hisdate<=%s and summary_type='qinggan' GROUP BY key_name",
                (company_id, from_date, end_date))
            qinggan_count_list = cursor.fetchall()
            print(qinggan_count_list, 'qinggan_count_list')
            qinggan_all = 0
            qinggan_count_names = []
            qinggan_count_values = []
            for qinggan in qinggan_count_list:
                print(qinggan[0], qinggan[1])
                qinggan_count_names.append(qinggan[0])
                qinggan_count_values.append(qinggan[1])
                qinggan_all += int(qinggan[1])
            print('qinggan_count_names', qinggan_count_names)
            print('qinggan_count_values', qinggan_count_values)
            paragraph1 = doc.add_paragraph()
            paragraph1.add_run('监测周期：{from_date} - {end_date}\n'.format(from_date=from_date, end_date=end_date)).bold = True
            paragraph1.add_run('监测范围：').bold = True
            paragraph1.add_run('新闻、微博、传统纸媒、贴吧、微信公众号、等全网络监测\n')
            paragraph1.add_run('舆情综述：').bold = True
            paragraph1.add_run(
                '针对全网信息进行监测，共抓取信息{all}条，正面信息{zhengmian}条，中性信息{zhongxing}条，敏感信息{mingan}条\n'.format(all=qinggan_all, zhengmian=
                qinggan_count_values[qinggan_count_names.index('正面')], zhongxing=qinggan_count_values[
                    qinggan_count_names.index('中性')], mingan=qinggan_count_values[qinggan_count_names.index('敏感')]))
            paragraph1.add_run('舆情概况：').bold = True
            paragraph1.add_run('监测周期内，网媒{wangmei}条，微信公众号{weixin}条，传统纸媒{paper}条，微博{weibo}条，贴吧{tieba}条。\n'.format(
                wangmei=meiti_value_count_list[meiti_name_count_list.index('网媒')],
                weixin=meiti_value_count_list[meiti_name_count_list.index('微信公众号')],
                paper=meiti_value_count_list[meiti_name_count_list.index('报纸')],
                weibo=meiti_value_count_list[meiti_name_count_list.index('微博')],
                tieba=meiti_value_count_list[meiti_name_count_list.index('百度贴吧')]))

            cursor.execute("select id,title from company_popular_feelings where company_id={company_id} and is_del=0".format(
                company_id=company_id))
            ti_list = cursor.fetchall()

            # 文件路径
            file_name = "E:\phpStudy\PHPTutorial\WWW\www.yuqing.cn\public\web\\analyse"
            end_date_str = re.match('\d{4}-\d{2}', str(end_date))
            file_name = file_name + str('\\') + end_date_str.group()
            isExists = os.path.exists(file_name)
            if isExists is not True:
                # 如果文件夹不存在
                os.makedirs(file_name)
            for ti in ti_list:
                title_id, title_name = ti
                print(title_id, title_name)
                # print()
                # 先获取title_name 的情感
                cursor.execute(
                    "SELECT  key_name,sum(key_value) AS counts FROM  analyse_count_number where title_id=%s and hisdate>=%s and hisdate<=%s and summary_type='qinggan' GROUP BY key_name",
                    (title_id, from_date, end_date))
                qingan_list = cursor.fetchall()
                qinggan_count = 0
                qinggan_names = []
                qinggan_values = []
                for qinggan in qingan_list:
                    print(qinggan[0], qinggan[1])
                    qinggan_names.append(qinggan[0])
                    qinggan_values.append(qinggan[1])
                    qinggan_count += int(qinggan[1])
                print("qinggan_names", qinggan_names)
                print("qinggan_values", qinggan_values)
                # 生成情感环形图
                plt.pie(qinggan_values,
                        labels=qinggan_names,  # 每个扇形的名字，和percent对应
                        autopct='%1.1f%%',  # 百分比的小数点方式到1个小数点
                        shadow=False,  # 阴影
                        wedgeprops=dict(width=0.5, edgecolor='w'),  # 生成环形饼图，width=0.5是环形的宽度为0.5
                        )
                plt.axis('equal')  # 正圆
                print(2)
                # 此处保存位置后期需要变化，文件名也需要变化

                file_name_png = file_name + str('\\') + '123.png'

                plt.savefig(file_name_png, dpi=120, )  # 保存为123456.png， 保存之后如果要使用，需要等待一段时间才能保存完毕，大概时间是5秒。dpi=120图片大小刚好适合
                # plt.show()
                plt.close()
                print(file_name_png)

                paragraph = doc.add_paragraph()
                paragraph.add_run('{}监测相关信息\n'.format(title_name)).bold = True

                paragraph.add_run('1.情感分析：\n').bold = True
                paragraph.add_run('监测期内，正面信息{zhengmian}条，中立信息{zhongxing}条，敏感信息{mingan}条\n'.format(qinggan_count=qinggan_count,
                                                                                                  zhengmian=qinggan_values[
                                                                                                      qinggan_names.index(
                                                                                                          '正面')],
                                                                                                  zhongxing=qinggan_values[
                                                                                                      qinggan_names.index(
                                                                                                          '中性')],
                                                                                                  mingan=qinggan_values[
                                                                                                      qinggan_names.index(
                                                                                                          '敏感')]))
                # 只有总数不为0,才进行图片插入,否则没有意义,是一张空白图片
                if qinggan_count != 0:
                    pic1 = doc.add_picture(file_name_png, width=Inches(4.5), )
                    last_paragraph = doc.paragraphs[-1]
                    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 图片居中设置
                    os.remove(file_name_png)  # 插入图片完毕之后删除掉

                # =================================================================================================================
                # 媒体来源
                cursor.execute(
                    "SELECT key_name,sum(key_value) AS counts FROM  analyse_count_number where title_id=%s  and hisdate>=%s and hisdate<=%s and summary_type='meiti' GROUP BY key_name",
                    (
                        title_id, from_date, end_date))
                media_list = cursor.fetchall()
                media_count = 0
                media_names = []
                media_values = []
                for media in media_list:
                    print(media[0], media[1])
                    media_names.append(media[0])
                    media_values.append(media[1])
                    media_count += int(media[1])
                # 生成媒体统计饼图
                plt.pie(media_values,
                        labels=media_names,  # 每个扇形的名字，和percent对应
                        autopct='%1.1f%%',  # 百分比的小数点方式到1个小数点
                        shadow=False,  # 阴影
                        )
                plt.axis('equal')  # 正圆
                print(2)
                # 此处保存位置后期需要变化，文件名也需要变化
                # file_name = 'a/' + str(int(time.time() * 10000)) + ".png"
                # file_name_png = file_name + '123.png'
                plt.savefig(file_name_png, dpi=120)  # 保存为123456.png， 保存之后如果要使用，需要等待一段时间才能保存完毕，大概时间是5秒。dpi=120图片大小刚好适合
                # plt.show()
                plt.close()
                paragraph_media = doc.add_paragraph()
                paragraph_media.add_run('2.媒体分析：\n').bold = True
                paragraph_media.add_run('监测周期内，网媒{wangmei}条，微信公众号{weixin}条，传统纸媒{paper}条，微博{weibo}条，贴吧{tieba}条。\n'.format(
                    wangmei=media_values[media_names.index('网媒')], weixin=media_values[media_names.index('微信公众号')],
                    paper=media_values[media_names.index('报纸')], weibo=media_values[media_names.index('微博')],
                    tieba=media_values[media_names.index('百度贴吧')]))
                # 只有总数不为0,才进行图片插入,否则没有意义,是一张空白图片
                if media_count != 0:
                    pic1 = doc.add_picture(file_name_png, width=Inches(4.5))
                    last_paragraph = doc.paragraphs[-1]
                    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 图片居中设置
                    os.remove(file_name_png)  # 插入图片完毕之后删除掉

                # =================================================================================================================
                # 信息来源
                cursor.execute(
                    "SELECT key_name,sum(key_value) AS counts FROM  analyse_count_number where title_id=%s and  hisdate>=%s and hisdate<=%s and summary_type='hotmedia' GROUP BY key_name",
                    (
                        title_id, from_date, end_date))
                hotmedia_list = list(cursor.fetchall())
                # 对hotmedia_list进行倒序排列,按下标为1的值进行排序
                hotmedia_list = sorted(hotmedia_list, key=itemgetter(1), reverse=True)
                print("hotmedia_list", hotmedia_list)
                hotmedia_names_list = []
                hotmedia_values_list = []
                add_str = '监测周期内，'
                if len(hotmedia_list) >= 10:
                    for tup in hotmedia_list[:10]:
                        add_str = add_str + tup[0] + str(tup[1]) + '条,'
                        hotmedia_names_list.append(tup[0])
                        hotmedia_values_list.append(tup[1])
                else:
                    for tup in hotmedia_list:
                        add_str = add_str + tup[0] + str(tup[1]) + '条,'
                        hotmedia_names_list.append(tup[0])
                        hotmedia_values_list.append(tup[1])
                # 生成媒体统计柱状图
                plt.bar(hotmedia_names_list, hotmedia_values_list, )
                plt.xticks(rotation=20)
                # plt.show()

                # print(2)
                # 此处保存位置后期需要变化，文件名也需要变化
                # file_name = 'a/' + str(int(time.time() * 10000)) + ".png"
                # file_name = "E:\phpStudy\PHPTutorial\WWW\www.yuqing.cn\public\web\\analyse"
                # end_date_str = re.match('\d{4}-\d{2}',str(end_date))
                # file_name = file_name + end_date_str.group()+ str('\\')

                plt.savefig(file_name_png, dpi=120)  # 保存为123456.png， 保存之后如果要使用，需要等待一段时间才能保存完毕，大概时间是5秒。dpi=120图片大小刚好适合
                # plt.show()
                plt.close()
                paragraph_hotmedia = doc.add_paragraph()
                paragraph_hotmedia.add_run('3.信息来源分析：\n').bold = True
                paragraph_hotmedia.add_run(add_str)
                # 只有总数不为0,才进行图片插入,否则没有意义,是一张空白图片
                if media_count != 0:
                    pic1 = doc.add_picture(file_name_png, width=Inches(4.5))
                    last_paragraph = doc.paragraphs[-1]
                    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 图片居中设置
                    os.remove(file_name_png)  # 插入图片完毕之后删除掉

            doc_name = file_name + str('\\') + str(int(time.time() * 10000)) + ".docx"
            print(doc_name)
            doc.save(doc_name)
            path = re.match(r"E:\\phpStudy\\PHPTutorial\\WWW\\www.yuqing.cn\\public(.*)", doc_name)
            if path:
                path = path.group(1).replace("\\", '/')
                cursor.execute("UPDATE gen_report set flag=%s,path=%s where id = %s", ('0', path, id))
                connect.commit()
                print('更新完成')
        time.sleep(10)
    else:
        print('没有需要生成的报告')
        time.sleep(60)


