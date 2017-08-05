'''
Created on 2017年7月29日

@author: gql
'''
from Business import baidu

def test_bd(selenium):
    '''测试百度搜索'''
    title=baidu.bd_search(selenium)
    assert 'python_' in title


if __name__ == '__main__':
    import pytest
    import os
    import time
    stamp=time.strftime('%Y%m%d_%H%M%S')
    file_name=os.path.basename(__file__)
    print(file_name)
    report_name=os.path.abspath(os.path.join('..','Reports',file_name.split('.')[0]+'_'+stamp+'.html'))
    print(report_name)
    args = [file_name,'--driver=Chrome','--html='+report_name,'--self-contained-html']
    pytest.main(args)