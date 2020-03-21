# coding:utf8
from  common import logger


class Txt:
    """
        powered by Mr Will
           at 2018-12-21
        用来读写文件
    """

    # 构造函数打开txt
    def __init__(self, path, t='r', coding='utf8'):
        """
        初始化实例，打开一个txt文件
        :param path: txt的路径
        :param t: 打开文件的方式，r:只读(默认)；w:只写；rw:可读写
        :param coding: 打开文件的编码，默认utf8
        """
        self.data = []#保存txt文件每一行的内容，把每一行的内容当元素保存在列表
        self.f = None
        if t == 'r':#读
            # 打开文件，并且逐行读取
            for line in open(path, encoding=coding):
                self.data.append(line)
            # 去掉换行(txt文件末尾会有换行符\n，添加列表的时候处理掉)
            for i in range(self.data.__len__()):
                #处理非法字符
                self.data[i] = self.data[i].encode('utf-8').decode('utf--8-sig')
                self.data[i] = self.data[i].replace('\n', '')

            return

        if t == 'w':#写
            # 打开可读文件
            #a代表在文件末尾追加写入的内容，不用a，会覆盖原来的内容
            #encoding编码格式
            self.f = open(path, 'a', encoding=coding)
            return

        if t == 'rw':#读写
            for line in open(path, encoding=coding):
                self.data.append(line)
            # 去掉换行
            for i in range(self.data.__len__()):
                self.data[i] = self.data[i].encode('utf-8').decode('utf--8-sig')
                self.data[i] = self.data[i].replace('\n', '')

            self.f = open(path, 'a', encoding=coding)
            return

    # 读取
    def read(self):
        """
        将txt文件按行读取为列表
        :return: 返回txt所有内容的列表
        """
        return self.data

    def writeline(self, s):
        """
        往txt文件末尾写入一行
        :param s: 需要写入的内容，若要换行，请自己添加\n
        :return: 无
        """
        #知道打开的文件不为空，即打开文件成功，写入内容，失败就提示
        if self.f is None:
            logger.error('error：未打开可写入txt文件')
            return

        self.f.write(str(s))

    def save_close(self):
        '''
        写入文件后，必须要保存
        :return: 无
        '''
        #c成功打开文件后才能关闭文件，若没成功打开，抛出异常
        if self.f is None:
            logger.error('error：未打开可写入txt文件')
            return

        self.f.close()


# 调试
if __name__ == '__main__':
    # 读取
    # reader = Txt('../lib/logs/all.log')
    reader = Txt('../lib/conf/conf.txt')
    t = reader.read()
    print(t)

    # 写入
    # writer = Txt('../lib/logs/all.log', t='w')
    # writer.writeline('写入成功\n')
    # writer.save_close()
