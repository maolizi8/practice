'''
@author: gql
'''
from selenium import webdriver
from time import sleep
import os
import json

def login_via_account(selenium,account):
    selenium.get("http://www.111.com.cn/")
    sleep(2)
    selenium.find_element_by_css_selector("#logininfo>a[title=\"登录1药网\"]").click()
    sleep(2)
    print(selenium.current_url)
    username=selenium.find_element_by_id("userName")
    username.clear()
    username.send_keys(account[0])
    pwd=selenium.find_element_by_id("userPass")
    pwd.clear()
    pwd.send_keys(account[1])
    selenium.find_element_by_id("btnSubmit").click()
    sleep(2)
    print(selenium.current_url)
    dictCookies=selenium.get_cookies()
    jsonCookies=json.dumps(dictCookies)
    with open('cookies.json','w') as f:
        f.write(jsonCookies)
    disp_name=selenium.find_element_by_css_selector("#logininfo>span").text
    selenium.quit()
    print(disp_name)

def login_via_cookie(selenium):
    selenium.get("http://www.111.com.cn/")
    sleep(2)
    selenium.delete_all_cookies()
    # 读取登录时存储到本地的cookie
    with open('cookies.json', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        selenium.add_cookie({
            'domain': '.111.com.cn',  # 此处xxx.com前，需要带点
            'name': cookie['name'],
            'value': cookie['value'],
            'path': '/',
            'expires': None
        })
    sleep(2)
    # 再次访问页面，便可实现免登陆访问
    selenium.get('http://www.111.com.cn/')
    sleep(2)
    disp_name = selenium.find_element_by_css_selector("#logininfo>span").text
    #selenium.quit()
    print(disp_name)


if __name__ == '__main__':
    account=['13817023324','123456']
    driver=webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(20)
    #login_via_account(driver,account)
    login_via_cookie(driver)