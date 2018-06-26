import itchat
#coding:utf-8

@itchat.msg_register(itchat.content.TEXT)
def test_reply(msg):
        itchat.send(msg['Text'],msg['FromUserName'])

itchat.auto_login()
itchat.run()

