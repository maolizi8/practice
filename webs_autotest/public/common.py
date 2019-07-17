'''
Created on 2017年8月5日

@author: gql
'''
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
import configparser
from conftest import root_dir

def mailSend(mail):
    inifile=root_dir+'conf.ini'
    config = configparser.ConfigParser()
    config.readfp(open(inifile, 'r',encoding='utf-8'))
    username=config.get("smtp", "username")
    password=config.get("smtp", "password")
    mail_info = {
        "from": username,
        "to": username,
        "hostname": "smtp.qq.com",
        "username": username,
        "password": password,
        "mail_subject": "send mails automatically",
        "mail_encoding": "utf-8"
    }
    smtp = SMTP_SSL(mail_info["hostname"])
    smtp.set_debuglevel(1)
    
    smtp.ehlo(mail_info["hostname"])
    smtp.login(mail_info["username"], mail_info["password"])

    msg = MIMEText(mail, "html", mail_info["mail_encoding"])
    msg["Subject"] = Header(mail_info["mail_subject"], mail_info["mail_encoding"])
    msg["from"] = mail_info["from"]
    msg["to"] = mail_info["to"]   
    smtp.sendmail(mail_info["from"], mail_info["to"], msg.as_string())
    smtp.quit()
    
if __name__ == '__main__':
    pass