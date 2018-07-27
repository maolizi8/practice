'''
Created on 2017年7月11日

@author: gql
'''
import unittest
import os
import time
from Tools.HTMLTestRunner import HTMLTestRunner
from Tools.PubLib import send_mail,get_new_report

report_dir=os.path.abspath('Reports')
mail_to_list=os.path.abspath(os.path.join('Data','mail_to_userlist.txt'))

if __name__ == '__main__':
    timestamp=time.strftime("%Y_%m_%d %H_%M_%S")
    report_file=os.path.abspath(os.path.join('Reports',timestamp+' Report.html'))
    test_dir=os.path.abspath('Test')
    discover = unittest.defaultTestLoader.discover(test_dir,pattern='Test*.py')
    with open(report_file,'wb') as f:
        runner = HTMLTestRunner(stream=f,verbosity=2, title='UI自动化全部测试用例执行报告',description='执行所有测试用例')
        runner.run(discover)
    
    new_report = get_new_report(report_dir)
    send_mail(new_report,mail_to_list)