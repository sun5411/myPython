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
	#fstat=open(logDir+"exec_results_"+time.strftime("%Y-%m-%d"),"a")
	fstat=open(logDir+"exec_results_2016-07-26","a")
	fstat.write("### Start time : %s, CIDs number: %d ###\n"%(time.strftime("%H:%M:%S"),len(cids)))
	for id in cids:
		sqlName=getSqlName(id)
		file = getFile(str(id))
		print "Read import record from ",max(file)
		fp = open(max(file),"r")
		contents = fp.read()
		sellChange = p0.findall(contents)
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
		print '######',sqlName,lstatus,lexcept
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
			fstat.write("%s %s DELETE FROM cinema_sell_log\n"%(id,sqlName))
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
		print sql
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
    cLists = [11010841L, 11050761L, 11050801L, 11110751L, 11140861L, 11160851L, 12230691L, 12250811L, 13010101L, 13010201L, 13010701L, 13011201L, 13011902L, 13014001L, 13016301L, 13020391L, 13024201L, 13025201L, 13062901L, 13063101L, 13082701L, 13100102L, 13104701L, 14022471L, 14022511L, 14050701L, 14052433L, 14052451L, 14052501L, 14052531L, 14062811L, 14071101L, 14072441L, 14072841L, 14092541L, 14102561L, 14102781L, 14102791L, 14102861L, 14112301L, 14242831L, 15021011L, 21010801L, 21020541L, 21040111L, 21040141L, 21050061L, 21070121L, 21100131L, 22060301L, 22070601L, 22090602L, 22110501L, 22110802L, 23018221L, 23040321L, 23068111L, 31011501L, 31030603L, 31070101L, 31073101L, 31073201L, 31081501L, 31092101L, 31113801L, 31113901L, 31114301L, 31114501L, 31124201L, 31124501L, 31125001L, 31126301L, 31127201L, 31127501L, 31142101L, 31142301L, 31142401L, 31193801L, 31194301L, 32011501L, 32014901L, 32015711L, 32016611L, 32017011L, 32017811L, 32021201L, 32026101L, 32028711L, 32028911L, 32029011L, 32029041L, 32029061L, 32035611L, 32036411L, 32036611L, 32036711L, 32036911L, 32037211L, 32038011L, 32043101L, 32053311L, 32105111L, 32110401L, 32120302L, 32121411L, 33013401L, 33019241L, 33019261L, 33019291L, 33034301L, 33041901L, 33046801L, 33064501L, 33076901L, 33080801L, 33095101L, 34013001L, 34015801L, 34016001L, 34016301L, 34022701L, 34023301L, 34031201L, 34070101L, 34120301L, 34170301L, 34171701L, 35014051L, 35014201L, 35034471L, 35052201L, 35054211L, 35084121L, 36010501L, 36010801L, 36012401L, 36113901L, 37027081L, 37027142L, 37037071L, 37047051L, 37057061L, 37063001L, 37063101L, 37063201L, 37067031L, 37067061L, 37067101L, 37070101L, 37080101L, 37082101L, 37082501L, 37087141L, 37101201L, 37107031L, 37127051L, 37132001L, 37137021L, 37137051L, 37137061L, 37137071L, 37157021L, 37157041L, 41016501L, 41016601L, 41033001L, 41033701L, 41181201L, 42032601L, 42041301L, 42052601L, 42052701L, 42072201L, 42092501L, 42092601L, 42101101L, 42102501L, 42150701L, 43140701L, 44001081L, 44001291L, 44005201L, 44011211L, 44011281L, 44011291L, 44011411L, 44011421L, 44011611L, 44071601L, 44072001L, 44083601L, 44091101L, 44108201L, 44136001L, 44136701L, 44136801L, 44137501L, 44141502L, 44151601L, 44151801L, 44170601L, 45030101L, 45030281L, 45030291L, 45030351L, 45030361L, 45090071L, 45090081L, 45110101L, 45140021L, 45140041L, 46050101L, 46130101L, 50020071L, 50030501L, 50050602L, 50060111L, 50060121L, 50060801L, 50070121L, 50080021L, 50090061L, 50120221L, 50120501L, 50160021L, 50340051L, 50340401L, 50420201L, 51010111L, 51010201L, 51010401L, 51010601L, 51011231L, 51011701L, 51011801L, 51012001L, 51012501L, 51015201L, 51018001L, 51020601L, 51020701L, 51030021L, 51040021L, 51040031L, 51040201L, 51050301L, 51060301L, 51068101L, 51068301L, 51068501L, 51068601L, 51069971L, 51083201L, 51090401L, 51090501L, 51090701L, 51120501L, 51128901L, 51130010L, 51130401L, 51130601L, 51139971L, 51140021L, 51140501L, 51150401L, 51165101L, 51190011L, 52012901L, 52013001L, 52013301L, 52032101L, 52032701L, 52221701L, 53010801L, 53014401L, 53015501L, 53031701L, 61014801L, 61015201L, 61015701L, 61015901L, 61016001L, 61016201L, 61016301L, 61016401L, 61016501L, 61017101L, 61017201L, 61031901L, 61051201L, 61060701L, 61061201L, 61070901L, 61071001L, 61071501L, 61080401L, 61081001L, 61090201L, 61091501L, 61091601L, 61091901L, 61100701L, 61100801L, 62012801L, 62012901L, 62013101L, 62020601L, 62020801L, 62030401L, 62030601L, 62040601L, 62041001L, 62050501L, 62060301L, 62060801L, 62070801L, 62080301L, 62080501L, 62090201L, 62090301L, 62100301L, 62110301L, 62141201L, 63010202L, 63010402L, 63050021L]
    cidsNum = len(cLists)
    print "Import %s cinema IDs, lists: %s"%(cidsNum,cLists)
    for i in range(1):
    	#processPools(cidsNum,1)
    	insResults(cLists)
