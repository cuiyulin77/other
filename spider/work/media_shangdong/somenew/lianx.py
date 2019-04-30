import requests
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

class get_es_data(object):
    def __init__(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        }

    def get_url(self):
        es2 = Elasticsearch()


        print(re)

    def run(self):
        self.get_url()




if __name__ == '__main__':
    D = get_es_data()
    D.run()
