import requests,json,jsonpath
from common import logger





class HTTP():

    def __init__(self,write):
        self.session = requests.session()
        #定义字典，保存请求后返回json解析结果
        self.jsoners = {}
        self.res = ''
        #定义变量保存传递的参数
        self.parame = {}
        #定义变量保存地址
        self.url =  ''
        #写入结果的excel(write是传入的一个实例，然后用self.write保存了write实例)
        self.write = write

    #post请求
    def post(self,path,data1=None):
        # try:
        #     path1 = self.__geturl(path)
        #     if data1 == None or data1 == '':
        #         result = self.session.get(path1)
        #     else:
        #         dic = self.__getparame(data1)
        #         dic1 = self.__todic(dic)
        #         result = self.session.get(path1, data=data1)
        #         logger.debug('---------------------' + result.text)
        try:
            path1 = self.__geturl(path)
            print(path1)
            if data1 == None or data1 == '':
                result = self.session.post(path1)
            else:
                if 'username' in data1 or 'password' in data1:
                    dic = self.__getparame(data1)
                    dic1 = self.__todic(dic)
                    result = self.session.post(path1, data=dic1)
                else:
                    result = self.session.post(path1, data=data1)
            logger.debug(result.text)

            # 兼容jsonpath设置
            try:
                res = result.text

            except Exception as e:
                logger.exception(e)

            try:  # 若返回的res不是一个json格式的字符串,解释json.lo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   ads(res)的时候会报错,所以做容错处理
                self.jsoners = json.loads(res)
                self.res = ''
            except:
                self.jsoners = None
                self.res = res

            self.write.write(self.write.row, self.write.clo, 'PASS')
            self.write.write(self.write.row, self.write.clo + 1,str(self.jsoners) + '  ' + self.res[self.res.find('{'):self.res.find('}') + 1])
        except Exception as e:
            self.write.write(self.write.row, self.write.clo, 'FAIL')
            self.write.write(self.write.row, self.write.clo + 1,str(self.jsoners) + '  ' + self.res[self.res.find('{'):self.res.find('}') + 1])

    # get请求
    def get(self, path, data1=None):
        try:
            path1 = self.__geturl(path)
            if data1 == None or data1 == '':
                result = self.session.get(path1)
            else:
                dic = self.__getparame(data1)
                dic1 = self.__todic(dic)
                result = self.session.get(path1, data=data1)

            # 兼容jsonpath设置
            try:
                res = result.text
                res = res[res.find('{'):res.rfind('}') + 1]
            except Exception as e:
                logger.exception(e)

            try:#若返回的res不是一个json格式的字符串,解释json.loads(res)的时候会报错,所以做容错处理
                self.jsoners = json.loads(res)
                self.res = ''
            except:
                self.jsoners = None
                self.res = res

            self.write.write(self.write.row, self.write.clo, 'PASS')
            self.write.write(self.write.row, self.write.clo + 1,str(self.jsoners) + '  ' + self.res[self.res.find('{'):self.res.find('}') + 1])
        except Exception as e:
            self.write.write(self.write.row, self.write.clo, 'FAIL')
            self.write.write(self.write.row, self.write.clo + 1,str(self.jsoners) + '  ' + self.res[self.res.find('{'):self.res.find('}') + 1])

    #断言返回结果跟期望结果是否相等
    def assertequals(self,jsonpaths,value):
        #这里容错处理的情况跟def savejson(self,key,p)的方法一样，都是用户未登陆的情况
        res = None
        if self.jsoners is None:
            res = self.res
        else:
            try:
                # res = str(self.jsoners[key])
                res = str(jsonpath.jsonpath(self.jsoners,'status')[0])
                logger.debug(res)
            except Exception as e:
                logger.exception(e)
            #v alue传的擦函数是字符串，jsoners字典里面的jsoners[key]值是int，比较需要类型相同
        if res == str(value):
            self.write.write(self.write.row, self.write.clo, 'PASS')
            self.write.write(self.write.row, self.write.clo + 1, res)
        else:
            self.write.write(self.write.row, self.write.clo, 'FAIL')
            self.write.write(self.write.row, self.write.clo + 1, res)

    #更新头
    def addheader(self,key,value):
        p = self.__getparame(value)
        self.session.headers[key] = p
        self.write.write(self.write.row, self.write.clo, 'PASS')
        self.write.write(self.write.row, self.write.clo + 1, value)

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
        # logger.debug(p)
        # logger.debug(self.parame)
        for key in  self.parame:
            # logger.debug(key)
            p = p.replace('{'+ key +'}',self.parame[key])
            # logger.debug('p:',p)
        return  p

    #把传入的字符串转换为字典
    def __todic(self,s):
        dic = {}
        # logger.debug(s)
        l = s.split('&')
        # logger.debug(l)
        for ss in l:
            ll = ss.split('=')
            # logger.debug(ll)

            #1·解决传入的参数错误问题，传入参数s正确格式是username=Crtims123&password=123456，若传入了Crtims123·123456
            #2· l= s.split('&')分割后的列表l = ['Crtims123·123456']
            #3·遍历l再次分割ll = ss.split('=')，l只有一个元素，所以ss便利出来还是只有一个元素，所以最后ll=ss.split('=')分割后的列表ll = ['Crtims123·123456']
            #4·所以但传入的参数s的格式不对，最后得出ll列表元素个数只有一个
            #5·因此当ll的元素个数大于1个的时候，才运行下面代码，否则返回空列表
            if len(ll) > 1:
                dic[ll[0]] = ll[1]
            else:
                dic[ll[0]] = ''
        # logger.debug(dic)
        return dic

    def seturl(self,url):
        #判断url是否以http开头
        if url.startswith('http'):
            self.url = url
            self.write.write(self.write.row,self.write.clo,'PASS')
        else:
            logger.error("error:地址不合法")
            self.write.write(self.write.row, self.write.clo, 'FAIL')
            self.write.write(self.write.row, self.write.clo+1, 'error:地址不合法')

    def __geturl(self,path):
        path = self.url + '/' +  path
        return path

    def removeheader(self,key):
        try:
            self.session.headers.pop(key)
            # logger.debug(self.session.headers)
            self.write.write(self.write.row, self.write.clo, 'PASS')
            self.write.write(self.write.row, self.write.clo + 1, self.session.headers)
        except Exception as e:
            logger.warn("warn:没有可删除的头")
            self.write.write(self.write.row, self.write.clo, 'PASS')
            self.write.write(self.write.row, self.write.clo + 1, 'warn:没有可删除的头')
