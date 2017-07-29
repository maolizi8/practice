'''
Created on 2017年7月29日

@author: lxl
'''
import pytest
import time
from time import sleep
import os
import logging
from Business import baidu
 
logging.basicConfig(level=logging.DEBUG)
 

def test_baidu(selenium):
    log = logging.getLogger('test_1')
    baidu.bd_search(selenium)
    sleep(2)
    log.debug('after 2 sec')
    assert 1!=1

if __name__ == '__main__':
    stamp=time.strftime('%Y%m%d_%H%M%S')
    report_name = os.path.abspath(os.path.join('..', 'Reports', 'test_browser_report'+stamp+'.html'))

    print(report_name)
    args = ['-s','test_browser.py','--driver=Chrome','--html='+report_name,'--self-contained-html']
    pytest.main(args)