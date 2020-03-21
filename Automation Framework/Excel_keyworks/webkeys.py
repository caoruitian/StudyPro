from selenium import webdriver
from common import logger
from selenium.webdriver.common.action_chains import ActionChains
import os,time


class WEB:

    def __init__(self):
        self.driver = None
        #保存窗口id
        self.handles = []

    def openbrowser(self, browser):
        if browser == 'google':
            # 解决浏览器加载慢的问题
            option = webdriver.ChromeOptions()
            # 去掉提示条配置
            option.add_argument('disable-infobars')
            # 加快浏览速度，获取本机用户路径
            userdir = os.environ['USERPROFILE']
            userdir = 'user-data-dir=' + userdir + '\\AppData\\Local\\Google\\User Data'
            # 添加用户目录
            option.add_argument(userdir)
            logger.debug(userdir)

            # 打开浏览器
            self.driver = webdriver.Chrome(executable_path='./lib/driver/chromedriver', options=option)
            return self.driver
        if browser == 'fire':
            self.driver = webdriver.Firefox(executable_path='./lib/driver/geckodriver.exe')
            return self.driver

        if browser == 'ie':
            self.driver = webdriver.Ie(executable_path='./lib/driver/IEDriverServer.exe')
            return self.driver

    # 打开网址
    def openurl(self, url):
        try:
            self.driver.get(url)
        except:
            logger.exception('无效网址')

    # 元素处理
    def __element(self, element):
        if element[0] == '/':
            ele = self.driver.find_element_by_xpath(element)
        elif element[0] == '#':
            ele = self.driver.find_element_by_css_selector(element)
        elif element[0] == '<':
            ele = self.driver.find_element_by_id(element)
        else:
            logger.error('只支持xpath，selector，id这三种元素，检查元素：' + element)
        return ele

    # 点击
    def click(self, element):
        ele = self.__element(element)
        try:
            ele.click()
        except:
            logger.exception('无效元素')

    # 输入/上传图片
    def sendkeys(self, element, value):
        ele = self.__element(element)
        try:
            ele.send_keys(value)
        except:
            logger.exception('失败')


    #切换窗口
    def switchhandles(self,handle):
        try:
            handle = int(handle)
        except:
            logger.exception('handle必须为int类型')
        self.driver.switch_to.window(self.handles[handle])
        logger.debug(self.handles)
        logger.debug(self.handles[handle])

    #获取handles
    def gethandles(self):
        self.handles = self.driver.window_handles

    #切入iframe
    def switchtoiframe(self,element):
        ele = self.__element(element)
        try:
            self.driver.switch_to.frame(ele)
        except Exception as e:
            logger.exception(e)

    #切出iframe
    def switchoutiframe(self):
        try:
            self.driver.switch_to.defaule_content()
        except Exception as e:
            logger.exception(e)

    #悬停/移动到元素
    def hover(self,element):
        ele = self.__element(element)
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(ele).perform()
        except Exception as e:
            logger.exception(e)

    # 关闭浏览器
    def closebrowser(self):
        try:
            self.driver.quit()
        except:
            logger.exception('浏览器未关闭')

    #隐式等待
    def wait(self,t):
        try:
            t = int(t)
        except:
            t = 5
        self.driver.implicitly_wait(t)

    #强制等待
    def timewait(self,t):
        try:
            t = int(t)
        except:
            t = 5
        time.sleep(t)

    #鼠标滚轮滑动
    def scroll(self,x,y):
        #js的console语法window.scrollBy(x,y)
        js = 'window.scrollBy(' + str(x) + ',' + str(y) + ');'
        self.driver.execute_script(js)





if __name__ == '__main__':
    pass
    web = WEB()
    web.openbrowser('google')
    web.openurl('https://www.baidu.com/')

