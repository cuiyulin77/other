# coding=utf-8
from selenium import webdriver
from time import sleep

class DouYu:
    def __init__(self):
        self.start_url = "https://www.douyu.com/directory/all"
        self.driver = webdriver.Chrome()

    def get_content_list(self): #3. 获取数据，下一页的按钮
        li_list = self.driver.find_elements_by_xpath("//ul[@id='live-list-contentbox']/li")
        content_list = []
        for li in li_list: #提取数据
            item = {}
            item["title"] = li.find_element_by_xpath("./a").get_attribute("title")
            item["cate"] = li.find_element_by_xpath(".//div[@class='mes-tit']/span").text
            item["watch_num"] = li.find_element_by_xpath(".//span[@class='dy-num fr']").text
            print(item)
            content_list.append(item)
        #获取下一页的按钮
        next_page = self.driver.find_elements_by_class_name("shark-pager-next")
        next_page = next_page[0] if len(next_page)>0 else None
        return content_list,next_page

    def save_content_list(self,content_list):
        pass

    def run(self):
        #1.start_url
        #2.发送请求，
        self.driver.get(self.start_url)
        #3. 获取数据，下一页的按钮
        content_list,next_page = self.get_content_list()
        #4.保存
        self.save_content_list(content_list)
        #5.到下一页，循环
        while next_page is not None:
            next_page.click()
            sleep(1)
            # 3. 获取数据，下一页的按钮
            content_list, next_page = self.get_content_list()
            # 4.保存
            self.save_content_list(content_list)
        # self.driver.quit()

    def __del__(self):
        self.driver.quit()

if __name__ == '__main__':
    douyu = DouYu()
    douyu.run()