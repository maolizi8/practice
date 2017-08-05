
import pytest
from time import sleep
import sys

testdata=[
    ('python','python'),
    ('selenium','selenium'),
    ('test','test')
]

@pytest.mark.parametrize("search_words,expected", testdata)
def test_bd_search(selenium,search_words,expected):
    '''测试百度搜索'''
    selenium.get('https://www.baidu.com/')
    sleep(2)
    print(selenium.title)
    sys.stderr.write("world\n")
    search_in=selenium.find_element_by_id('kw')
    search_in.clear()
    search_in.send_keys(search_words)
    selenium.find_element_by_id('su').click()
    sleep(2)
    exp_title=expected+"_百度搜索"
    result_title=selenium.title
    selenium.quit()
    assert result_title==exp_title


if __name__=="__main__":
    import os
    import time
    stamp=time.strftime('%Y%m%d_%H%M%S')
    file_name=os.path.basename(__file__)
    print(file_name)
    report_name=os.path.abspath(os.path.join('..','Reports',file_name.split('.')[0]+'_'+stamp+'.html'))
    print(report_name)
    args = [file_name,'--driver=Chrome','--html='+report_name,'--self-contained-html']
    pytest.main(args)