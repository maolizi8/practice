'''
Created on 2017-07-22

@author: lxl
'''
import pytest
import os
import time


if __name__ == '__main__':
    tc_dir=os.path.abspath('Tests')
    report_dir=os.path.abspath('Reports')
    timestamp=time.strftime('%Y%m%d_%H%M%S')
    report_name=os.path.join(report_dir,'all_'+timestamp+'.html')
    print(report_name)
    args=['-q',tc_dir,'--html='+report_name]
    pytest.main(args)  # 指定测试目录