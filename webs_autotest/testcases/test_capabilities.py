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
    from utils.PubLib import run_testcase
    run_testcase(os.path.basename(__file__))