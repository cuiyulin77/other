#coding=utf-8
from selenium import webdriver

while True:
    driver = webdriver.Chrome()
    driver.get('http://www.theping.cn/e/action/ListInfo/?classid=139')
    driver.find_element_by_xpath('//*[@id="divcon1"]/div[1]/a/div[2]/h1').click()
    driver.close()


