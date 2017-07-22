import os
import pytest
from selenium import webdriver
from time import sleep


testdata=[
    (webdriver.Chrome,'python','python'),
    (webdriver.Firefox,'selenium','selenium'),
    (webdriver.Chrome,'test','test')
]

@pytest.mark.parametrize("browser,search_words,expected", testdata)
def test_bd_search(browser,search_words,expected):
    '''测试百度搜索'''
    driver=browser()
    driver.implicitly_wait(30)
    driver.get('https://www.baidu.com/')
    sleep(2)
    search_in=driver.find_element_by_id('kw')
    search_in.clear()
    search_in.send_keys(search_words)
    driver.find_element_by_id('su').click()
    sleep(2)
    exp_title=expected+"_百度搜索"
    result_title=driver.title
    driver.quit()
    assert result_title==exp_title


if __name__=="__main__":
    report_name = os.path.abspath(os.path.join('..', 'Reports', 'test_baidu_report.html'))
    print(report_name)
    args = ['-q', 'test_baidu.py', '--html=' + report_name]
    pytest.main(args)