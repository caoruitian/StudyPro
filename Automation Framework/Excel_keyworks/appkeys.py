 #-*- coding: UTF-8 -*-
from appium import webdriver
from common import logger
from appium.webdriver.common.touch_action import TouchAction
import os,threading,time

class APP:

    def __init__(self,writer):
        #打开app的对象
        self.driver = None
        #写入excel执行结果
        self.writer = writer
        #保存参数
        self.params = {}
        #保存appium端口
        self.port = ''
        os.system('chcp 65001')


    def runappium(self,path,port,choose):

        if port != '':
            self.port = port
        else:
            self.port = '4723'

        self.portOccupancy(self.port)

        #启动appium
        logger.info('appium启动中...')
        if choose == 'command'or choose == '':
            self.__commandappium(path +  '\\AppData\\Local\\Programs\\Appium',port)
        elif choose == 'windows':
            self.__windowsappium(path +  '\\AppData\\Local\\Programs\\Appium',port)
        else:
            logger.error('输入参数command或者windows选择打开appium的方式')
            return


    # 查看端口是否被占用
    def portOccupancy(self,port):
        cmd = 'netstat -aon | findstr ' + port + '| findstr LISTENING'
        # res=0,端口被占用；res=1，端口未被占用
        res = str(self.__run(cmd))
        if res == '1':
            logger.info('端口未被占用')
        elif res == '0':
            self.close(self.port)


    def close(self,port):

        if port == '':
            port = self.port

        cmd = 'netstat -aon | findstr ' + port + '| findstr LISTENING'
        try:
            res = os.popen(cmd).read().split()
            logger.info('端口被占用,结束端口进程: ' + res[-1])
            os.system('taskkill /F /im ' + res[-1])
        except Exception as e:
            logger.exception(e)


    #调用命令行appium
    def __commandappium(self,path,port):
        cmd = 'node ' + path + '\\resources\\app\\node_modules\\appium\\build\\lib\\main.js --address 127.0.0.1 -p ' + port
        th = threading.Thread(target=self.__run, args=(cmd,))
        th.start()
        time.sleep(5)


    #调用窗口appium
    def __windowsappium(self,path,port):
        # cmd = 'cmd /c start node ' + path + '\\resources\\app\\node_modules\\appium\\build\\lib\\main.js --address 127.0.0.1 -p ' + port
        cmd = 'cmd /c start node ' + path + '\\resources\\app\\node_modules\\appium\\build\\lib\\main.js -p ' + port
        os.system(cmd)


    #多线程函数，用来执行cmd命令
    def __run(self,cmd):
        res = os.system(cmd)
        return res


    def __time(self, t):
        try:
            t = int(t)
            if t < 0:
                t = 10
                logger.exception('时间不能为负数，默认等待10秒')
        except:
            t = 10
            logger.exception('时间参数有误，默认等待10秒')
        return t


    def runapp(self, c, t):

        conf = {
            'platformName': 'Android',
            'platformVersion': '6.0.1',
            'deviceName': '127.0.0.1:7555',
            'appPackage': 'com.Glaciwaker.SmithStory',
            'appActivity': 'com.unity3d.player.UnityPlayerActivity',
            'noReset': 'true',
        }

        try:
            c = eval(c)
            for key in c:
                conf[key] = c[key]
        except Exception as e:
            logger.warn('app配置错误，请检查')
            logger.exception(e)

        #多个设备需要指定连接设备
        conf['udid'] = conf['deviceName']
        #确保设备是连上的
        try:
            os.system('adb connect ' + conf['deviceName'])
            os.system('adb devices')
        except:
            pass

        #连接appium并且启动app
        self.driver = webdriver.Remote('http://localhost:' + self.port + '/wd/hub', conf)
        # self.driver = webdriver.Remote('http://127.0.0.1:4777/wd/hub', conf)
        #隐式等待
        self.wait(t)
        return self.driver

    # 强行等待
    def sleep(self,t):
        t = self.__time(t)  # 处理时间参数
        time.sleep(t)

    #隐式等待
    def wait(self,t):
        t = self.__time(t)#处理时间参数
        self.driver.implicitly_wait(t)

    def __driver(self,path):
        if ':id' in path:
            logger.info('by id')
            driver = self.driver.find_element_by_id(path)
        elif path[0] == '/' :
            logger.info('by xpath')
            driver = self.driver.find_element_by_xpath(path)
        else:
            logger.info('by accessibility_id')
            driver = self.driver.find_element_by_accessibility_id(path)
        return  driver

    def click(self,path):
        driver = self.__driver(path)
        driver.click()

    def sendkeys(self,path,value):
        driver = self.__driver(path)
        driver.send_keys(value)

    def swipe(self,p1,p2):
        try:
            x1 = p1.split(',')[0]
            y1 = p1.split(',')[1]
            x2 = p2.split(',')[0]
            y2 = p2.split(',')[1]
            TouchAction(self.driver).press(x=x1, y=y1).move_to(x=x2, y=y2).release().perform()
        except Exception as e:
            logger.exception(e)

if __name__ == '__main__':
#     conf = {
#     "platformName": "Android",
#     "platformVersion": "6.0.1",
#     "deviceName": "127.0.0.1:7555",
#     "appPackage": "com.Glaciwaker.SmithStory",
#     "appActivity": "com.unity3d.player.UnityPlayerActivity",
#     "noReset": "true",
# }

    conf = {
    "platformName": "Android",
    "platformVersion": "6.0.1",
    "deviceName": "127.0.0.1:7555",
    "appPackage": "com.tencent.mm",
    "appActivity": "ui.LauncherUI",
    "noReset": "true",
    "unicodeKeyboard": "true",
    "resetKeyboard": "true"
    }
    path = 'C:\\Users\\Administrator'
    app = APP(None)
    app.runappium(path,'4779','command')
    app.runapp(conf,'15')

 # 'unicodeKeyboard': 'ture',
 # 'resrKeybord': 'true'

