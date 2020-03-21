from common.Excel import Reader,Writer
from common.mail import Mail
from Excel_keyworks.httpkeys import HTTP
from Excel_keyworks.soapkeys import SOAP
from Excel_keyworks.webkeys import WEB
from Excel_keyworks.appkeys import APP
import inspect,sys
from common import config
from common.mysql import Mysql
from common.excelresult_class import Res
from common import logger
import  datetime

path = '.'
#用例路径
casepath = ''
resultpath = ''

#获取发射后的func
def get_func(h,line):
    #设置func充默认为空，如果有错，则返回空的func
    #用于解决传入的参数line[3]错了，比如方法有post，但是表写错，返回的line[3]为poss，HTTP类是没有poss方法的，因此会报错
    func = None
    try:
        func = getattr(h, line[3])
    except Exception as e:
        print(e)
    return func


#获取反射后方法的参数个数
def get_args(func):
    #配合get_func()返回的空func处理,如果func为空
    if func:
        args = inspect.getfullargspec(func).__str__()
        args = args[args.find('args=')+5 : args.find(', varargs')]
        args = eval(args)
        args.remove('self')
        L = len(args)
        return L
    else:
        return 0


def run(func,L,line):
    #配合get_func()返回的空func处理，如果func为空，则不执行下面代码
    if func is None:
        return
    if L < 1:
        func()
    elif L < 2:
        func(line[4])
    elif L < 3:
        func(line[4],line[5])
    elif L < 4:
        func(line[4],line[5],line[6])
    else:
        print('error:不能超过3个参数')


def runCase():
    global casepath,resultpath
    r = Reader()
    w = Writer()

    r.open_excel(casepath)#打开表,默认为第一个sheet
    w.copy_open(casepath, resultpath)
    sheetname = r.get_sheets()

    #根据表格的配置，创建不同的对象，例如表中第2行第2个字段为WEB，即创建WEB()对象
    way = r.getparameter('1','1')
    if way == 'APP':
        obj = APP(None)
    elif way == 'HTTP':
        obj = HTTP(w)
    elif way == 'SOAP':
        obj = SOAP(w)
    elif way == 'WEB':
        obj = WEB()

    w.set_sheet(sheetname[0])
    w.write(2, 3, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))  # StartTime

    for sheet in sheetname:
        #设置读写都是当前的sheet页面
        r.set_sheet(sheet)
        w.set_sheet(sheet)
        w.clo = 7#写入的列数以固定，所以设置列数为第8列，！第一列为0
        for i in range(r.rows):
            line = r.readline()
            w.row = i #读到第几行就写入第几行
            print(line)
            if len(line[0]) > 0 or len(line[1]) > 0:
                continue
            else:
                # 接口类型设置2
                func = get_func(obj, line)

                L = get_args(func)
                run(func,L,line)

    w.set_sheet(sheetname[0])
    w.write(2, 4, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))#EndTime
    w.save_close()
        # print('==============================='+ sheet+'==============================')

if __name__ == '__main__':
    #路径处理
    try:
        casepath = sys.argv[1]
    except:
        casepath = ''

    if casepath == '':
        #如果casepath为空，使用默认路径
        casepath = path + '/lib/cases/Mytest_HTTP接口用例.xls'
        resultpath = path + '/lib/results/result-Mytest_HTTP接口用例.xls'
    else:
        #如果是绝对路径，就使用绝对路径
        if casepath.find(':') >= 0:
            #获取用例文件名
            resultpath = path + '/lib/results/result-' + casepath[casepath.rfind('\\')+1:]
        else:
            logger.error('非法路径')

    #执行用例
    config.get_config(path + '/lib/conf/conf.txt')
    #还原数据库
    mysql = Mysql()
    mysql.init_mysql(path + '/lib/mysql/userinfo.sql')
    StartTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    runCase()
    EndTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    res = Res()
    r = res.get_res(resultpath)

    #邮件设置
    text = config.config['mailtext']
    if r['status'] == 'PASS':
        text = text.replace('status', r['status'])
    else:
        text = text.replace('<font style="font-weight: bold;font-size: 14px;color: #00d800;">status</font>','<font style="font-weight: bold;font-size: 14px;color: red;">Fail</font>')
    text = text.replace('passrate', r['passrate'])
    text = text.replace('casecount', r['casecount'])
    text = text.replace('runtype',r['runtype'])
    text = text.replace('title',r['title'])
    text = text.replace('starttime',r['StartTime'])
    text = text.replace('endtime',r['EndTime'])
    config.get_config('./lib/conf/conf.txt')
    mail = Mail()
    mail.send(text)
