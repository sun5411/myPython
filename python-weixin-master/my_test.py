#coding:utf-8
from weixin import WXAPPAPI

api = WXAPPAPI(appid=APP_ID,
                  app_secret=APP_SECRET)
session_info = api.exchange_code_for_session_key(code=code)

# 获取session_info 后

session_key = session_info.get('session_key')
crypt = WXBizDataCrypt(WXAPP_APPID, session_key)

# encrypted_data 包括敏感数据在内的完整用户信息的加密数据
# iv 加密算法的初始向量
# 这两个参数需要js获取
user_info = crypt.decrypt(encrypted_data, iv)
