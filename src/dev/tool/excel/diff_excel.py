#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
import xlrd, os, sys
 
#if len(sys.argv) != 3:
#    print "\n        ./script diff_1.xlsx diff_2.xlsx \n"
#    sys.exit()

diff = {}
xls1 = sys.argv[1]
xls2 = sys.argv[2]

if os.path.isfile(xls1) and os.path.isfile(xls2):
    pass
else:
    print "\n file not  exists \n"
    sys.exit()


def getcontent(table):  # 获取xlsx表内容
    tmp_data = {}
    tmp_table = ''
    all_data = {}
    
    for j in xrange(table.nrows):
        tmp = table.row_values(j)
        if list(set(tmp)) == ['']:
            tmp_data[tmp_table] = ''
            if tmp_table != '':
                all_data[j] = tmp_table
            tmp_table = ''
        else:
            tmp2 = ""
            for i in tmp:
                try:
                    tmp2 = tmp2 + i + ","
                except:
                    tmp2 = tmp2 + str(i) + ","
                tmp_table = tmp_table + tmp2 + "\n"  # 把多行的内容放一起
    return (tmp_data, all_data)


def write_file(excel_diff, filename):
    f = open(filename, 'w')
    f.write(excel_diff)
    f.close()


def diff_content(table1, table2):  # 检查两个表差异
    diff_tmp = []
    for i in table1:
        if i in table2:
            pass
        else:
            diff_tmp.append(i)
    return list(set(diff_tmp))


def get_rows(diff, all_data):  # 获取差异位置
    tmp = []
    for i in diff:
        for j in all_data:
            if all_data[j].strip() == i.strip():
                tmp.append(j)
                break
    return tmp

for i in range(0, 20):  # 比较几个表
    data1 = xlrd.open_workbook(xls1)
    table1 = data1.sheets()[i]
    data2 = xlrd.open_workbook(xls2)
    table2 = data2.sheets()[i]

    tmp1, all1 = getcontent(table1)
    tmp2, all2 = getcontent(table2)
 
    result = diff_content(tmp1, tmp2)  # 1 中有 2 没有的具体内容
    #  result2= diff_content(tmp2, tmp1)  #2 中有 1 没有的具体内容
    diff[i] = get_rows(result, all1)
    print sorted(diff[i])

    write_file(sorted(diff[i]), "diff.txt")

#  diff[i] = get_rows(result2,all2)
#  print sorted(diff[i])
