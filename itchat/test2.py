#coding:utf-8
import itchat
#登录微信
#itchat.auto_login(enableCmdQR=-1)#enableCmdQR在终端或命令行中为True,在notebook中为-1
itchat.auto_login(hotReload=True)

def sendMessageToWechat(markName=u'张三',message=u'已经处理完毕'):
    '''
    markName: 微信备注的名字
    message: 要发送的内容
    eg: sendMessageToWechat(markName=u'鹏举',message=u'已经处理完毕')
    '''    
    #想给谁发信息，先查找到这个朋友    
    users = itchat.search_friends(name=markName)
    if users:        
        #找到UserName
        userName = users[0]['UserName']
        itchat.send(message,toUserName = userName)
	print userName
	print("发送成功...., userName : %s"%(str(userName)))
    else:
        print('通讯录中无此人')


from time import sleep


def func1():        
    sleep(2)
def func2():
    sleep(2)

func1()
sendMessageToWechat(markName=u'张三',message=u'func1已经处理完毕')
func2()
sendMessageToWechat(markName=u'曹静',message=u'test...')

### 问题 ： 只有扫码的登录时，才能发送成功
