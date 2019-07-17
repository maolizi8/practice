'''
Created on 2017年7月27日

@author: geqiuli
'''
import pytest
from py.xml import html,raw #html的错误提示请忽略
import os
import json
import time
from localplugins.simplehtml import HTMLReport
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

DesiredCapabilities.INTERNETEXPLORER['ignoreProtectedModeSettings'] = True

projname='webs_autotest'
root_dir=os.path.abspath('conftest.py').split(projname)[0]+projname+os.sep
#print('conftest - root_dir :',root_dir)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print('conftest - BASE_DIR :',BASE_DIR)


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

@pytest.fixture
def selenium(selenium):
    print('脚本运行的浏览器：',selenium.name)
    if selenium.name!='internet explorer':
        selenium.implicitly_wait(30)
    print('浏览器版本：',selenium.capabilities['version'])
    selenium.maximize_window()
    selenium.set_page_load_timeout(30)  #页面加载时间限制，防止部分js加载时间过长，页面一直等待
    return selenium

@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('--start-maximized')
    prefs= {
        "profile.managed_default_content_settings.images":1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player":1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player":1,
        "credentials_enable_service":False,
        "profile.password_manager_enabled":False
        }
    chrome_options.add_experimental_option('prefs', prefs)
    return chrome_options

'''钩子'''
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

# @pytest.mark.optionalhook
# def pytest_html_results_table_header(cells):
#     cells.insert(1, html.th('用例功能描述'))
#     cells.pop()
# 
# @pytest.mark.optionalhook
# def pytest_html_results_table_row(report, cells):
#     
#     if hasattr(report,"description"):
#         des=report.description
#     else:
#         des="无"
#     cells.insert(1, html.td(des))
#     cells.pop()

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    #print('report.__dict__: ',report.__dict__)
    #print('item.__dict__: ',item.__dict__)
    #print('outcome.__dict__: ',outcome.__dict__)
    #print()
    #print(report.nodeid)
    #print('longrepr: ',report.longrepr)
    #print('sections: ',report.sections)
    #print()
    
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
        


'''
增加命令行参数
'''
def pytest_addoption(parser):
    '''命令行参数'''
    group = parser.getgroup('terminal reporting')
    group.addoption('--htmlhead', action='store', dest='htmlhead',default='测试报告',
                    help='the head of html report.')
    group.addoption('--simple-html', action='store_true',
                    help='use simple html moudle.')
    group.addoption('--jkbuildid', action='store',default=-1,
                    help='jenkins buildid, to make online html report.')
    group.addoption('--jkjobname', action='store',
                    help='jenkins jobname, to make online html report.')
    
    parser.addoption("--uname", action="store", default="testzdauto01",
        help="The username to login webs")
    parser.addoption("--password", action="store",
        help="The password to login webs")
    
    parser.addoption("--mailreceiver", action="store",default="qm_dept@111.com.cn",
        help="用于邮件的接收者")
    
    parser.addoption("--exc_env", action="store", default='prd',
        help="脚本运行的环境，prd-线上，pre-预发布，test-测试。默认prd")
    
     

@pytest.fixture
def account(request):
    '''命令行输入username，读取账号密码'''
    username=request.config.getoption("--uname")
    password=request.config.getoption("--password")
    if password:
        print('use specific password')
        return {"name": username,"password": password}
    else:
        print('use stored password from file')
        user_account=read_json('account','account')
        for user in user_account:
            if username == user['name']:
                return user

@pytest.fixture
def exc_env(request):
    '''参数 exc_env,运行环境，prd-线上，pre-预发布，test-测试。默认prd'''
    return request.config.getoption("--exc_env")


@pytest.fixture
def mailreceiver(request):
    '''用于邮件的接收者'''
    receiver=request.config.getoption("--mailreceiver")
    mailreceiver=receiver.split(",")
    return mailreceiver
