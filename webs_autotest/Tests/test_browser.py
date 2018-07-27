'''
Created on 2017年7月29日

@author: gql
'''
from time import sleep
import logging
from Business import baidu
 
logging.basicConfig(level=logging.DEBUG)
 

def test_baidu(selenium):
    log = logging.getLogger('test_1')
    baidu.bd_search(selenium)
    sleep(2)
    log.debug('after 2 sec')
    assert 1!=1

if __name__ == '__main__':
    import pytest
    import os
    import time
    from conftest import root_dir
    report_dir=root_dir+'Reports'+os.sep
    stamp=time.strftime('%Y%m%d_%H%M%S')
    file_name=os.path.basename(__file__)
    print(file_name)
    report_name=os.path.abspath(report_dir+file_name.split('.')[0]+'_'+stamp+'.html')
    print(report_name)
    args = [file_name,'--driver=Chrome','--html='+report_name,'--self-contained-html']
    pytest.main(args)