from suds.client import Client
from suds.xsd.doctor import ImportDoctor,Import #命名空间设置
import requests,json,jsonpath
from common import logger




class SOAP():
    def __init__(self,write):
        self.doctors = None
        self.wsdlurl = ''
        self.client = None
        self.header = {}
        self.result = None
        self.jsoners = None
        self.parame = {}
        self.res = ''
        self.write = write


    def adddoctor(
                  self,
                  targetNamespace,
                  XLMSchema = 'http://www.w3.org/2001/XMLSchema',
                  locations = 'http://www.w3.org/2001/XMLSchema.xsd'
                  ):

        # 添加默认的XLMSchema
        imp = Import(XLMSchema, location=locations)
        # 添加命名空间
        imp.filter.add(targetNamespace)
        self.doctors = ImportDoctor(imp)
        self.write.write(self.write.row, self.write.clo, 'PASS')


    def setwsdl(self,url):
        self.wsdlurl = url
        try:
            self.client = Client(self.wsdlurl, doctor=self.doctors)
            self.write.write(self.write.row, self.write.clo, 'PASS')
            self.write.write(self.write.row, self.write.clo + 1, str(self.jsoners))

        except Exception as e:
            self.write.write(self.write.row, self.write.clo, 'FAIL')
            self.write.write(self.write.row, self.write.clo + 1, str(self.jsoners))
            logger.exception(e)


    def addheader(self,key,value):
        p = self.__getparame(value)
        self.header[key] = p
        try:
            self.client = Client(self.wsdlurl, doctor=self.doctors, headers=self.header)
            self.write.write(self.write.row, self.write.clo, 'PASS')
            self.write.write(self.write.row, self.write.clo + 1, str(self.jsoners))

        except Exception as e:
            self.write.write(self.write.row, self.write.clo, 'FAIL')
            self.write.write(self.write.row, self.write.clo + 1, str(self.jsoners))
            logger.exception(e)


    def callmethod(self,method,data = ''):
        try:
            data = self.__getparame(data)
            if data == '':
                self.result = self.client.service.__getattr__(method)()
            else:
                d = data.split('、')
                self.result = self.client.service.__getattr__(method)(*d)

            self.jsoners = json.loads(self.result)
            print(self.result)
            self.write.write(self.write.row, self.write.clo, 'PASS')
            self.write.write(self.write.row, self.write.clo + 1, str(self.jsoners))
        except Exception as e:
            self.write.write(self.write.row, self.write.clo, 'FAIL')
            self.write.write(self.write.row, self.write.clo + 1, str(self.jsoners))
            logger.exception(e)




    #断言返回结果跟期望结果是否相等
    def assertequals(self,jsonpaths,value):
        #这里容错处理的情况跟def savejson(self,key,p)的方法一样，都是用户未登陆的情况
        res = None
        if self.jsoners is None:
            res = self.res
        else:
            try:
                # res = str(self.jsoners[key])
                res = str(jsonpath.jsonpath(self.jsoners,jsonpaths)[0])
                logger.debug(res)
            except Exception as e:
                logger.exception(e)
            #value传的擦函数是字符串，jsoners字典里面的jsoners[key]值是int，比较需要类型相同
        if res == str(value):
            self.write.write(self.write.row, self.write.clo, 'PASS')
            self.write.write(self.write.row, self.write.clo + 1, res)
        else:
            self.write.write(self.write.row, self.write.clo, 'FAIL')
            self.write.write(self.write.row, self.write.clo + 1, res)


    #保存token
    def savejson(self,key,p):#传入的参数要跟读表读出的顺序一样，否则会变成self.parame[key] = self.jsoners[p]
        #1·在获取角色信息的时候，例如userid的时候
        #2·若改角色已经登陆，self.jsoners = {'status': 201, 'msg': '用户已经在别处登陆}
        #3·所以传入的key的时候，key = userid，而self.jsoners字典没有userid的键，因此会报错
        #4·所以要特殊处理
        res = ''
        try:
            res = self.jsoners[key]
        except Exception as e:
            logger.exception(e)
        self.parame[p] = res
        self.write.write(self.write.row, self.write.clo, 'PASS')
        self.write.write(self.write.row, self.write.clo + 1, res)
        # logger.info(self.parame)

    #功能：遍历parame字典，如果字典里面的value含有{}的字符串
    def __getparame(self,p):
        for key in  self.parame:
            p = p.replace('{'+ key +'}',self.parame[key])
        return  p


    def removeheader(self,key):
        try:
            self.header.pop(key)
            self.client = Client(self.wsdlurl, doctor=self.doctors, headers=self.header)
            self.write.write(self.write.row, self.write.clo, 'PASS')
            self.write.write(self.write.row, self.write.clo + 1, str(self.jsoners))

        except Exception as e:
            self.write.write(self.write.row, self.write.clo, 'FAIL')
            self.write.write(self.write.row, self.write.clo + 1, str(self.jsoners))
            logger.exception(e)



