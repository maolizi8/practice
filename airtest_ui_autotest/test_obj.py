'''
Created on 2019年7月19日

@author: geqiuli
'''
from airtest.cli.runner import AirtestCase, run_script
from argparse import *
import airtest.report.report as report
import jinja2
import shutil
import os
import io
 
 
class CustomAirtestCase(AirtestCase):
    def setUp(self):
        print("custom setup")
        # add var/function/class/.. to globals
        # self.scope["hunter"] = "i am hunter"
        # self.scope["add"] = lambda x: x+1
 
        # exec setup script
        # self.exec_other_script("setup.owl")
        super(CustomAirtestCase, self).setUp()
 
    def tearDown(self):
        print("custom tearDown")
        # exec teardown script
        # self.exec_other_script("teardown.owl")
        super(CustomAirtestCase, self).setUp()
 
    def run_air(self, root_dir, device):
        # 聚合结果
        results = []
        # 获取所有用例集
        root_log = root_dir + '\\' + 'log'
        if os.path.isdir(root_log):
            print('log folder is exist')
            #shutil.rmtree(root_log)
        else:
            os.makedirs(root_log)
            print(str(root_log) + 'is created')
        
        print('')
        for f in os.listdir(root_dir):
            print('root_dir > f:',f)
            if f.endswith(".air"):
                # f为.air案例名称：手机银行.air
                print('test file:',f)
                airName = f
                script = os.path.join(root_dir, f)
                # airName_path为.air的全路径：D:\tools\airtestCase\案例集\log\手机银行
                print('script:',script)
                # 日志存放路径和名称：D:\tools\airtestCase\案例集\log\手机银行1
                log = os.path.join(root_dir, 'log' + '\\' + airName.replace('.air', ''))
                print('log：',log)
                if os.path.isdir(log):
                    print('log： if exist ')
                    #shutil.rmtree(log)
                else:
                    os.makedirs(log)
                    print(str(log) + ' is created')
                log_file=log+'\\log.txt'
                if not os.path.exists(log_file):
                    ff = open(log_file,'w')
                    print('create log file: ',ff)
                    ff.close()
                else:
                    print(log_file + " already existed.")
                output_file = log + '\\' + 'log.html'
                args = Namespace(device=device, log=log, recording=None, script=script)
                try:
                    print('运行脚本开始')
                    run_script(args, AirtestCase)
                    print('运行脚本结束')
                except Exception as e:
                    print('运行失败，',e)
                finally:
                    try:
                        print('生成报告')
                        rpt = report.LogToHtml(script_root=root_dir, log_root=log, script_name=script)
                        print('output_file:',output_file)
                        rpt.report("log_template.html", output_file=output_file)
                        result = {}
                        result["name"] = airName.replace('.air', '')
                        result["result"] = rpt.test_result
                        results.append(result)
                    except Exception as e:
                        print('运行失败，暂时不抛异常，',e)
                    
        
        print('生成聚合报告')
        # 生成聚合报告
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(root_dir),
            extensions=(),
            autoescape=True
        )
        template = env.get_template("summary_template.html", root_dir)
        html = template.render({"results": results})
        output_file = os.path.join(root_dir, "summary.html")
        with io.open(output_file, 'w', encoding="utf-8") as f:
            f.write(html)
        print('output_file:',output_file)
 
 
if __name__ == '__main__':
    test = CustomAirtestCase()
    device = ['android:///']
    test.run_air('E:\\mypython\\airtest_ui_autotest', device)
