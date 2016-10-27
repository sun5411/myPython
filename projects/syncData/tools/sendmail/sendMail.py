#!/usr/bin/env python
#coding:utf-8

'''
Send mail with txt format
Author : Sun Ning
'''
import mailconf
import smtplib
from email.MIMEText import MIMEText

_to=mailconf.mailto_list
_host=mailconf.mail_host
_user=mailconf.mail_user
_pass=mailconf.mail_pass
_cc=mailconf.cc_list

def send_mail(sub,content):
    msg = MIMEText(content,_charset="utf-8")
    msg['Subject'] = sub
    msg['From'] = _user
    msg['To'] = ";".join(_to)
    msg['Cc'] = ";".join(_cc)
    emails = _to + _cc
    try:
        server = smtplib.SMTP()
        server.connect(_host)
        server.login(_user,_pass)
        #server.sendmail(_user,_to,msg.as_string())
        server.sendmail(_user,emails,msg.as_string())
        server.close()
        return True
    except Exception,e:
        print str(e)
        return False

if __name__ == '__main__':
    if send_mail("hello","hello world!"):
        print "Send Successed !"
    else:
        print "Send Failed !"
