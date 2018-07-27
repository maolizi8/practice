'''
Created on 2017年7月12日

@author: geqiuli
'''
import logging
import os
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import time

def send_mail(file_new,mail_to):
    with open(file_new,'rb') as f:
        mail_body = f.read()
    
    users=""
    with open(mail_to,'r') as f:
        for line in f.readlines():
            users+=line.strip()+";"
        
    timestamp=time.strftime('%Y-%m-%d')    
    mail_info = {
        "from": "uiautomationreport@111.com.cn",
        "to": users,
        "mail_subject": "【UI自动化测试报告  "+timestamp+'】',
        "mail_encoding": "utf-8"
    }
    msg = MIMEText(mail_body, "html", mail_info["mail_encoding"])
    msg["Subject"] = Header(mail_info["mail_subject"], mail_info["mail_encoding"])
    msg["From"] = mail_info["from"]
    msg["To"] = mail_info["to"] 
    
    smtp = smtplib.SMTP()
    smtp.connect("10.6.8.16")
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()
    print('email has send out !')
    
def log_config(logFile):
    logging.basicConfig(level=logging.INFO,  
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%m-%d %H:%M',  
                        filename=logFile,  
                        filemode='w')  
     
    console = logging.StreamHandler()  
    # console.setLevel(logging.DEBUG) 
    console.setLevel(logging.INFO) 
    formatter = logging.Formatter('%(message)s')  
    console.setFormatter(formatter)  
    logging.getLogger('').addHandler(console)

def get_new_report(report_dir):
    lists = os.listdir(report_dir)
    lists.sort(key=lambda fn:os.path.getmtime(os.path.join(report_dir,fn)))
    file_new = os.path.join(report_dir,lists[-1])
    print(file_new)
    return file_new

if __name__=='__main__':
    d=os.path.abspath(os.path.join('..','Reports'))
    get_new_report(d)