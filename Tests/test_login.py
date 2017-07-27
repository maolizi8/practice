'''
Created on 2017年7月27日

@author: geqiuli
'''
import os
import pytest
from Business import login
testdata=[
    (['13817023324','123456'])
    ]

@pytest.mark.parametrize("account",testdata)
def test_login_account(selenium, account):
    result=login.login_via_account(selenium, account)
    assert result=='13817023324 欢迎您！'
    
if __name__ == '__main__':
    report_name = os.path.abspath(os.path.join('..', 'Reports', 'test_login_report.html'))
    print(report_name)
    args = ['-q','test_login.py','--driver=Chrome', '--html=' + report_name]
    pytest.main(args)