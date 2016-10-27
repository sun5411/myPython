#!/usr/bin/env python
#coding:utf-8

from mysql import MySQL
from sqlImport import SqlImport,getLogger
from CustomException import *
import dbconf
import Queue
import threading
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

class WorkManager(object):
    def __init__(self,work_num=10,thread_num=2):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.__init_work_queue(work_num)
        self.__init_thread_pool(thread_num)

    ### Initialize thread
    def __init_thread_pool(self,thread_num):
	print "Initialing %d threads ..."%(thread_num)
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))

    ###Initialize the queue
    def __init_work_queue(self, jobs_num):
        for i in range(jobs_num):
            self.add_job(do_job, i)

    ### Add one job, Queue contain the synchronization mechanism
    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))

    ### Check the queue
    def check_queue(self):
        return self.work_queue.qsize()

    ### Wait for all threads done
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():
                item.join()

class Work(threading.Thread):
    def __init__(self,work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()
    def run(self):
        while True:
            try:
                do, args = self.work_queue.get(block=False)
                do(args)
                self.work_queue.task_done()
            except Exception,e:
                print str(e)
                break

### The job actually running
def do_job(args):
    id = cLists[args[0]]
    logger = getLogger(id)
    t_start = time.strftime("%Y-%m-%d_%H:%M:%S")
    logger.info("Thread %s, start time: %s"%(args,t_start))
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
    	logger.info("Thread %s, end time: %s"%(args,t_end))
        if flag:
                logger.info("IMPORT RESULT: %s SUCCESSED %s %s %s %s"%(str(id),t_start,t_end,str(exceptNo),cardInfo))
        else:
                logger.info("IMPORT RESULT: %s FAILED %s %s %s %s"%(str(id),t_start,t_end,str(exceptNo),cardInfo))
	sys.stdout.flush()
        if task:
                del task

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

#Insert import results into mysql DB
def insResults(cids):
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
		result = re.findall(rc,contents)
		if len(result) == 0:
			fstat.write("%s %s cannot_import\n"%(id,sqlName))
			continue
		else:
			lists = result[len(result) - 1]
		runTimes = calTime(lists.split()[2],lists.split()[3])
		lstatus = getRecordStatus(sqlName)
		lexcept = getLastExcept(sqlName)
		if lstatus == "SUCCESSED":
			fstat.write("%s %s no_sql_file\n"%(id,sqlName))
			continue
		elif str(lexcept) == '5':
			fstat.write("%s %s local_data_not_equal_with_DX\n"%(id,sqlName))
			continue
		status = lists.split()[1]
		importTime = lists.split()[2]
		exceptType=lists.split()[4]
		sellInfo = re.findall(r"None",lists)
		if exceptType == str(5):
			sell = p1.findall(contents)
			mlist = p2.findall(contents)
			t = mlist[len(mlist)-1]
			sellInfo = "%s  %s  %s"%(sell[len(sell) - 1],t[0],t[1])
		else:
			if sellInfo:
				sellInfo = sellInfo[0]
			else:
				sellInfo=re.findall(r"\((.*?)\)",lists)[0].split(',')
				s1 = round(float(sellInfo[0]),2)
				s2 = round(float(sellInfo[1]),2)
				sellInfo = "%s,%s"%(s1,s2) 
		execNum = getExecNum(sqlName) + 1
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
		print sql
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
    cLists = reschedule_cids(cids)
    cidsNum = len(cLists)
    print "Import %s cinema IDs, lists: %s"%(cidsNum,cLists)
    try:
        saveout = sys.stdout
        saveerr = sys.stderr
        f = open("log/import_record"+time.strftime("%m%d_%H%M%S"),"a")
        sys.stdout = f
        sys.stderr = f
    	print "Import %s cinema IDs, lists: %s"%(cidsNum,cLists)
	for i in range(1):
		print "****** The %d time(s) try... ******"%(i)
        	start = time.strftime("%Y-%m-%d %H:%M:%S")
        	work_manager = WorkManager(cidsNum,8)
        	work_manager.wait_allcomplete()
        	end = time.strftime("%Y-%m-%d %H:%M:%S")
        	print "Process(es) start times: ",start
        	print "Process(es) end times: ",end
    finally:
        print "Statistics the import results and write results into mysql"
        insResults(cLists)
        f.close()
        
