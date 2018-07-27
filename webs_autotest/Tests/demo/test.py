'''
Created on 2017年8月6日

@author: lxl
'''
import pytest
@pytest.mark.capabilities(foo='bar')
def test_capabilities(selenium):
    selenium.get('http://www.example.com')
    
if __name__ == '__main__':
    import os
    import time
    from conftest import root_dir
    report_dir=root_dir+'Reports'+os.sep
    stamp=time.strftime('%Y%m%d_%H%M%S')
    file_name=os.path.basename(__file__)
    print(file_name)
    report_name=os.path.abspath(report_dir+file_name.split('.')[0]+'_'+stamp+'.html')
    print(report_name)
    args = ['-v',file_name,'--driver=Chrome','--html='+report_name,'--self-contained-html']
    pytest.main(args)