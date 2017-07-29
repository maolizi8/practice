import pytest
import os
import time
from time import sleep

def test_bd(selenium):
    '''测试fixture: selenium'''
    selenium.get('http://www.baidu.com')
    sleep(2)


if __name__ == '__main__':
    stamp=time.strftime('%Y%m%d_%H%M%S')
    report_name = os.path.abspath(os.path.join('..', 'Reports', 'test_driver_report'+stamp+'.html'))

    print(report_name)
    args = ['test_driver.py','--driver=Chrome','--html=' + report_name,'--self-contained-html']
    pytest.main(args)