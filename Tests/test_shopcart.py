# -*- coding: utf-8 -*-
'''
Created on 2017年7月26日

@author: geqiuli
'''
import pytest
import os
from Business import login
from Business import shop_cart
from Tools.FilesOpr import get_info_from_txt



def test_addtoshopcart_login(selenium):
    account_info=get_info_from_txt("../Datas/sensitive/account.txt")
    login.login_via_account(selenium, account_info)
    selenium.refresh()
    before,after=shop_cart.add_to_shop_cart(selenium)
    assert int(after)==int(before)+1
    
def test_addtoshopcart_visitor(selenium):
    before,after=shop_cart.add_to_shop_cart(selenium)
    assert int(after)==int(before)+1

if __name__ == '__main__':
    report_name = os.path.abspath(os.path.join('..', 'Reports', 'test_shopcart_report.html'))
    print(report_name)
    args = ['-q','test_shopcart.py','--driver=Chrome', '--html=' + report_name]
    pytest.main(args)