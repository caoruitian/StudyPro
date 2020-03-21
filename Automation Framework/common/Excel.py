# coding:utf8
import os
import xlrd
from xlutils.copy import copy


class Reader:
    """
        powered by Mr Will
           at 2018-12-21
        用来读取Excel文件内容
    """
    def __init__(self):
        # 整个excel工作簿缓存
        self.workbook = None
        # 当前工作sheet
        self.sheet = None
        # 当前表的总行数
        self.rows = 0
        # 当前sheet的行数
        self.r = 0
        # 当前表的总列数
        self.cols = 0
        # 当前sheet的列数
        self.c = 0

    # 打开excel
    def open_excel(self, srcfile):
        if not os.path.isfile(srcfile):
            print("error：%s not exist!" % (srcfile))
            return

        # 设置读取excel使用utf8编码
        xlrd.Book.encoding = "utf8"
        # 读取excel内容到缓存workbook
        self.workbook = xlrd.open_workbook(filename=srcfile)
        # 选取第一个sheet页面
        self.sheet = self.workbook.sheet_by_index(0)
        # 设置rows为当前sheet的总行数
        self.rows = self.sheet.nrows
        # 设置默认读取为第一行
        self.r = 0
        # 设置cols为当前sheet的总列数
        self.cols = self.sheet.ncols
        # 设置默认读取为第一列
        self.c = 0
        return

    # 获取sheet页面
    def get_sheets(self):
        # 获取所有sheet的名字，并返回
        sheets = self.workbook.sheet_names()
        print(sheets)
        return sheets

    # 切换sheet页面
    def set_sheet(self, name):
        # 通过sheet名字，切换sheet页面
        self.sheet = self.workbook.sheet_by_name(name)
        self.rows = self.sheet.nrows
        self.r = 0
    # 逐行读取
        return

    #获取表格内容
    def getparameter(self,row,col,sheetname = 'first'):
        try:
            row = int(row)
            col = int(col)
            if row > self.rows or col > self.cols:
                row = 0
                col = 0
                print('超出行列，读取当前sheet第1个表格')
        except:
            row = 0
            col = 0
            print('输入错误，读取当前sheet第1个表格')
        if sheetname == 'first':
            parameter = self.sheet.cell(row,col).value
        else:
            try:
                parameter = self.workbook.sheet_by_name(sheetname).cell(row, col).value
            except:
                print('您输入的sheetname有误！')
                return
        return parameter
        # print(parameter)

    def readline(self):
        row1 = None

        # 如果当前还没到最后一行，则读取一行
        if self.r < self.rows:
            #获取第self.r行的内容
            row = self.sheet.row_values(self.r)
            self.r = self.r + 1
            i = 0
            row1 = row
            # 如果读取的是小数，则判断是不是整数
            for strs in row:
                if type(strs) == float:
                    if strs == int(strs):
                        # 如果是10.0这样的，则取整；如果要输入10.0，请使用在excel里面输入'10.0
                        row1[i] = str(int(strs))
                    else:
                        # 其他数据，转为字符串
                        row1[i] = str(strs)
                else:
                    row1[i] = strs

                i = i + 1
        return row1


class Writer:
    """
        powered by Mr Will
        用来复制写入Excel文件
           at 2018-12-21
    """
    def __init__(self):
        # 读取需要复制的excel
        self.workbook = None
        # 拷贝的工作空间
        self.wb = None
        # 当前工作的sheet页
        self.sheet = None
        # 记录生成的文件，用来保存
        self.df = None
        # 记录写入的行
        self.row = 0
        # 记录写入的列
        self.clo = 0

    # 复制并打开excel
    def copy_open(self, srcfile, dstfile):
        # 判断要复制的文件是否存在
        if not os.path.isfile(srcfile):
            print(srcfile + " not exist!")
            return

        # 判断要新建的文档是否存在，存在则提示
        if os.path.isfile(dstfile):
            print("warning：" + dstfile + " file already exist!")

        # 记录要保存的文件
        self.df = dstfile
        # 读取excel到缓存
        #formatting_info带格式复制
        #self.workbook源文件的内存空间，改动会直接改源文件
        self.workbook = xlrd.open_workbook(filename=srcfile, formatting_info=True)
        # 拷贝
        # 把self.workbook复制到self.wb后，再改动self.wb，就不会影响源文件
        self.wb = copy(self.workbook)
        # 默认使用第一个sheet
        # self.sheet = self.wb.get_sheets('sheet1')
        return

    # 切换sheet页面
    def set_sheet(self, name):
        # 通过sheet名字，切换sheet页面
        self.sheet = self.wb.get_sheet(name)
        print(name)
        return

        # 切换sheet页面
    def get_sheets(self):
        # 获取所有sheet的名字，并返回
        sheets = self.workbook.sheet_names()
        print(sheets)
        return sheets

    # 写入指定单元格，保留原格式
    def write(self, r, c, value):
        # 获取要写入的单元格
        def _getCell(sheet, r, c):
            """ HACK: Extract the internal xlwt cell representation. """
            # 获取第r行
            row =sheet._Worksheet__rows.get(r)
            if not row:
                return None

            # 获取单元格(row中确定r行后，获取c列)
            cell = row._Row__cells.get(c)
            return cell

        # 获取要写入前的单元格
        cell = _getCell(self.sheet, r, c)

        # 写入值
        self.sheet.write(r, c, value)
        if cell:
            # 获取要写入后的单元格
            ncell = _getCell(self.sheet, r, c)
            if ncell:
                # 设置写入后格式和写入前一样
                ncell.xf_idx = cell.xf_idx

        return

    # 保存
    def save_close(self):
        # 保存复制后的文件
        self.wb.save(self.df)
        return


class test:
    pass



# 调试
if __name__ == '__main__':
#     pass
#     reader = Reader()
#     reader.open_excel('../lib/cases/Mytest_HTTP接口用例.xls')
#     sheetname = reader.get_sheets()
#     for i in range(reader.rows):
#         print(reader.readline())

    # writer = Writer()
    # writer.copy_open('../lib/cases/Mytest_HTTP接口用例.xls', '../lib/results/Mytest_HTTP接口用例.xls')
    # sheetname = writer.get_sheets()
    # writer.set_sheet(sheetname[0])
    # writer.write(1, 1, 'William')
    # writer.save_close()


    # 获取表格内容测试
    reader = Reader()
    reader.open_excel('../lib/cases/Mytest_HTTP接口用例.xls')
    sheetname = reader.get_sheets()
    a = reader.getparameter('1','1','登录接口')
    print(a)

