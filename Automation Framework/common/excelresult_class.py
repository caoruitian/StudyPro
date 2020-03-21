from common.Excel import Reader
from common import logger

class Res:

    def __init__(self):
        #用于记录所有模块分组信息名称
        self.sumarry = {}

    def get_res(self,result_path):
        #用于记录执行结果，逻辑行为，只要分组中出现一个失败，则认为改分组结果失败
        self.sumarry.clear()
        status = 'Fail'
        #标识是否有失败
        flag = True
        #统计测试用例的用例总数
        totalcount = 0
        #统计所有用例中通过用例的条数
        totalpass = 0

        reader = Reader()
        reader.open_excel(result_path)
        #获取所有sheet页面
        sheetname = reader.get_sheets()
        for n in sheetname:
            #从第一个页面开始解析
            reader.set_sheet(n)
            #获取当前sheeet的总行数，用来遍历
            row = reader.rows
            #设置从第二行开始读
            reader.r = 1

            #遍历sheet里面所有用例
            for i in range(1,row):
                line = reader.readline()
                #查找记录了分组信息的行
                #如果第一列(分组信息)和第二列(类名或者用例名)不同时为空，则不是用例，执行非用例操作
                # if not (line[0]  == '' and line[1]  == ''):
                if len(line[0]) > 0 or len(line[1]) > 0:
                    pass
                #非用例行判断借宿
                #第一列信息和第二列信息均为空的行，这时开始进行用例数、通过数、状态的统计
                else:
                    #判断执行结果列，如果为空，将flag置为false，是为改行有误，不纳入用例数量计算
                    if len(line) < 6 or len(line[7]) == '':
                        flag = False
                    #执行结果不为空，则将用例统计数自增
                    else:
                        totalcount += 1
                        #如果通过，则通过数和总通过数均自增
                        if line[7]  == 'PASS':
                            totalpass += 1
                        else:
                            #出现了用例执行结果不是pass的情况，则视为当前分组执行失败
                            flag = False
            #for循环结束

        #所有用例执行概况
        #计算执行通过率
        #如果flag = True
        if flag:
            status = 'Pass'

        #计算通过率
        try:
            p = int(totalpass * 10000 / totalcount)
            passrate = p / 100
        except Exception as e:
            passrate = 0.0
            logger.exception(e)

        #设置默认第一个sheet,用来读取runtype，title，StartTime，EndTime
        reader.set_sheet(sheetname[0])

        self.sumarry['runtype'] = str(reader.getparameter('1','1'))        #请求方式
        self.sumarry['title'] = str(reader.getparameter('1','2'))          #标题
        self.sumarry['StartTime'] = str(reader.getparameter('2','3'))      #开始时间
        self.sumarry['EndTime'] = str(reader.getparameter('2','4'))        # 结束时间
        self.sumarry['casecount'] = str(totalcount)                         #用例总数
        self.sumarry['passrate'] = str(passrate) + '%'                     #通过率
        self.sumarry['status'] = status                                     #结果

        return self.sumarry


if __name__ == '__main__':
    res = Res()
    sumarry = res.get_res('../lib/results/result-Mytest_HTTP接口用例.xls')
    logger.info(sumarry)

