'''
Created on 2017年8月6日

@author: lxl
'''
import pytest
@pytest.mark.capabilities(foo='bar')
def test_capabilities(selenium):
    selenium.get('http://www.example.com')
    
if __name__=="__main__":
    from public.tests import run_case
    run_case(__file__,'bd_1')