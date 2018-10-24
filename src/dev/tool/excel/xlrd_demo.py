#!/usr/bin/env python
# -*- coding:utf-8 -*-
# encoding: utf-8
 
import xlrd, os, sys
 
# if len(sys.argv) != 3:
#    print "\n        ./script diff_1.xlsx diff_2.xlsx \n"
#    sys.exit()
 
diff = {}
xls1 = sys.argv[1]
 
if os.path.isfile(xls1) :
    pass
else:
    print "\n file not  exists \n"
    sys.exit()


def process_xlsx(xls1, xls2):
    xls1_dict = {}
    xls2_dict = {}
    
    wb1 = xlrd.open_workbook(xls1)
    wb2 = xlrd.open_workbook(xls2)
    xls1_sheet_names = wb1.sheet_names()
    xls1_sheet_num = len(xls1_sheet_names)
    print 'xls1 sheet_name num:%s' % str(xls1_sheet_num)
    for name1 in xls1_sheet_names:
        xls1_dict[name1] = 'init'
    
    xls2_sheet_names = wb2.sheet_names()
    xls2_sheet_num = len(xls2_sheet_names)
    print 'xls2 sheet_name num:%s' % str(xls2_sheet_num)
    for name2 in xls2_sheet_names:
        xls2_dict[name2] = 'init'

    both_exist = []
    exist_in_xls1 = []
    exist_in_xls2 = []

    for k1 in xls1_dict:
        if xls2_dict.has_key(k1):
            xls1_dict[k1] = 'exist'
            xls2_dict[k1] = 'exist'
            both_exist.append(k1)
        else:
            exist_in_xls1.append(k1)

    for k1 in xls2_dict:
        if (not xls1_dict.has_key(k1)):
            exist_in_xls2.append(k1)
    print '只存在在xls1中的有:%s\n' % len(exist_in_xls1)
    for k in exist_in_xls1:
        print k
    print '\n'
    print '只存在在xls2中的有:%s\n' % len(exist_in_xls2)
    for k in exist_in_xls2:
        print k
    print '\n'
    print 'xls1和xls2中都有的:%s\n' % len(both_exist)
    for k in both_exist:
        print k
    print '\n'
    
    print '下面开始分析数据:\n'
    tmp_sheet_num = 0
    for sheet_name  in both_exist:
        tmp_sheet_num = tmp_sheet_num + 1
        xls1_sheet = wb1.sheet_by_name(sheet_name)
        xls2_sheet = wb2.sheet_by_name(sheet_name)
        xls1_rows = xls1_sheet.nrows
        xls1_ncols = xls1_sheet.ncols
        xls2_rows = xls2_sheet.nrows
        xls2_ncols = xls2_sheet.ncols
        print '处理xls1[%s],name:%s,共%s行,%s列\n' % (str(tmp_sheet_num), sheet_name.encode('utf-8'), str(xls1_rows), str(xls1_ncols))
        print '处理xls2[%s],name:%s,共%s行,%s列\n' % (str(tmp_sheet_num), sheet_name.encode('utf-8'), str(xls2_rows), str(xls2_ncols))
        '''
        try:
            xls1_sheet = wb1.sheet_by_name(sheet_name)
            print 'xls1打开sheet:%s成功' % sheet_name.encode('utf-8')
        except Exception:
            print 'xls1打开sheet:%s失败啦!!!!' % sheet_name
        try:
            xls2_sheet = wb2.sheet_by_name(sheet_name)
            print 'xls2打开sheet:%s成功' % sheet_name.encode('utf-8')
        except Exception:
            print 'xls2打开sheet:%s失败啦!!!!' % sheet_name
        '''
        ##################
        if(xls1_rows <= xls2_rows):
            smaller_rows = xls1_rows
        else:
            smaller_rows = xls2_rows
        if(xls1_ncols <= xls2_ncols):
            smaller_cols = xls1_ncols
        else:
            smaller_cols = xls2_ncols
        print 'smaller_row:%s,smaller_column:%s' % (str(smaller_rows), str(smaller_cols))
        # if(xls1_rows <= smaller_rows):
        for r in xrange(smaller_rows):
            for n in xrange(smaller_cols):
                xls1_value = xls1_sheet.cell_value(r, n)
                xls2_value = xls2_sheet.cell_value(r, n)
                # print 'sheet_num:%s,name:%s,row:%s,col:%s:%s\txls2 cell:%s' % (tmp_sheet_num, sheet_name, r, n, xls1_value, xls2_value)
                #print '[%s,%s],xls1_value:%s,xls2_value:%s' % (r + 1, n + 1, xls1_value, xls2_value)
                try:
                    int(xls1_value)
                except:
                    if (xls1_value == 'Y'):
                        xls1_cell = 'Y'
                    elif(not xls1_value):
                        xls1_cell = '空'
                    else:
                        xls1_cell = xls1_value.encode('utf-8')
                else:
                    xls1_cell = xls1_value
                # try-catch
                try:
                    int(xls2_value)
                except:
                    if (not xls2_value):
                        xls2_cell = '空'
                    elif (xls2_value == 'Y'):
                        xls2_cell = 'Y'
                    else:
                        xls2_cell = xls2_value.encode('utf-8')
                    # xls2_cell = xls2_value.encode('utf-8')
                else:
                    xls2_cell = xls2_value
                
                if(xls1_cell != xls2_cell):
                    print '发现不同:[%s],位于[%s],第%s行第%s列:xls1:%s\t xls2:%s' % (tmp_sheet_num, sheet_name.encode('utf-8'), r + 1, n + 1, str(xls1_cell), str(xls2_cell))
        print 'sheet:[%s]处理完毕\n' % sheet_name.encode('utf-8')


def test():
    s = u'中国'
    # s为unicode先转为utf-8
    s_utf8 = s.encode('UTF-8')
    print s_utf8
    print(s_utf8.decode('UTF-8') == s)
    i = 0
    f = 1.0
    print type('')
    print type(0)


if __name__ == '__main__':
    xls1 = sys.argv[1]
    xls2 = sys.argv[2]
    process_xlsx(xls1, xls2)
    #test()
