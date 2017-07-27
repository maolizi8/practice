# -*- coding: utf-8 -*-
'''
@author: gql
'''
from time import sleep

def add_to_shop_cart(selenium):
    selenium.get("http://www.111.com.cn/product/50007206.html")
    sleep(2)
    before_add=selenium.find_element_by_class_name("cart_num").text.strip()
    print(before_add)
    add_btn=selenium.find_element_by_id('seriesCartButton')
    add_btn.click()
    sleep(2)
    after_add=selenium.find_element_by_class_name("cart_num").text.strip()
    print(after_add)
    return before_add,after_add


if __name__ == '__main__':
    from selenium import webdriver
    import login
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(20)
    account=['13817023324','123456']
    login.login_via_account(driver, account)
    driver.refresh()
    add_to_shop_cart(driver)