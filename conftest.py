import pytest
import logging
import time
import os
import sys

rootdir=os.path.abspath(sys.argv[0]).split('python_selenium')[0]

logging.basicConfig(level=logging.DEBUG,
                filename=rootdir+'\\python_selenium\\Logs\\myapp'+time.strftime('%Y%m%d_%H%M%S')+'.log',
                filemode='w')

@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(10)
    selenium.maximize_window()
    return selenium


