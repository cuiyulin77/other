# coding=utf-8
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Completion
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

# connections.create_connection(hosts=['47.92.77.18'])
connections.create_connection(hosts=['localhost'])
# connections.create_connection(hosts=['192.168.3.15'])

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word",filter=["lowercase"])

class Sina_type(DocType):
    suggest = Completion(analyzer=ik_analyzer,)
    title = Text(analyzer='ik_max_word',)
    publish_time = Date()
    create_time = Date()
    url = Keyword()
    media = Keyword()
    comm_num = Integer()
    read_num = Integer()
    fav_num = Integer()
    env_num = Integer()
    content = Text(analyzer='ik_max_word')



    class Meta:
        index = 'spider'
        doc_type = 'article'

if __name__ == '__main__':
    Sina_type.init()
