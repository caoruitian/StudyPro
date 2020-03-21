# import xlrd

# data = xlrd.open_workbook(r'../lib/Mytest_HTTP接口用例.xlsx')
# print(data)
#
#
# sheet = data.sheet_names()
# print(sheet)
#
# sheet1 = data.sheet_by_index(0)
# print(sheet1)
# sheet2 = data.sheet_by_name('授权接口')
# print(sheet2)
# sheet3 = data.sheets()[0]
# print(sheet3)
#
# print(sheet1.nrows)
# print(sheet2.ncols)
#
# print(sheet1.row_values(0))
# print(sheet2.col_values(1))
#
# print(sheet2.row_values(1)[0])


# class Read():
#     def __init__(self):
#         self.data = None
#         self.sheet = None
#         self.rows = 0
#         self.line = 0
#
#     def get_sheet(self):
#         self.sheet = self.data.sheet_by_index(0)
#
#     def open_workbook(self,path):
#         self.data = xlrd.open_workbook(path)
#
#     def get_rows(self):
#         self.rows = self.sheet.nrows
#         return self.rows
#
#     def get_row_value(self,l):
#         self.line = self.sheet.row_values(l)
#         return self.line

# if __name__ == '__main__':
#
#     # data = xlrd.open_workbook(r'../lib/Mytest_HTTP接口用例.xlsx')
#     # sheet1 = data.sheet_by_index(0)
#     # for i in range(sheet1.nrows):
#     #     print(sheet1.row_values(i))
#     read = Read()
#     read.open_workbook(r'../lib/Mytest_HTTP接口用例.xlsx')
#     read.get_sheet()
#     for i in range(read.get_rows()):
#         print(read.get_row_value(i))



# from  Excel_keyworks.httpkeys import HTTP
# import inspect



# a = 'post'
# http = HTTP()
#
#
#
# def test():
#     # getattr(http,a) = http.post
#     # getattr(http,a)() = http.post()
#     # func() = http.post()
#     func = getattr(http,a)
#     print(func)
#     print(http.post)
#
#     #相当于args = inspect.getfullargspec(http.post).__str__()
#     #获取参数
#     args = inspect.getfullargspec(func).__str__()
#     print(args)
#     #字符串截取
#     args = args[args.find('args=')+5:args.find(', varargs')]
#     print(args)
#     #截取后还是字符串，所以要处理成列表
#     args = eval(args)
#     print(args)
#     args.remove('self')
#     print(args)
#     print(len(args))
#     #查看方法描述
#     print(func.__doc__)
#
#
#
#
#
# a = ['' , '' , '没有字段' , 'post' , 'http://112.74.191.10:8081/inter/HTTP/auth' , '' , '' , '' , '']
# http = HTTP()
# func = getattr(http,a[3])
#
#
# args = inspect.getfullargspec(func).__str__()
# args = args[args.find('args=') + 5:args.find(', varargs')]
# args = eval(args)
# args.remove('self')
# print(args)
# l = len(args)
#
# if l < 1:
#     func()
#
# if l < 2:
#     func(a[4])
#
# if l < 3:
#     func(a[4],a[5])



from suds.client import Client
from suds.xsd.doctor import ImportDoctor,Import #命名空间设置
import json


# # url = 'http://www.webxml.com.cn/WebServices/WeatherWebService.asmx?wsdl'#天气预告
# url = 'http://192.168.1.104:8080/inter/SOAP?wsdl'#课程接口
# XLMSchema = 'http://www.w3.org/2001/XMLSchema'#一般为固定值
# locations = 'http://www.w3.org/2001/XMLSchema.xsd'#一般为固定值
# targetNamespace = 'http://WebXml.com.cn/'#命名空间，用于查找接口的位置，非固定
#
# #添加默认的XLMSchema
# imp = Import(XLMSchema,location=locations)
# #添加命名空间
# imp.filter.add(targetNamespace)
# doctors = ImportDoctor(imp)
#
# #用来发送webservice请求的对象，相当于driver
# #url是wsd文档的全路径
# client = Client(url,doctor=doctors)
# # res = client.service.getWeatherbyCityName('长沙')#天气预告
# res = client.service.auth()#课程接口
# print(res)
#
# res = json.loads(res)
# print(res)
#
# header = {}
# header['token'] = res['token']
# client = Client(url,doctor=doctors,headers=header)
#
# m = 'login'
# res = client.service.__getattr__(m)('Crtims123','123456')
# # res = client.service.login('Crtims123','123456')
# print(res)
#
# res = client.service.logout()
# print(res)

###################################################################
# from Excel_keyworks.soapkeys import SOAP
#
# s = SOAP()
# s.adddoctor('')
# s.setwsdl('http://192.168.1.104:8080/inter/SOAP?wsdl')
# s.callmethod('auth')
# s.savejson('token','token')
# s.addheader('token','{token}')
# s.callmethod('login','Crtims123、123456')
# s.callmethod('logout')

#######################################################################
 #-*- coding: UTF-8 -*-
# import os,threading
#
# #调用cmd命令
# cmd = 'node C:\\Users\\Administrator\\AppData\\Local\\Programs\\Appium\\resources\\app\\node_modules\\appium\\build\\lib\\main.js -p 4777'
# # os.system(cmd)
#
#
# def run(cmd):
#     res = os.system(cmd)
#     print('子线程')
#     return res
#
# #创建一个程来执行函数
# th = threading.Thread(target=run, args=(cmd,))
# #开始执行子线程
# th.start()
# print('主线程')

###################################################################
import os



# class Appium:
#
#     def __init__(self):
#         pass
#
#     def openappium(self,port,path):
#         try:
#             os.system('taskkill /f /im node.exe')
#         except Exception as e:
#             print(e).encoding('utf-8')
#
#         #处理端口被占用
#         p = os.popen(f'netstat  -aon|findstr ' + port)
#         print(p)
#         p0 = p.read().strip()
#         print(p0)
#         if p0 != '' and 'LISTENING' in p0:
#             print('检查该端口被占用，结束进程')
#             p1 = p0.split()[4]  # 获取进程号
#             print(p1)
#             os.popen(f'taskkill /F /PID ' + p1)  # 结束进程
#             print('端口已结束')
#
#         print('启动appium')
#         #单独启动appium
#         # cmd =  'cmd /c start node '+ path + '\\resources\\app\\node_modules\\appium\\build\\lib\\main.js --address 127.0.0.1 -p ' + port
#         #命令行启动appium
#         cmd = 'node ' + path + '\\resources\\app\\node_modules\\appium\\build\\lib\\main.js --address 127.0.0.1 -p ' + port
#         os.system(cmd)
#
# path = 'C:\\Users\\Administrator\\AppData\\Local\\Programs\\Appium'
# appium = Appium()
# appium.openappium('4723',path)

# {
#     "platformName": "Android",
#     "platformVersion": "6.0.1",
#     "deviceName": "127.0.0.1:7555",
#     "appPackage": "com.tencent.mm",
#     "appActivity": "ui.LauncherUI",
#     "noReset": "true",
#     "unicodeKeyboard": "true",
#     "resetKeyboard": "true"
#     }




# from selenium import webdriver
# option = webdriver.ChromeOptions()
# option.add_argument('disable-infobars')
# driver = webdriver.Chrome(executable_path='../lib/driver/chromedriver',options=option) # # 打开chrome浏览器
# driver.get('https://www.baidu.com/')
# driver.implicitly_wait(5)
# driver.find_element_by_xpath('//*[@id="kw"]').send_keys('大肥猫')
# driver.implicitly_wait(5)
# driver.find_element_by_css_selector('#su').click()
# print(driver.title)


import requests,json,jsonpath

parame = {}
session = requests.session()



def getparame(p):
    global parame
    # logger.debug(p)
    # logger.debug(self.parame)
    for key in parame:
        # logger.debug(key)
        p = p.replace('{' + key + '}', parame[key])
        # logger.debug('p:',p)
    return p

def addheader(key, value):
    p = getparame(value)
    session.headers[key] = p


def getjsonpaths(url):
    result = session.post(url)
    res = result.text
    print('====result.text====')
    print(res)

    #将json字符串res转换为字典
    jsoners = json.loads(res)
    print('====jsoners====')
    print(jsoners)


    print('====jsonpaths====')
    jsonpaths = str(jsonpath.jsonpath(jsoners,'token')[0])
    print(jsonpaths)
    return jsonpaths





print(session.headers)
addheader('token','5c4e6acab39e4072814e2af85bb300aa')
print(session.headers)
jsoners = getjsonpaths('http://192.168.1.104:8080/inter/HTTP/auth')
parame['token'] = jsoners
print('parame =' + parame['token'])


addheader('token','{token}')
print(session.headers)
result = session.post('http://192.168.1.104:8080/inter/HTTP/auth')
print(result.text)
