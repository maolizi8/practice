'''
Created on 2017年7月29日

@author: gql
'''
from src.Homepage import Homepage
import pytest


@pytest.mark.bd_1
def test_search(selenium):
    h=Homepage(selenium)
    h.open_baidu()
    t=h.baidu_search('python')
    assert 'python' in t

if __name__=='__main__':
    import os
    from utils.PubLib import run_testcase
    run_testcase(os.path.basename(__file__))