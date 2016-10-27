#!/usr/bin/env python
#coding:utf-8

from mysql import MySQL
from sqlImport import SqlImport,getLogger
from CustomException import *
import dbconf
import Queue
from multiprocessing import Pool
import time,datetime
import sys,os
import traceback
import re
import glob 
import copy

logDir = "./log/"
dataDir = "./data/"
sqlDir = "../binlog/"
dbconfig = {'host':dbconf.g_resultDBHost,
        'port':dbconf.g_resultDBPort,
        'user':dbconf.g_resultDBUser,
        'passwd':dbconf.g_resultDBPwd,
        'db':dbconf.g_resultDBName,
        'charset':'utf8'}
db = MySQL(dbconfig)
dbHost=dbconf.g_importDBHost
sql1 = "select cID from available_CID where cinema_flag=1 and db_host_ip='%s';"%(dbHost)
cids = db.fetchAllRows(sql1)

### The job actually running
def do_job(args):
    id = cLists[args]
    print id
    logger = getLogger(id)
    t_start = time.strftime("%Y-%m-%d_%H:%M:%S")
    logger.info("Process %s, start time: %s"%(args,t_start))
    task = None
    flag = True
    exceptNo = 0
    cardInfo = None
    try:
        task = SqlImport(id,logger)
	sqlFile=task.getRecords()[0]
        logger.info("SQL FILE : %s",sqlFile)
        task.runDumpDB()
	cardInfo=task.getCardSum()
    except CustomException:
        exceptNo = 1
        flag = False
        logger.info(traceback.format_exc())
    except DB_cinema_movie_show_seat_stat:
        exceptNo = 2
        flag = False
        logger.info(traceback.format_exc())
    except Shell_RUN_EXCEPTION:
        exceptNo = 3
        flag = False
        logger.info(traceback.format_exc())
    except MD5_NOT_SAME_EXCEPTION:
        exceptNo = 4
        flag = False
        logger.info(traceback.format_exc())
    except LOCAL_NOT_EQUAL_DX:
        exceptNo = 5
        flag = False
        logger.info(traceback.format_exc())
    except SQL_2014:
        exceptNo = 6
        flag = False
        logger.info(traceback.format_exc())
    except SQL_1062:
        exceptNo = 7
        flag = False
        logger.info(traceback.format_exc())
    except SQL_1064:
        exceptNo = 8
        flag = False
        logger.info(traceback.format_exc())
    except SQL_2013:
        exceptNo = 9
        flag = False
        logger.info(traceback.format_exc())
    except SQL_1609:
        exceptNo = 10
        flag = False
        logger.info(traceback.format_exc())
    except Exception, e:
        exceptNo = 99
        flag = False
        logger.info(traceback.format_exc())
    finally:
    	t_end = time.strftime("%Y-%m-%d_%H:%M:%S")
    	logger.info("Process %s, end time: %s"%(args,t_end))
        if flag:
                logger.info("IMPORT RESULT: %s SUCCESSED %s %s %s %s"%(str(id),t_start,t_end,str(exceptNo),cardInfo))
        else:
                logger.info("IMPORT RESULT: %s FAILED %s %s %s %s"%(str(id),t_start,t_end,str(exceptNo),cardInfo))
	sys.stdout.flush()
        if task:
                del task

### The process(es) pool
def processPools(work_num=10,pro_num=4):
    pool = Pool(processes=pro_num)
    for i in range(work_num):
        result = pool.apply_async(do_job, (i,))
    pool.close()
    pool.join()
    if result.successful():
        print 'All tasks is done!'

### Below method is for results format
def getExecNum(str):
	sql = "select tried_num from import_status_record where curr_sql_file='%s';"%(str)
	if db.fetchOneRow(sql) is None:
		return 0
	else:
		return db.fetchOneRow(sql)[0]

def getRecordStatus(str):
	sql = "select status from import_status_record where curr_sql_file='%s';"%(str)
	if db.fetchOneRow(sql) is None:
		return 0
	else:
		return db.fetchOneRow(sql)[0]

def getLastExcept(str):
	sql = "select exception_type from import_status_record where curr_sql_file='%s';"%(str)
	if db.fetchOneRow(sql) is None:
		return 0
	else:
		return db.fetchOneRow(sql)[0]
def calTime(start,end):
	start=time.strptime(start,"%Y-%m-%d_%H:%M:%S")
	end=time.strptime(end,"%Y-%m-%d_%H:%M:%S")
	start=datetime.datetime(start[0],start[1],start[2],start[3],start[4],start[5])
	end=datetime.datetime(end[0],end[1],end[2],end[3],end[4],end[5])
	return end-start

def getFile(str):
	return glob.glob(logDir+str+'*.log')	

def getFileSize(cid,dateStr):
	return os.path.getsize("%s%s-%s.sql"%(sqlDir,cid,dateStr))

def getSqlName(cid):
	f = open(dataDir+"record_"+str(cid))
	return f.readline().split()[0]

def getSeekValue(cid):
    f = open(dataDir+"record_"+str(cid))
    return f.readline().split()[1]

def getNextSql(fileName):
    items = fileName.split('-')
    days = items[3].split('.')
    last = datetime.datetime.strptime(items[1]+'-'+items[2]+'-'+days[0],'%Y-%m-%d')
    nextDay = last+ datetime.timedelta(days=1)
    return items[0]+'-'+nextDay.strftime('%Y-%m-%d')+'.sql'

def getLastSql(fileName):
    items = fileName.split('-')
    days = items[3].split('.')
    last = datetime.datetime.strptime(items[1]+'-'+items[2]+'-'+days[0],'%Y-%m-%d')
    nextDay = last - datetime.timedelta(days=1)
    return items[0] + '-' + nextDay.strftime('%Y-%m-%d')+'.sql'
#########################################################
# This method is for sellCount normally judgement While 
# found delete some info from cinema_sell_log
# If local sellCount must greather than DX,return True; otherwise return False.
#########################################################
def sellCount_is_greater_than_DX(string):
	print string
	a=string.split(':')[1].split(',')
	return a[0].strip() > a[1].strip()

# if local and DX cardSum are the same, return True; otherwise return False
def cardSum_equal(string):
	print string
	a=string.split(':')[1].split(',')
	return float(a[0].strip()) == float(a[1].strip())

# remove the import lock
def remove_lock(id):
	lock_path="./data/"
	os.remove(lock_path+"lock_%d"%(id))	

#Insert import results into mysql DB
def insResults(cids):
	p0 = re.compile(r'DELETE FROM cinema_sell_log')
	p1 = re.compile(r'\[(sellCount.+?)[\]\n]')
	p2 = re.compile(r'(cardSum.+).{3}(consumeSum.+)]')
	r=r"IMPORT RESULT: (.*)"
	rc=re.compile(r)
	fstat=open(logDir+"exec_results_"+time.strftime("%Y-%m-%d"),"a")
	fstat.write("### Start time : %s, CIDs number: %d ###\n"%(time.strftime("%H:%M:%S"),len(cids)))
	for id in cids:
		sqlName=getSqlName(id)
		file = getFile(str(id))
		print "Read import record from ",max(file)
		fp = open(max(file),"r")
		contents = fp.read()
		sellChange = p0.findall(contents)
		#if sellChange:
		#	fstat.write("%s %s %s\n"%(id,sqlName,sellChange[0]))
		result = re.findall(rc,contents)
		if len(result) == 0:
			fstat.write("%s %s cannot_import\n"%(id,sqlName))
			continue
		else:
			lists = result[len(result) - 1]
		exceptType=lists.split()[4]
		#if md5 check error and the first time tried, get the nextDay sql file
		if exceptType == '4' and getLastExcept(sqlName) == 0:
			sqlName = getNextSql(sqlName)
		#judge if the failed caused by md5 check failed
		elif exceptType == '1' and getLastExcept(getNextSql(sqlName)) == 4:
			sqlName = getNextSql(sqlName)
		runTimes = calTime(lists.split()[2],lists.split()[3])
		lstatus = getRecordStatus(sqlName)
		lexcept = getLastExcept(sqlName)
		triedTime = getExecNum(sqlName)
		if lstatus == "SUCCESSED":
			fstat.write("%s %s no_sql_file\n"%(id,sqlName))
			continue
		elif str(lexcept) == '5':
			fstat.write("%s %s local_data_not_equal_with_DX\n"%(id,sqlName))
			continue
		elif str(lexcept) == '4' and exceptType == '1':
			fstat.write("%s %s MD5_NOT_SAME_EXCEPTION\n"%(id,sqlName))
			continue
		elif str(lexcept) == '98':
			fstat.write("%s %s DELETE-FROM-cinema_sell_log\n"%(id,sqlName))
			continue
		status = lists.split()[1]
		importTime = lists.split()[2]
		sellInfo = re.findall(r"None",lists)
		if exceptType == str(5):
			sell = p1.findall(contents)
			mlist = p2.findall(contents)
			t = mlist[len(mlist)-1]
			sellInfo = "%s  %s  %s"%(sell[len(sell) - 1],t[0],t[1])
			# if found it delete info from cinema_sell_log and other info is normally, reset exceptType, or delete import lock
			if sellChange:
				fstat.write("%s %s %s\n"%(id,sqlName,sellChange[0]))
				if sellCount_is_greater_than_DX(sell[len(sell) - 1]) and cardSum_equal(t[1]):
					exceptType = '98'
					remove_lock(id)
				else:
					exceptType = '98'
			elif str(getLastExcept(getLastSql(sqlName))) in "5,98":
				if sellCount_is_greater_than_DX(sell[len(sell) - 1]) and cardSum_equal(t[1]):
					remove_lock(id)

		else:
			if sellInfo:
				sellInfo = sellInfo[0]
			else:
				sellInfo=re.findall(r"\((.*?)\)",lists)[0].split(',')
				s1 = round(float(sellInfo[0]),2)
				s2 = round(float(sellInfo[1]),2)
				sellInfo = "%s,%s"%(s1,s2) 
		execNum = triedTime + 1
		currSqlDate = re.search(r'\d{4}-\d{2}-\d{2}',sqlName).group(0)
		if execNum == 1:
			sql="INSERT INTO import_status_record \
			(cID,status,import_time,curr_sql_file,duration,tried_num,exception_type,curr_sql_date,card_sum) \
			VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s');"\
			%(id,status,importTime,sqlName,runTimes,execNum,exceptType,currSqlDate,sellInfo)
		else:
			sql="UPDATE import_status_record SET status='%s',import_time='%s',duration='%s',\
			tried_num='%s',exception_type='%s',card_sum='%s' where curr_sql_file='%s';"\
			%(status,importTime,runTimes,execNum,exceptType,sellInfo,sqlName)
		if status == 'FAILED':
			fstat.write("%s %s %s %s\n"%(id,sqlName,status,exceptType))
		else:
			fstat.write("%s %s %s\n"%(id,sqlName,status))
		db.insert(sql)
	fstat.close()

def reschedule_cids(cids):
    lists=[]
    today = datetime.date.today()
    lastDay = today - datetime.timedelta(days = 1)
    f=open(logDir+"no_file_record_"+time.strftime("%Y-%m-%d"),"a")
    f.write("### %s, Record the cids which unscheduled ###\n"%(time.strftime("%H:%M:%S")))
    for list in cids:
        id=list[0]
        lists.append(id)
    new_lists=copy.deepcopy(lists)
    for id in lists:
        sqlName = getSqlName(id)
	fileSize = None
        currSqlDate = re.search(r'\d{4}-\d{2}-\d{2}',sqlName).group(0)
	if os.path.exists("%s%s-%s.sql.gz"%(sqlDir,id,currSqlDate)):
		continue
	if os.path.exists("%s%s-%s.sql"%(sqlDir,id,currSqlDate)):
        	fileSize = getFileSize(id,currSqlDate)
	else:
                f.write("%d %s\n"%(id,sqlName))
		new_lists.remove(id)
        seekSize = getSeekValue(id)
        if str(currSqlDate) == str(lastDay) and str(fileSize) == str(seekSize):
            new_lists.remove(id)
    f.close()
    return new_lists

if __name__ == "__main__":
    #cLists = reschedule_cids(cids)
    cLists = [50120501]
    cidsNum = len(cLists)
    print "Import %s cinema IDs, lists: %s"%(cidsNum,cLists)
    for i in range(1):
    	processPools(cidsNum,1)
    	insResults(cLists)
    #try:
    #    saveout = sys.stdout
    #    saveerr = sys.stderr
    #    f = open("log/import_record"+time.strftime("%m%d_%H%M%S"),"a")
    #    sys.stdout = f
    #    sys.stderr = f
    #	print "Import %s cinema IDs, lists: %s"%(cidsNum,cLists)
    #    for i in range(2):
    #    	print "****** The %d time(s) try... ******"%(i)
    #    	start = time.strftime("%Y-%m-%d %H:%M:%S")
    #    	processPools(cidsNum,16)
    #    	end = time.strftime("%Y-%m-%d %H:%M:%S")
    #    	print "Statistics the import results and write results into mysql"
    #    	insResults(cLists)
    #    	print "Process(es) start times: ",start
    #    	print "Process(es) end times: ",end
    #finally:
    #    f.close()
