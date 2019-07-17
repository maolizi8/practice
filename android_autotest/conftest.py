"""
Created on 2018年8月7日

@author: geqiuli
"""
import pytest
import os
from py.xml import html #html的错误提示请忽略
from datetime import datetime
import io
import json
from appium import webdriver
from localplugins.simplehtml import HTMLReport


proj_name="android_autotest"
root_dir=os.path.abspath(__file__).split(proj_name)[0]+proj_name+os.sep
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print('conftest - BASE_DIR :',BASE_DIR)


DEVICE="emulator-5554" #模拟器为例
APP_PACKAGE = "APP_PACKAGE"	# APP包名
APP_START_ACTIVITY = ".LoadingActivity"

APPIUM_HOST = "localhost"   #window下：127.0.0.1   mac下：0.0.0.0
APPIUM_PORT = "4723"

def pytest_configure(config):
    htmlpath = config.getoption('htmlpath')
    htmlhead = config.getoption('htmlhead')
    is_simplehtml = config.getoption('--simple-html')
    
    if htmlpath and is_simplehtml:
        for csspath in config.getoption('css') or []:
            open(csspath)
        if not hasattr(config, 'slaveinput'):
            config._html = HTMLReport(htmlpath, config, htmlhead)
            config.pluginmanager.register(config._html)

def pytest_unconfigure(config):
    html = getattr(config, '_html', None)
    if html:
        del config._html
        config.pluginmanager.unregister(html)
        
def read_json(file_name, subdir=""):
    if subdir:
        fpath=os.sep.join([BASE_DIR,"file",subdir,file_name]) + ".json"
    else:
        fpath=os.sep.join([BASE_DIR,"file",file_name]) + ".json"
    json_content={}    
    with open(fpath, "r", encoding="utf-8") as f:
        json_content = json.loads(f.read())
    return json_content    
    
def pytest_addoption(parser):
    """命令行参数"""
    group = parser.getgroup('terminal reporting')
    group.addoption('--htmlhead', action='store', dest='htmlhead',default='测试报告',
                    help='the head of html report.')
    group.addoption('--simple-html', action='store_true',
                    help='use simple html moudle.')
    group.addoption('--jkbuildid', action='store',default=-1,
                    help='jenkins buildid, to make online html report.')
    group.addoption('--jkjobname', action='store',
                    help='jenkins jobname, to make online html report.')
    
    parser.addoption("--device", action="store", default=DEVICE,
        help="udid of the device to run scripts")
    parser.addoption("--appium_host", action="store", default=APPIUM_HOST,
        help="appium server host")
    parser.addoption("--appium_port", action="store", default=APPIUM_PORT,
        help="appium server port")
    parser.addoption("--exc_env", action="store", default="test",
        help="testcase excute envirenment: test/prd")


@pytest.fixture
def device(request):
    """命令行输入设备的udid"""
    return request.config.getoption("--device")

@pytest.fixture
def appium_host(request):
    """命令行输入appium server的host"""
    return request.config.getoption("--appium_host")

@pytest.fixture
def appium_port(request):
    """命令行输入appium server的port"""
    return request.config.getoption("--appium_port")

@pytest.fixture
def exc_env(request):
    '''运行环境'''
    return request.config.getoption("--exc_env")

# @pytest.fixture(scope="session")
# def app_driver_class(request):
#     driver = request.config.getoption("app_driver")
#     if driver is None:
#         raise pytest.UsageError("--app_driver must be specified")
#     return driver

@pytest.fixture(scope="module")
def app_driver(request):
    """"""
    test_devices={
        "emulator-5554":{
            #模拟器，这里以mumu模拟器为例，如果是雷电模拟器，需将"automationName":"uiautomator2"注释掉
            #"automationName":"uiautomator2"
            "platformVersion": "5.1.1",
            "deviceName": "模拟器",
            "udid":"emulator-5554",
            }
    }
    udid=request.config.getoption("--device")
    if udid in test_devices:
        print("运行手机：",test_devices[udid]["deviceName"],udid)
        
    clear_command="adb -s "+udid+" shell pm clear "+APP_PACKAGE
    print("清除缓存：",clear_command)
    os.system(clear_command)
    capabilities = {
                    #"app": "apk路径",
                    #"automationName":"uiautomator2", #android7及以上需要加此参数 mac也需要此参数
                    "platformName": "Android",
                    "platformVersion": "6.0.1",
                    "deviceName": udid,
                    "udid":udid,
                    "appPackage": APP_PACKAGE,
                    "appActivity": APP_START_ACTIVITY,
                    "unicodeKeyboard": True,
                    "resetKeyboard": True,
                    "noReset": True
                    }
    
    if udid in test_devices:
        capabilities.update(test_devices[udid])
    #print(capabilities)
    dr = webdriver.Remote("http://"+APPIUM_HOST+":"+APPIUM_PORT+"/wd/hub", capabilities)
    if dr.is_locked():
        dr.unlock()
    yield dr
    def dr_finalizer():
        dr.close_app()
        print("清除缓存：",clear_command)
        os.system(clear_command)   #清除缓存
        dr.quit()
    request.addfinalizer(dr_finalizer)


'''测试报告'''            
def _gather_driver_log(item, summary, extra):
    pytest_html = item.config.pluginmanager.getplugin('html')
    if hasattr(item.config, '_driver_log') and \
       os.path.exists(item.config._driver_log):
        if pytest_html is not None:
            with io.open(item.config._driver_log, 'r', encoding='utf8') as f:
                extra.append(pytest_html.extras.text(f.read(), 'Driver Log'))
            summary.append('Driver log: {0}'.format(item.config._driver_log))
            
def _gather_screenshot(item, report, driver, summary, extra):
    try:
        #截图前先切回原生： NATIVE_APP
        pre_context=driver.current_context
        if pre_context!='NATIVE_APP':
            driver.switch_to.context('NATIVE_APP')
        screenshot = driver.get_screenshot_as_base64()
        
        if pre_context!='NATIVE_APP':
            driver.switch_to.context(pre_context)
    except Exception as e:
        summary.append('WARNING: Failed to gather screenshot: {0}'.format(e))
        return
    pytest_html = item.config.pluginmanager.getplugin('html')
    if pytest_html is not None:
        # add screenshot to the html report
        extra.append(pytest_html.extras.image(screenshot, 'Screenshot'))

def _gather_html(item, report, driver, summary, extra):
    try:
        html = driver.page_source
    except Exception as e:
        summary.append('WARNING: Failed to gather HTML: {0}'.format(e))
        return
    pytest_html = item.config.pluginmanager.getplugin('html')
    if pytest_html is not None:
        # add page source to the html report
        extra.append(pytest_html.extras.text(html, 'HTML'))

def format_log(log):
    timestamp_format = '%Y-%m-%d %H:%M:%S.%f'
    entries = [u'{0} {1[level]} - {1[message]}'.format(
        datetime.utcfromtimestamp(entry['timestamp'] / 1000.0).strftime(
            timestamp_format), entry).rstrip() for entry in log]
    log = '\n'.join(entries)
    return log

def _gather_logs(item, report, driver, summary, extra):
    pytest_html = item.config.pluginmanager.getplugin('html')
    try:
        types = driver.log_types
    except Exception as e:
        # note that some drivers may not implement log types
        summary.append('WARNING: Failed to gather log types: {0}'.format(e))
        return
    for name in types:
        try:
            log = driver.get_log(name)
        except Exception as e:
            summary.append('WARNING: Failed to gather {0} log: {1}'.format(
                name, e))
            return
        if pytest_html is not None:
            extra.append(pytest_html.extras.text(
                format_log(log), '%s Log' % name.title()))


'''钩子'''
# @pytest.mark.optionalhook
# def pytest_html_results_table_header(cells):
#     cells.insert(2, html.th('Description'))
#     cells.pop()
# 
# @pytest.mark.optionalhook
# def pytest_html_results_table_row(report, cells):
#     if hasattr(report,"description"):
#         des=report.description
#     else:
#         des="无"
#     cells.insert(2, html.td(des))
#     cells.pop()
                  
def pytest_collection_finish(session):
    print('----pytest_collection_finish--------')
    jkbuildid=session.config.getoption("--jkbuildid")
    jkjobname=session.config.getoption("--jkjobname")
    htmlhead=session.config.getoption("--htmlhead")
    if jkbuildid!=-1 and jkjobname:
        #print('insert test collection to mysql, jobname: {}, buildid: {}'.format(jkjobname,jkbuildid))
        try:
            from localplugins.mysql_opr import query_pymysql
            #print('[session.fspath: {}]'.format(session.fspath))
            fspath=str(session.fspath).replace('\\','\\\\')
            fpath=os.path.join(BASE_DIR,'localplugins','resources', 'mysql_conn.json')
            f=open(fpath, 'r', encoding='utf-8')
            dbinfo = json.loads(f.read())
            sql='''
            INSERT INTO uitest_collect(htmlhead,jk_jobname,jk_buildid,fpath,tests_count)
            VALUES('{0}','{1}','{2}','{3}','{4}')
            '''.format(htmlhead,jkjobname,jkbuildid,fspath,len(session.items))
            query_pymysql(dbinfo['host'],dbinfo['user'],dbinfo['password'],dbinfo['port'],'qateam',sql)
            #print('.......insert test collection to mysql<uitest_collect>......',time.strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            #print('[Exception<inserting to uitest_collect>]',end='')
            print('Exception when inserting test collection to mysql: ',e)
            #print('[Exception<inserting to uitest_collect>: {}]'.format(e),end='')


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    summary = []
    extra = getattr(report, 'extra', [])
    
    driver=None
    if 'app_driver' in item.funcargs:
        driver = item.funcargs['app_driver']
        
    xfail = hasattr(report, 'wasxfail')
    failure = (report.skipped and xfail) or (report.failed and not xfail)
    when = item.config.getini('selenium_capture_debug').lower()
    capture_debug = when == 'always' or (when == 'failure' and failure)
    
    
    if capture_debug:
        exclude = item.config.getini('selenium_exclude_debug').lower()
        if 'logs' not in exclude:
            # gather logs that do not depend on a driver instance
            _gather_driver_log(item, summary, extra)
        #print('--------------driver--------------')
        #print(driver)
        if driver is not None:
            # gather debug that depends on a driver instance
            if 'screenshot' not in exclude:
                _gather_screenshot(item, report, driver, summary, extra)
            #if 'html' not in exclude:
            #    _gather_html(item, report, driver, summary, extra)
            #if 'logs' not in exclude:
            #    _gather_logs(item, report, driver, summary, extra)

    if summary:
        report.sections.append(('pytest-appdriver', '\n'.join(summary)))
    report.extra = extra
    
    jkbuildid=item.config.getoption("--jkbuildid")
    jkjobname=item.config.getoption("--jkjobname")
    if jkbuildid!=-1 and jkjobname:
        try:
            from html import escape
            from localplugins.mysql_opr import query_many_pymysql
            
            fpath=os.path.join(BASE_DIR,'localplugins','resources', 'mysql_conn.json')
            f=open(fpath, 'r', encoding='utf-8')
            dbinfo = json.loads(f.read())
            
            test_log=''
            error_png=''
            error_link=''
            error_html=''
            error_driverlog=''
            test_duration='%.4f' % report.duration
            
            if report.longrepr:
                log1=escape(report.longreprtext)
                log2=log1.replace('\\','\\\\')
                for line in log2.splitlines():
                    separator = line.startswith('_ ' * 10)
                    if separator:
                        test_log+=line[:80]
                    else:
                        exception = line.startswith("E   ")
                        if exception:
                            test_log+='<span class="error">{}</span><br>'.format(line)
                        else:
                            test_log+=line
                    test_log+='<br>'
    
            for section in report.sections:
                header = section[0]
                content = escape(section[1].replace("\\","\\\\"))
                test_log+=' {0} '.format(header).center(80, '-')
                test_log+='<br>'
                #if ANSI:
                #    converter = Ansi2HTMLConverter(inline=False, escaped=False)
                #    content = converter.convert(content, full=False)
                test_log+=content
                
            test_log=test_log.replace("'","\\'")

            if report.extra:
                for o in report.extra:
                    if o['name']=='Screenshot':
                        error_png=o['content']
                    #if o['name']=='HTML':
                    #    error_html=o['content'].replace("'","\\'")
                    if o['name']=='URL':
                        error_link=o['content']
                    #if o['name']=='Driver Log':
                    #    error_driverlog+=o['content']
            
            sql1=''
            sql2=''
            run_phase=getattr(report, 'when', 'call')
            #print('[run_phase:{}, status:{}]'.format(run_phase,report.outcome))
            testcase_name=(' ::').join(report.nodeid.split('::'))
            if run_phase == 'setup':
                if report.outcome=='failed' or report.outcome=='errors':
                    sql1='''
                    INSERT INTO uitest_tests(jk_jobname,jk_buildid,test_name,
                    test_result,test_phase,test_desc,test_duration)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}')
                    '''.format(jkjobname, jkbuildid, testcase_name+' ::setup', 
                               report.outcome, report.when, report.description,test_duration)
                    sql2='''
                    INSERT INTO uitest_tests_errors(jk_jobname,jk_buildid,test_name,test_log,error_png,error_link)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}')
                    '''.format(jkjobname,jkbuildid,testcase_name+' ::setup',test_log, error_png,error_link)
            elif run_phase == 'call':
                if report.outcome=='failed' or report.outcome=='errors':
                    sql1='''
                    INSERT INTO uitest_tests(jk_jobname,jk_buildid,test_name,test_result,
                    test_phase,test_desc,test_duration)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}')
                    '''.format(jkjobname, jkbuildid, testcase_name, report.outcome,
                               report.when, report.description,test_duration)
                    sql2='''
                    INSERT INTO uitest_tests_errors(jk_jobname,jk_buildid,test_name,test_log,error_png,error_link)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}')
                    '''.format(jkjobname,jkbuildid,testcase_name,test_log, error_png,error_link)
                else:
                    sql1='''
                    INSERT INTO uitest_tests(jk_jobname,jk_buildid,test_name,test_result,
                    test_phase,test_desc,test_duration,test_log)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')
                    '''.format(jkjobname, jkbuildid, testcase_name, report.outcome,
                               report.when, report.description,test_duration,test_log)
            elif run_phase == 'teardown':
                if report.outcome=='failed' or report.outcome=='errors':
                    sql1='''
                    INSERT INTO uitest_tests(jk_jobname,jk_buildid,test_name,
                    test_result,test_phase,test_desc,test_duration)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}')
                    '''.format(jkjobname, jkbuildid, testcase_name+' ::tearDown', 
                               report.outcome, report.when, report.description, test_duration)
                    sql2='''
                    INSERT INTO uitest_tests_errors(jk_jobname,jk_buildid,test_name,test_log,error_png,error_link)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}')
                    '''.format(jkjobname,jkbuildid,testcase_name+' ::tearDown',test_log, error_png,error_link)
            query_many_pymysql(dbinfo['host'],dbinfo['user'],dbinfo['password'],dbinfo['port'],'qateam',sql1,sql2)
        except Exception as e:
            #print('[Exception<inserting to uitest_tests>]',end='')
            print('[Exception<inserting to uitest_tests>: {}]'.format(e),end='')
    
    
    



            
# def _gather_driver_log(item, summary, extra):
#     pytest_html = item.config.pluginmanager.getplugin("html")
#     if hasattr(item.config, "_driver_log") and \
#        os.path.exists(item.config._driver_log):
#         if pytest_html is not None:
#             with io.open(item.config._driver_log, "r", encoding="utf8") as f:
#                 extra.append(pytest_html.extras.text(f.read(), "Driver Log"))
#             summary.append("Driver log: {0}".format(item.config._driver_log))
#             
# def _gather_screenshot(item, report, driver, summary, extra):
#     try:
#         #print("get_screenshot_as_base64")
#         pre_context=driver.current_context
#         if pre_context!="NATIVE_APP":
#             driver.switch_to.context("NATIVE_APP")
#         screenshot = driver.get_screenshot_as_base64()
#         if pre_context!="NATIVE_APP":
#             driver.switch_to.context(pre_context)
#         #print(screenshot)
#     except Exception as e:
#         summary.append("WARNING: Failed to gather screenshot: {0}".format(e))
#         return
#     pytest_html = item.config.pluginmanager.getplugin("html")
#     if pytest_html is not None:
#         # add screenshot to the html report
#         extra.append(pytest_html.extras.image(screenshot, "Screenshot"))
# 
# def _gather_html(item, report, driver, summary, extra):
#     try:
#         html = driver.page_source
#     except Exception as e:
#         summary.append("WARNING: Failed to gather HTML: {0}".format(e))
#         return
#     pytest_html = item.config.pluginmanager.getplugin("html")
#     if pytest_html is not None:
#         # add page source to the html report
#         extra.append(pytest_html.extras.text(html, "HTML"))
# 
# def format_log(log):
#     timestamp_format = "%Y-%m-%d %H:%M:%S.%f"
#     entries = [u"{0} {1[level]} - {1[message]}".format(
#         datetime.utcfromtimestamp(entry["timestamp"] / 1000.0).strftime(
#             timestamp_format), entry).rstrip() for entry in log]
#     log = "\n".join(entries)
#     return log
# 
# def _gather_logs(item, report, driver, summary, extra):
#     pytest_html = item.config.pluginmanager.getplugin("html")
#     try:
#         types = driver.log_types
#     except Exception as e:
#         # note that some drivers may not implement log types
#         summary.append("WARNING: Failed to gather log types: {0}".format(e))
#         return
#     for name in types:
#         try:
#             log = driver.get_log(name)
#         except Exception as e:
#             summary.append("WARNING: Failed to gather {0} log: {1}".format(
#                 name, e))
#             return
#         if pytest_html is not None:
#             extra.append(pytest_html.extras.text(
#                 format_log(log), "%s Log" % name.title()))
# 
# 
# @pytest.mark.optionalhook
# def pytest_html_results_table_header(cells):
#     cells.insert(2, html.th("Description"))
#     cells.pop()
# 
# @pytest.mark.optionalhook
# def pytest_html_results_table_row(report, cells):
#     if hasattr(report,"description"):
#         des=report.description
#     else:
#         des="无"
#     cells.insert(2, html.td(des))
#     cells.pop()
# 
#                    
# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item, call):
# 
#     outcome = yield
#     report = outcome.get_result()
#     report.description = str(item.function.__doc__)
#     summary = []
#     extra = getattr(report, "extra", [])
#     
#     driver=None
#     if "app_driver" in item.funcargs:
#         driver = item.funcargs["app_driver"]
#         
#     xfail = hasattr(report, "wasxfail")
#     failure = (report.skipped and xfail) or (report.failed and not xfail)
#     when = item.config.getini("selenium_capture_debug").lower()
#     capture_debug = when == "always" or (when == "failure" and failure)
#     
#     
#     if capture_debug:
#         exclude = item.config.getini("selenium_exclude_debug").lower()
#         if "logs" not in exclude:
#             # gather logs that do not depend on a driver instance
#             _gather_driver_log(item, summary, extra)
#         #print("--------------driver--------------")
#         #print(driver)
#         if driver is not None:
#             # gather debug that depends on a driver instance
#             if "screenshot" not in exclude:
#                 _gather_screenshot(item, report, driver, summary, extra)
#             #if "html" not in exclude:
#             #    _gather_html(item, report, driver, summary, extra)
#             #if "logs" not in exclude:
#             #    _gather_logs(item, report, driver, summary, extra)
# 
#     if summary:
#         report.sections.append(("pytest-appdriver", "\n".join(summary)))
#     report.extra = extra
