# coding=utf-8
from selenium import webdriver
from time import sleep
import json
class Sina:
    def __init__(self):
        self.url = 'http://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1'
        self.driver = webdriver.Chrome()

    def get_content_list(self):
        sleep(1.5)
        li_list = self.driver.find_elements_by_xpath("//div[@id='d_list']/ul/li")
        contetn_list = []
        for li in li_list:
            item={}
            item['url'] = li.find_element_by_xpath("./span[@class='c_tit']/a").get_attribute('href')
            item['title'] = li.find_element_by_xpath("./span[@class='c_tit']/a").text
            item['time'] = li.find_element_by_xpath("./span[@class='c_time']").text
            print(item)
            contetn_list.append(item)
        #获取下一页的按钮
        next_page = self.driver.find_elements_by_xpath("//span[@class='pagebox_pre']/a[text()='下一页']")
        next_page = next_page[0] if len(next_page)>0 else None
        return contetn_list,next_page

    def save_content_list(self,content_list):
        for content in content_list:
            with open('get_url_2','a') as f:
                f.write(json.dumps(content,ensure_ascii=False,indent=2))


    def run(self):
        # 1.start_url
        # 2.发送请求
        self.driver.get(self.url)
        #3.获取数据和下一页的按钮
        content_list,next_page = self.get_content_list()
        #4.保存
        self.save_content_list(content_list)
        #5.到下一页，循环
        while next_page is not None:
            sleep(2.5)
            next_page.click()
            # 3.获取数据和下一页的按钮
            content_list, next_page = self.get_content_list()
            # 4.保存
            self.save_content_list(content_list)

    def __del__(self):
        self.driver.quit()

if __name__ == '__main__':
    sina = Sina()
    sina.run()







