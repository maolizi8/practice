import pytest
from business.home_page import HomePage
from business.user_center import UserCenter

@pytest.mark.test_level_0
def test01_home(app_driver):
    '''首页，广告弹框'''
    h=HomePage(app_driver)
    h.go_to_home()
    h.go_to_home_pop_advise()
    

if __name__ == '__main__':
    from func import tools
    import os
    tools.run_case(__file__, 'test_level_0',['--device=emulator-5554']) 
