from common.Excel import Reader
from common import logger


#测试结果
#通过率
#用例数
'''
1·获取用例总数
2·获取通过数
3·计算通过率
4·通过率小于100.0%=fail
'''

# class read():
#
#     def __init__(self,path):
#         #保存用例总数
#         self.sum = 0
#         #保存通过的用例数
#         self.passs = 0
#         #保存测试结果
#         self.result = 'Fail'
#         #保存通过率
#         self.passrate = 0
#         self.passrate1 = ''
#         #保存读取的测试用例(表)
#         self.r = Reader()
#         self.__getparams(path)
#
#
#     def __getparams(self,path):
#
#         # open_excel方法已有容错处理
#         self.r.open_excel(path)
#
#         self.passrate1 = self.__getpassrate()
#         self.__getresult()
#         return [self.passrate1,self.result]
#
#     #获取通过率
#     def __getpassrate(self):
#         for i in range(self.r.rows):
#             msg = self.r.readline()
#             # logger.debug(msg)
#             if not (len(msg[0]) > 0  or len(msg[1]) > 0):
#                 self.sum += 1
#             if msg[6] == 'PASS':
#                 self.passs += 1
#         self.passrate = self.passs/self.sum*100
#         s = str(self.passs/self.sum*100)+'%'
#         return s
#
#
#     def __getresult(self):
#         if not self.passrate < 100.0:
#             self.result = 'PASS'
#         return self.result


class read():

    def __init__(self):
        #定义字典保存结果
        self.sumarry = {}


    def getparams(self, path):
        # open_excel方法已有容错处理
        r = Reader()
        r.open_excel(path)
        tup = self.__getpassrate(r)
        # logger.debug(tup)
        #获取总用例数
        sum = tup[1]
        #获取通过率
        passrate = tup[0]
        #获取测试结果
        result = self.__getresult(passrate)
        self.sumarry['casecount'] = str(sum)
        self.sumarry['passrate'] = passrate
        self.sumarry['status'] = result


        return self.sumarry

    # 获取通过率
    def __getpassrate(self,r):
        # 保存用例总数
        sum = 0
        # 保存通过的用例数
        passs = 0
        for i in range(r.rows):
            msg = r.readline()
            # logger.debug(msg)
            if not (len(msg[0]) > 0 or len(msg[1]) > 0):
                sum += 1
                if msg[6] == 'PASS':
                    passs += 1
        self.passrate = passs / sum * 100
        s = str(passs / sum * 100) + '%'
        return s,sum

    def __getresult(self,passrate):
        p = passrate.replace('%','')
        p = float(p)
        if not p < 100.0:
            return 'PASS'
        else:
            return 'Fail'






if __name__ == '__main__':
    # a = read('../lib/results/Mytest_HTTP接口用例.xls')
    # logger.info(a.result)
    # logger.info(a.passrate1)
    r = read()
    a = r.getparams('../lib/results/Mytest_HTTP接口用例.xls')
    logger.info(a)


