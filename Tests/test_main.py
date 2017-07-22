'''
Created on 2017-07-22

@author: lxl
'''
import pytest
import os

def test_main():
    '''测试方法的用例'''
    assert 5 != 5

def test_demo1():
    assert 5>4
    
if __name__ == '__main__':
    tc_dir=os.path.split(os.path.realpath(__file__))[0]
    print(tc_dir)
    
    pytest.main(tc_dir)  # 指定测试目录