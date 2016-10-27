#!/usr/bin/env python
#coding:utf-8
from sendMail import send_mail
import re
import datetime
import os,sys
sys.path.append("../..")
import dbconf

'''
Count the status for DBs imp
Author : Sun Ning
'''
dbHost=dbconf.g_importDBHost
logDir="/data0/syncdata/log/"
p = re.compile(r"(### .*)")
p0 = re.compile(r'^(\d{8}) .* DELETE FROM cinema_sell_log')
p1 = re.compile(r'^(\d{8} .*.sql)')
p2 = re.compile(r'^(\d{8} .*) no_sql_file')
p3 = re.compile(r'FAILED (\d{1,2})')
p4 = re.compile(r'^(\d{8} .*) MD5_NOT_SAME_EXCEPTION')

exceptDict =   {1:'custom exception',
		2:'cinema_movie_show_seat_stat',
		3:'run shell err',
		4:'check md5 err',
		5:'local data is not equal with DX',
		6:'''2014, Commands out of sync; you can't run this command now''',
		7:'''1062, Duplicate entry (*) for key (*) ''',
		8:'''1064, You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near...''',
		9:'2013, Lost connection to MySQL server during query',
		10:'''1609, The BINLOG statement of type `Table_map` was not preceded by a format description BINLOG statement.''',
		99:'other error!'}

def get_no_sql_cids(date):
	today = datetime.date.today()
	fname = "%sno_file_record_%s"%(logDir,today)
	if os.path.exists(fname):
		f = open(fname,'r')
		ret = f.read()
		recordList = p.findall(ret)
		lastStart = recordList[len(recordList) - 1]
		f.seek(0)
		flist = f.readlines()
		startNum = flist.index(lastStart + '\n')
		uList = flist[startNum + 1:]
		f.close()
		return [x.strip('\n') for x in uList]
	else:
		return []

def imp_result_reduce(date):
	fName = "%s/exec_results_%s"%(logDir,date)	
	rc = re.compile(r"(### Start time .*)")
	f = open(fName,'r')
	result = f.read()
	mlist = re.findall(rc,result)
	lastStart = mlist[len(mlist) - 1]
	f.seek(0)
	rlist=f.readlines()
	lineNum=rlist.index(lastStart+'\n')
	ulist = rlist[lineNum:] 
	f.close()
	
	dSellList=[]
	noFileList=get_no_sql_cids(date)
	dataErrList=[]
	md5ErrList=[]
	el1,el2,el3,el4,el5,el6,el7,el8,el9,el10,el99=[],[],[],[],[],[],[],[],[],[],[]
	sNum,fNum=0,0
	for ln in ulist:
		if 'SUCCESSED' in ln:
			sNum += 1
		elif 'FAILED' in ln:
			fNum += 1
			exceptNo = int(p3.findall(ln)[0])
			cid = re.findall(p1,ln)[0]
			if exceptNo == 1:
				el1.append(cid)
			elif exceptNo == 2:
				el2.append(cid)
			elif exceptNo == 3:
				el3.append(cid)
			elif exceptNo == 4:
				el4.append(cid)
			elif exceptNo == 5:
				el5.append(cid)
			elif exceptNo == 6:
				el6.append(cid)
			elif exceptNo == 7:
				el7.append(cid)
			elif exceptNo == 8:
				el8.append(cid)
			elif exceptNo == 9:
				el9.append(cid)
			elif exceptNo == 10:
				el10.append(cid)
			elif exceptNo == 99:
				el99.append(cid)
		elif 'no_sql_file' in ln:
			cid = re.findall(p2,ln)
			noFileList.append(cid[0])
		elif 'local_data_not_equal_with_DX' in ln:
			cid = re.findall(p1,ln)
			dataErrList.append(cid[0])
		elif 'MD5_NOT_SAME_EXCEPTION' in ln:
			cid = re.findall(p4,ln)
			md5ErrList.append(cid[0])
		elif 'DELETE FROM cinema_sell_log' in ln:
			cid = p0.findall(ln)
			dSellList.append(cid[0])

	#generate the mail content
	info = "总共导入:    %d\n"%(sNum+fNum+len(noFileList)+len(dataErrList))
	info += "成功:    %d\n失败:    %d\n没有SQL文件:    %d\n和鼎新数据不一致的:    %d\n\n"%(sNum,fNum,len(noFileList),len(dataErrList))
	if dataErrList:
		info += "###### load data not equal with DX cids: ######\n"
		for cid in dataErrList:
			info += "%s 数据不一致,请检查确认，如果没问题请清除锁文件，以便进行下一次导入\n"%(cid)	
	if md5ErrList:
		info += "###### 增量文件MD5校验失败，请检查并重传对应的增量文件，cids: ######\n"
		for cid in md5ErrList:
			info += "%s \n"%(cid)	
	if noFileList:
		info += "###### No SQL file's cids: ######\n"
		for list in noFileList:
			info += "%s\n"%(list)
	if dSellList:
		info += "###### The cid(s) witch delete info from cinema_sell_log: ######\n"
		for cid in dSellList:
			info += "%s 发现从cinema_sell_log删除信息，请检查\n"%(cid)

	info += "###### Import failed cid(s) and reason(s): ######\n"
	if el1:
		for cid in el1:
			info += "%s %s\n"%(cid,exceptDict[1])
	if el2:
		for cid in el2:
			info += "%s %s\n"%(cid,exceptDict[2])
	if el3:
		for cid in el3:
			info += "%s %s\n"%(cid,exceptDict[3])
	if el4:
		for cid in el4:
			info += "%s %s\n"%(cid,exceptDict[4])
	if el5:
		for cid in el5:
			info += "%s %s\n"%(cid,exceptDict[5])
	if el6:
		for cid in el6:
			info += "%s %s\n"%(cid,exceptDict[6])
	if el7:
		for cid in el7:
			info += "%s %s\n"%(cid,exceptDict[7])
	if el8:
		for cid in el8:
			info += "%s %s\n"%(cid,exceptDict[8])
	if el9:
		for cid in el9:
			info += "%s %s\n"%(cid,exceptDict[9])
	if el10:
		for cid in el10:
			info += "%s %s\n"%(cid,exceptDict[10])
	if el99:
		for cid in el99:
			info += "%s %s\n"%(cid,exceptDict[99])
	
	info += "\n谢谢,\n孙宁\n"
	if send_mail("影院导入情况汇总[%s][来自于%s]"%(str(today),dbHost),info):
		print "Send Successed !"
	else:
		print "Send Failed !"

if __name__ == '__main__':
	today = datetime.date.today()
	imp_result_reduce(today)
