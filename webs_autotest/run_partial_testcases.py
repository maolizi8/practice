"""
Created on 2017年7月11日

@author: gql
"""
import unittest
import time
import os
import importlib
from Tools.HTMLTestRunner import HTMLTestRunner
from Tools.PubLib import send_mail,get_new_report

# def set_testsuite():
#     test_suite=unittest.TestSuite()
#     from Test.TestLogin import TestLogin
#     from Test.TestShoppingCart import TestShoppingCart
#     testcases=[
#          TestLogin('test_login_pc'),
#          TestShoppingCart('test_demo1')
#          ]
#     test_suite.addTests(testcases)
#     return test_suite
        

def get_partial_tc(tc_file):
    suite=unittest.TestSuite()
    with open(tc_file,'r') as f:
        for line in f.readlines()[1:]:
            arr=line.strip().split(',')
            module_name=importlib.import_module('Test.'+arr[0])
            obj=getattr(module_name, arr[1])
            suite.addTest(obj(arr[2]))
    print(suite)
    return suite
            
report_dir=os.path.abspath('Reports')
tc_file=os.path.abspath(os.path.join('Data','run_partial_testcases.csv'))
mail_to_list=os.path.abspath(os.path.join('Data','mail_to_userlist.txt'))

if __name__=='__main__':

    test_suite=get_partial_tc(tc_file)
    
    timestamp=time.strftime("%Y_%m_%d %H_%M_%S")
    report_file=os.path.abspath(os.path.join('Reports',timestamp+' Report.html'))

    with open(report_file,'wb') as f:
        runner = HTMLTestRunner(stream=f,verbosity=2, title='UI自动化指定测试用例执行报告',description='执行部分重要测试用例')
        runner.run(test_suite)
    
    new_report = get_new_report(report_dir)
    #send_mail(new_report,mail_to_list)