'''
Created on 2018年7月27日

@author: gql
'''
from selenium.webdriver.common.by import By


class Home:
    search_input = (By.ID, "kw1")  # 搜索输入框
    search_button = (By.ID, "su")  # 百度一下
    

class Zhidao:
    search_input = (By.ID, "kw")  # 搜索输入框
    search_button = (By.ID, "search-btn")  # 搜索答案
    ask_button = (By.ID, "ask-btn-new")  # 我要提问