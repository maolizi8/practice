'''
@author: gql
'''
from selenium import webdriver
import login
from time import sleep

def add_to_shop_cart(selenium):
    login_via_cookie(selenium)
    selenium.get("http://www.111.com.cn/product/972682.html")
    sleep(2)
    print(selenium.find_element_by_class_name("cart_num").text)
    print(selenium.find_element_by_css_selector("#rightFloat>a[title=\"购物车\"]").text)
    selenium.find_element_by_id('seriesCartButton').click()
    sleep(2)
    print(selenium.find_element_by_class_name("cart_num").text)
    print(selenium.find_element_by_css_selector("#rightFloat>a[title=\"购物车\"]").text)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(20)
    add_to_shop_cart(driver)