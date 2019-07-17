#-*- coding: utf-8 -*-
'''
Created on 2018年9月19日

@author: geqiuli
'''
import pytest
import os

projname='AutoTest'
root_dir=os.path.abspath('conftest.py').split(projname)[0]+projname+os.sep
print(root_dir)


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(60)
    return selenium

@pytest.fixture
def chrome_options(chrome_options):
    mobileEmulation = {'deviceName': 'iPhone 6'}
    #chrome_options.add_argument('--start-maximized')
    chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)
    return chrome_options