'''
Created on 2017年7月11日

@author: gql
使用unittest框架，运行测试用例
'''
import unittest
import os
import time
from utils.HTMLTestRunner import HTMLTestRunner
from utils.PubLib import send_mail
from conftest import root_dir

def run_all_case(case_dir):
    ''''''
    report_dir=root_dir+'reports'+os.sep
    mail_to_list=os.path.abspath(os.path.join('Data','mail_to_userlist.txt'))
    timestamp=time.strftime("%Y%m%d %H%M%S")
    report_file=report_dir+'AllCases_Report_'+timestamp+'.html'
    test_dir=root_dir+case_dir+os.sep
    discover = unittest.defaultTestLoader.discover(test_dir,pattern='Test_*.py')
    with open(report_file,'wb') as f:
        runner = HTMLTestRunner(stream=f,verbosity=2, title='UI自动化全部测试用例执行报告',description='执行所有测试用例')
        result=runner.run(discover)
        if result.failure_count>0:
            print('有 {} 个失败的用例'.format(result.failure_count))
    
    send_mail(report_file,mail_to_list)
    

if __name__ == '__main__':
    run_all_case('testcases')