#!/usr/bin/env python
#coding:utf-8
import re
import datetime

'''
Count the status for DBs imp
Author : Sun Ning
'''
logDir="/data0/syncdata/log/"
p1 = re.compile(r'^(\d{8})')
p2 = re.compile(r'^(\d{8} .*) no_sql_file')
p3 = re.compile(r'(.+sql)')

today = datetime.date.today()
f = open("%sno_file_record_%s"%(logDir,today))
ret = f.read()
print p3.findall(ret)


def imp_result_reduce(date):
	#f = "%s/exec_results_%s"%(logDir,date)	
	f='./aaa'
	rc = re.compile(r"(### Start time .*)")
	f = open(f,'r')
	result = f.read()
	mlist = re.findall(rc,result)
	lastStart = mlist[len(mlist) - 1]
	f.seek(0)
	rlist=f.readlines()
	lineNum=rlist.index(lastStart+'\n')
	ulist = rlist[lineNum:] 
	f.close()
	
	flist=[]
	noFileList=[]
	dataErrList=[]
	sNum=0
	for ln in ulist:
		if 'SUCCESSED' in ln:
			sNum += 1
		elif 'FAILED' in ln:
			cid = re.findall(p1,ln)
			flist.append(cid[0])
		elif 'no_sql_file' in ln:
			cid = re.findall(p2,ln)
			noFileList.append(cid[0])
		elif 'local_data_not_equal_with_DX' in ln:
			cid = re.findall(p1,ln)
			dataErrList.append(cid[0])
	print "Successed number : %d \nFailed number : %d \nNo SQL file's number : %d \nLoad data not equal with DX number : %d"%(sNum,len(flist),len(noFileList),len(dataErrList))
	return (dataErrList,flist,noFileList)

#if __name__ == '__main__':
#	today = datetime.date.today()
#	l1,l2,l3 = imp_result_reduce(today)
#	if l1:
#		print "###### load data not equal with DX cids: ######"
#		for cid in l1:
#			print "%s 数据不一致,请检查确认。如果没问题请清除锁文件，以便进行下一次导入"%(cid)	
#	if l2:
#		print "###### Import failed cids: ######"
#		for cid in l2:
#			print "%s 导入失败"%(cid)
#	if l3:
#		print "###### No SQL file's cids: ######"
#		for list in l3:
#			print list
