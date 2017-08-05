import pytest
import os
import sys
from datetime import datetime
from py.xml import html

<<<<<<< HEAD

projname='python_selenium'
root_dir=os.path.abspath(sys.argv[0]).split(projname)[0]+projname+os.sep

=======
projname='python_selenium'
root_dir=os.path.abspath(sys.argv[0]).split(projname)[0]+projname+os.sep

>>>>>>> fb39ae436d8d77b07cd16f79538a7ac24ba77dc0
# import logging
# import time
# rootdir=os.path.abspath(sys.argv[0]).split('python_selenium')[0]
# 
# logging.basicConfig(level=logging.DEBUG,
#                 filename=rootdir+'\\python_selenium\\Logs\\myapp'+time.strftime('%Y%m%d_%H%M%S')+'.log',
#                 filemode='w')

@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(10)
    selenium.maximize_window()
    return selenium

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.pop()

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.pop()

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
