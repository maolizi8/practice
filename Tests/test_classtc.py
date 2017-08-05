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
    import pytest
    import os
    import time
    stamp=time.strftime('%Y%m%d_%H%M%S')
    file_name=os.path.basename(__file__)
    print(file_name)
    report_name=os.path.abspath(os.path.join('..','Reports',file_name.split('.')[0]+'_'+stamp+'.html'))
    print(report_name)
    args=[file_name,'--html='+report_name,'--self-contained-html']
    pytest.main(args)
    