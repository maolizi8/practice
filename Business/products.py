'''
Created on 2017年7月27日

@author: geqiuli
'''
from time import sleep

def search_pro(selenium):
    searchinput=selenium.find_element_by_id("word")
    searchinput.clear()
    searchinput.send_keys("1598980179")
    selenium.find_element_by_class_name("searchBtn").click()
    sleep(3)
    
    

if __name__ == '__main__':
    from selenium import webdriver
    driver=webdriver.Chrome()