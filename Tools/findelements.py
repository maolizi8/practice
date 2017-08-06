'''
Created on 2017年8月6日

@author: lxl
'''
#from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
def find_ele(driver,by,value):
    try:
        return driver.find_element(by,value)
    except NoSuchElementException:
        print('cannot find:'+value)
        raise

def test_find_ele(selenium):
    selenium.get("http://www.baidu.com")
    s=find_ele(selenium,by=By.ID,value='setf1')
    print(s.text)
    assert 1==1
    
if __name__ == '__main__':
    import pytest
    import os
    import time
    stamp=time.strftime('%Y%m%d_%H%M%S')
    file_name=os.path.basename(__file__)
    print(file_name)
    report_name=os.path.abspath(os.path.join('..','Reports',file_name.split('.')[0]+'_'+stamp+'.html'))
    print(report_name)
    args = ['-v',file_name,'--driver=Chrome','--html='+report_name,'--self-contained-html']
    pytest.main(args)