'''
Created on 10 May 2019

@author: geqiuli
'''
from email.mime.text import MIMEText
from email.header import Header
import smtplib
from public import files
from public import mysql_opr

def send_mail(subject, content, to_users):
    '''
    @param to_users: list eg.['aaa@xx.com','aaa@xx.com']
    '''
    #account = files.read_txt('local_account','yw_local')
    #sender = account[0]+'@111.com.cn'
    query='SELECT * FROM smtp_config ORDER BY id DESC LIMIT 1'
    conn=mysql_opr.get_connection('serverip', 'port', 'db_name', 'account', 'password')
    rsp_data=mysql_opr.select_from_mysql(conn,query,1)
    if rsp_data['code']!=0:
        raise Exception('查询邮件发送者出现异常：'+rsp_data['msg'])
    account = rsp_data['data']
    sender = account['sender_name']+account['sender_suffix']
    
    print('sender:', sender)
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = ','.join(to_users)
    #msg['To'] = to_users
    # msg['Cc'] = cc_user

    server = smtplib.SMTP()
    # server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
    # server.set_debuglevel(1)
    server.connect("smtp.exmail.qq.com")    #此处以腾讯企业邮箱为例
    server.starttls()
    server.login(sender, account['sender_pwd'])
    print('邮箱登录成功')

    senders = server.sendmail(sender, to_users, msg.as_string())
    print(senders)
    server.quit()
    return True

if __name__ == '__main__':
    pass