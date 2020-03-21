# a = ['a','1']
# b = ['b','2']
# c = {}
# c[a[0]] = a[1]
# print(c)
# c[b[0]] = b[1]
# print(c)

import json,jsonpath,requests
from  common import logger


# session = requests.session()
# ss = session.post('http://192.168.1.104:8080/inter/HTTP/auth')
# s = ss.text
# # s ='/**/jQuery11020890783716143493_1563978476869({"status":"0","t":"1563979251548","set_cache_time":"","data":[{"location":"澳大利亚","titlecont":"IP地址查询","origip":"1.1.1.1","origipquery":"1.1.1.1","showlamp":"1","showLikeShare":1,"shareImage":1,"ExtendedLocation":"","OriginQuery":"1.1.1.1","tplt":"ip","resourceid":"6006","fetchkey":"1.1.1.1","appinfo":"","role_id":0,"disp_type":0}]});'
# s = s[s.find('{'):s.rfind('}')+1]
# #
# #
# res = json.loads(s)
# print(s)
# print(jsonpath.jsonpath(res,'$.status')[0])



# #知乎login
# session = requests.session()
#
# session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
# session.headers['Content-Type'] ='application/x-www-form-urlencoded'
#
# # print(session.cookies)
# udid = session.post('https://www.zhihu.com/udid',data=None)
# print(udid.text)
# # print(session.cookies)
#
# y = session.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=cn')
# print(y.text)
#
# session.headers['x-zse-83'] ='3_2.0'
#
# # print(session.headers)
# # print(session.cookies)
# # aa = session.post('https://www.zhihu.com/api/v3/oauth/sign_in')
# # print(aa)
# ss = session.post('https://www.zhihu.com/api/v3/oauth/sign_in',data='aXt924U0gLNY-qNMmvcmErS0cT2tEgNmqgSMxU9qkLk9-qNZsUO1iugZoGVVxhYq8Ln9k4U0gXLxcTYhBupGeheVkCN_evx9BLfBFUCG-qVGNCNMMTYhXg9hgqxOcvSMccxGcrU0g6SYXqYhqbO8ArU0g7t_Jgp9BLf8igXGQwOfSTYhK0F0rHCmD9pOt9e0z_NM-ccM2wNOSTYhpvS8EACMQ_2pkLP0BT20ei9yQ0Fm2LfBpwNmkveMcBtxgLYymMY0Q4H8NGFXkXO8hwtqNgX0cTYpe0x0h9FBNb98b7YxkM20BLt924_BkC3VUbSBtq3qk478gGpucUO1PD3ZJCe8Xq2tgqNMsvSMS79hb72peMFqK7YqeQ9qr_LxgRVmZ9oMgGL1eBtxg_NMwGoM2JXMXq2tguVKKvwGEJHM3BtxgRF0zuFqrH9BrXxpggY8BTxyNguq6X2fS828G8OBFgr8Xq2tHgSVKbOBDBe8')
# print(ss.text)
#
# l = session.get('https://www.zhihu.com/logout')
# print(l.text)
#
#
#
# d = 'username=Crtims123&password=1234%$6'
# if 'username' in d:
#     print(d)
#
# d = {'a':'b'}
# if isinstance(d,dict):
#     print('1')
#
# s = 'adadadadad'
# l = s.split('&')
# print(l)