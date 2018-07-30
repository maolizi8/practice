'''
Created on 2017-07-22

@author: lxl
'''

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
    import os
    from utils.PubLib import run_testcase
    run_testcase(os.path.basename(__file__))
    