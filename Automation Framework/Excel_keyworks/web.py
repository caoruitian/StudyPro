# coding=utf8
from selenium import webdriver
from common import logger
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time, os,traceback


# 浏览器操作的类
class Web:
    """
    打开并操作浏览器的类
    """

    def __init__(self, w):
        self.driver = None
        # 写入结果
        self.writer = w

    def openbrowser(self, b='chrome', d='chromedriver.exe'):
        # if b == 'chrome' or b == "":
        #     if d == "":
        #         d = "./lib2/chromedriver"

        # op = Options()
        #     # 去掉提示条
        # op.add_argument('--disable-infobars')
        #     # 添加用户配置文件，可以带缓存
        # try:
        #         # userdir = os.environ['USERPROFILE'] + '\\AppData\\Local\\Google\\User Data'
        #     userdir = os.environ['USERPROFILE']
        #     userdir = 'user-data-dir=' + userdir + '\\AppData\\Local\\Google\\User Data'
        # except Exception as e:
        #         # 跑Selenium文件夹里面的123.py即可知道结果
        #     userdir = 'C:\\Users\\fotileshanghai3\\AppData\\Local\\Google\\Chrome\\User Data'
        # print(userdir)
        # op.add_argument('--user-data-dir=' + userdir)

        option = webdriver.ChromeOptions()
        # 去掉提示条配置
        option.add_argument('disable-infobars')
        # 加快浏览速度，获取本机用户路径
        userdir = os.environ['USERPROFILE']
        userdir = 'user-data-dir=' + userdir + '\\AppData\\Local\\Google\\User Data'
        # 添加用户目录
        option.add_argument(userdir)
        logger.debug(userdir)

        self.driver = webdriver.Chrome(executable_path='../lib/driver/chromedriver', options=option)
        self.driver.implicitly_wait(10)
        # self.writer.write(self.writer.row, self.writer.clo, "PASS")
        # self.writer.write(self.writer.row, self.writer.clo + 1, "成功打开浏览器")

    def geturl(self, url):
        self.driver.get(url)
        self.writer.write(self.writer.row, self.writer.clo, "PASS")
        self.writer.write(self.writer.row, self.writer.clo + 1, str(url))

    def click(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath).click()
            self.writer.write(self.writer.row, self.writer.clo, "PASS")
            self.writer.write(self.writer.row, self.writer.clo + 1, "点击成功")
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, self.writer.clo, "FAIL")
            self.writer.write(self.writer.row, self.writer.clo + 1, str(e))

    def input(self, xpath, text):
        try:
            self.driver.find_element_by_xpath(xpath).send_keys(text)
            self.writer.write(self.writer.row, self.writer.clo, "PASS")
            self.writer.write(self.writer.row, self.writer.clo + 1, "输入成功")
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, self.writer.clo, "FAIL")
            self.writer.write(self.writer.row, self.writer.clo + 1, str(e))

    # 比如图片上传（若id很长字符多变可上级/div[2]/input方式查找）
    def iniframe(self, xpath):
        try:
            self.driver.switch_to.frame(self.driver.find_element_by_xpath(xpath))
            self.writer.write(self.writer.row, self.writer.clo, "PASS")
            self.writer.write(self.writer.row, self.writer.clo + 1, "输入成功")
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, self.writer.clo, "FAIL")
            self.writer.write(self.writer.row, self.writer.clo + 1, str(e))

    def outiframe(self, xpath):
        try:
            self.driver.switch_to().default_content()
            self.writer.write(self.writer.row, self.writer.clo, "PASS")
            self.writer.write(self.writer.row, self.writer.clo + 1, "输入成功")
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, self.writer.clo, "FAIL")
            self.writer.write(self.writer.row, self.writer.clo + 1, str(e))

    # 切换进新窗口,窗口句柄
    def switchwindow(self, index):
        try:
            self.driver.switch_to.window(self.driver.window_handles[int(index)])
            self.writer.write(self.writer.row, self.writer.clo, "PASS")
            self.writer.write(self.writer.row, self.writer.clo + 1, "输入成功")

        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, self.writer.clo, "FAIL")
            self.writer.write(self.writer.row, self.writer.clo + 1, str(e))

    # 滚动 移动下来
    def moveto(self, xpath):
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(self.driver.find_element_by_xpath(xpath)).perform()
            self.writer.write(self.writer.row, self.writer.clo, "PASS")
            self.writer.write(self.writer.row, self.writer.clo + 1, "输入成功")

        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, self.writer.clo, "FAIL")
            self.writer.write(self.writer.row, self.writer.clo + 1, str(e))

    # 执行JS比如：window.scrollBy(0,3000)（移动）
    def excutejs(self, js):
        """
        封装了默认执行js的方法
        :param js: 需要执行的标准js语句
        :return: 无
        """
        try:
            self.driver.execute_script(js)
            self.writer.write(self.writer.row, self.writer.clo, 'PASS')
            return True
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            # traceback获得报错信息并往下执行
            self.writer.write(self.writer.row, self.writer.clo + 1, str(traceback.format_exc()))
            # 定位失败，则直接返回
            return False


if __name__ == '__main__':
    web = Web(None)
    web.openbrowser('chrome','')
    web.geturl('https://www.baidu.com')