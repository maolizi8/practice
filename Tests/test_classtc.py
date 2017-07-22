'''
Created on 2017-07-22

@author: lxl
'''

import pytest

class TestClass:
    '''测试类'''
    def test_one(self):
        '''测试类的用例1'''
        print('one')
        x = "this"
        assert 'h' in x
        
    def test_two(self):
        '''测试类的用例2'''
        print('two')
        x = "hello"
        assert hasattr(x, 'check')
        
if __name__ == '__main__':
    args=['-q','test_classtc.py','--html=test_class_report.html']
    pytest.main(args)