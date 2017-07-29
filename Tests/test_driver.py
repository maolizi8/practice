import pytest
import os
from time import sleep


# @pytest.fixture
# def selenium(selenium):
#     selenium.implicitly_wait(10)
#     selenium.maximize_window()
#     return selenium


def test_bd(selenium):
    '''测试fixture: selenium'''
    selenium.get('http://www.baidu.com')
    sleep(2)
    selenium.quit()


if __name__ == '__main__':
    report_name = os.path.abspath(os.path.join('..', 'Reports', 'test_driver_report.html'))

    print(report_name)
    args = ['test_driver.py','--driver=Chrome','--html=' + report_name,'--self-contained-html']
    pytest.main(args)