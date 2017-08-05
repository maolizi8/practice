'''
Created on 2017-07-22

@author: lxl
'''

def test_main():
    '''测试方法的用例'''
    assert 5 != 5

def test_demo1():
    assert 5>4
    
if __name__ == '__main__':
    import pytest
    import os
    import time
    stamp=time.strftime('%Y%m%d_%H%M%S')
    file_name=os.path.basename(__file__)
    print(file_name)
    report_name=os.path.abspath(os.path.join('..','Reports',file_name.split('.')[0]+'_'+stamp+'.html'))
    print(report_name)
    args = [file_name,'--html='+report_name,'--self-contained-html']
    pytest.main(args)