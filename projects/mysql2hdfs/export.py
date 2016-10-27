#flag = True!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
  Purpose: 从mysql查询结果并保存为文件
  Created: 2016/10/11
  Modified:2016/10/11
"""


#导入模块
from mysql import MySQL
import time
import os,sys
import datetime
import sqlConf
import logging
from multiprocessing import Pool
import traceback
import pdb

#日期
today = datetime.date.today()
yestoday = today - datetime.timedelta(days=1)

#对账日期
checkAcc_date = yestoday.strftime('%Y%m%d')

### 计算时间
def get_newTime(t,dur):
    t1 = datetime.datetime.strptime(t,"%Y-%m-%d %H:%M:%S")
    t2 = t1 + datetime.timedelta(minutes=dur)
    now = datetime.datetime.now()
    if not (t2 < now):
	t2 = None
    return t2

### 计算时间差
def calTime(start,end):
        start=time.strptime(start,"%Y-%m-%d %H:%M:%S")
        end=time.strptime(end,"%Y-%m-%d %H:%M:%S")
        start=datetime.datetime(start[0],start[1],start[2],start[3],start[4],start[5])
        end=datetime.datetime(end[0],end[1],end[2],end[3],end[4],end[5])
        return end-start


hdfsBase="/user/business/sync/30"
logDir = "logs/"
metaDir = "meta/"
hdfsTimeFile = metaDir + 'hdfs_time'
hf = open(hdfsTimeFile,'r')
t = hf.readline().strip('\n').split('\t')[0]
hf.close()
hdfsNewTime = get_newTime(t,30)
fileDir = "expData/%s"%(hdfsNewTime.strftime('%Y%m%d_%H%M%S'))
reStr1="startTime"
reStr2="endTime"
if not os.path.exists(fileDir):
    os.makedirs(fileDir)
if not os.path.exists(logDir):
    os.makedirs(logDir)
if not os.path.exists(metaDir):
    os.makedirs(metaDir)

opers = ['sell','refund','sell_add','pay','order']

# replace the time string with sqls
def replaceSqlTime(t1,t2):
    s1 = sqlConf.sql1.replace(reStr1,t1)
    s1 = s1.replace(reStr2,t2)
    s2 = sqlConf.sql2.replace(reStr1,t1)
    s2 = s2.replace(reStr2,t2)
    s3 = sqlConf.sql3.replace(reStr1,t1)
    s3 = s3.replace(reStr2,t2)
    s4 = sqlConf.sql4.replace(reStr1,t1)
    s4 = s4.replace(reStr2,t2)
    s5 = sqlConf.sql5.replace(reStr1,t1)
    s5 = s5.replace(reStr2,t2)
    return [s1,s2,s3,s4,s5]


def getLogger(cid):
        logger = logging.getLogger(str(cid))
        todayStr = str(today)
        processDir = os.path.dirname(os.path.abspath(sys.argv[0]))
        fn = processDir+'/'+logDir + str(cid)+'_'+todayStr+'.log'
        handler = logging.FileHandler(fn)
        formatter = logging.Formatter('[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s]  %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger;

### get cinema DB list
def getTask_list():
    sql = "select dc_ip,cinema_num from cinema_info where flag=1 and dc_ip is not NULL and dc_ip='10.10.1.30'"
    dbconfig = {'host':'10.10.0.90',
        'port':3306,
        'user':'read',
        'passwd':'yhz#read',
        'db':'cinema',
        'charset':'utf8'}
    db = MySQL(dbconfig)
    return db.fetchAllRows(sql)

def exec_record(cid,flag,t_start,logger,lastEndTime,endTime,rows):
    status = None
    if flag:
       status = 'SUCCESSED' 
    else:
       status = 'FAILED' 
    sql = "select tried_num from export_status_record where cID=%s and exec_time = '%s'"%(cid,t_start)
    dbconfig = {'host':'10.10.1.19',
        'port':3306,
        'user':'caofei',
        'passwd':'caofei',
        'db':'cinema_imp_record',
        'charset':'utf8'}
    expDb = MySQL(dbconfig)
    triedNum = expDb.fetchOneRow(sql)
    if not triedNum:
            triedNum = 0
    else:
            triedNum = expDb.fetchOneRow(sql)[0]
    runTimes = calTime(t_start,time.strftime("%Y-%m-%d %H:%M:%S"))
    sql="INSERT INTO export_status_record \
                (cID,status,exec_time,last_end_time,duration,tried_num,curr_end_time,fetch_rows) \
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s');"\
                %(cid,status,t_start,lastEndTime,runTimes,triedNum+1,endTime,','.join(rows))
    try:
        logger.info('Record the insert info, execute result : %s'%status)
        expDb.insert(sql)
    except Exception, e:
        logger.error(traceback.format_exc())
    finally:
        expDb.close()
    


### The job
def do_job(args):
    host = workList[args][0]
    id = workList[args][1]
    logger = getLogger(id)
    t_start = time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info("Process %s, start time: %s"%(args,t_start))
    task = None
    flag = True
    try:
        task = dbExport(id,host,logger,60)
        flag = task.doExtractDb()
        print "cid %s,task  %s :"%(str(id),args) + ','.join(task.rows)
    	exec_record(id,flag,t_start,logger,task.lastEndTime,task.endTime,task.rows)    
    except Exception, e:
        flag = False
    	exec_record(id,flag,t_start,logger,task.lastEndTime,task.endTime,task.rows)    
        logger.error(traceback.format_exc())
    finally:
        t_end = time.strftime("%Y-%m-%d %H:%M:%S")
        logger.info("Process %s, end time: %s"%(args,t_end))
        if flag:
            logger.info("EXPORT RESULT: %s SUCCESSED %s %s"%(str(id),t_start,t_end))
        else:
            logger.info("EXPORT RESULT: %s FAILED %s %s"%(str(id),t_start,t_end))
        if task:
            del task

### The process(es) pool
def processPools(work_num=10,pro_num=4):
    pool = Pool(processes=pro_num)
    for i in range(work_num):
        print "Processing with %s/%s ..."%(i+1,str(work_num))
        result = pool.apply_async(do_job, (i,))
    pool.close()
    pool.join()
    if result.successful():
        print 'All tasks is done!'

### upload exported file into hdfs 
def load_into_hdfs(newTime):
    #1. get last hdfs time record, and calculte the new end time 
    sqlTime = newTime.strftime('%Y%m%d_%H%M%S')
    hdfsRecordTime = newTime.strftime('%Y-%m-%d %H:%M:%S')
    # 2. create hdfs dir, and put export data into the correspond dir
    for oper in opers:
        sourceDir = '%s' %(fileDir)
        destDir = '%s/%s'%(hdfsBase,oper)
        sourceFile = '%s/sql_%s_*'%(sourceDir,oper)
        destFile = '%s/%s_%s.txt'%(destDir,oper,sqlTime)
        #cmd1="hadoop fs -mkdir %s"%(destDir)
        cmd2="cat %s |hadoop fs -put -f /dev/fd/0 %s"%(sourceFile,destFile)
        #cmd4="hadoop fs -test -e %s"%(destDir)
        cmd5="ls -la  %s |awk 'BEGIN{sum=0}{sum=sum+$5} END{print sum/1024}'"%(sourceFile)
        flag = True
        try:
            ret5 = os.popen(cmd5).readline().strip('\n')
            if ret5 == '0':
                print "%s is empty!!"%cmd5
                continue
            #ret4 = os.system(cmd4)
            #ret1 = None
            #if ret4 == 0:
            #    ret1 = 0
            #else:
            #    ret1 = os.system(cmd1)

            #if ret1 == 0:
            #    ret2 = os.system(cmd2)
            #    if ret2 != 0:
            #        flag = False
            #        raise Exception("Error : upload sourceFile (%s) into hdfs dir (%s) failed !"%(sourceFile,destFile))
            #else:
            #    flag = False
            #    raise Exception("Error : Create hdfs %s failed!"%(destDir))
            ret2 = os.system(cmd2)
            if ret2 != 0:
                flag = False
                raise Exception("Error : upload sourceFile (%s) into hdfs dir (%s) failed !"%(sourceFile,destFile))
    	except Exception, e:
    	    print traceback.format_exc()
    # generate SUCCESS file after extend file uploaded
    succFile='%s/_SUCCESS_%s'%(hdfsBase,sqlTime)
    print succFile
    cmd3 = 'hadoop fs -touchz %s'%(succFile)
    if flag:
        os.system(cmd3)
        f = open(hdfsTimeFile,'r+')
        f.seek(0)
        f.truncate()
        print 'hdfsRecordTIme : ' + hdfsRecordTime
        f.write(hdfsRecordTime)
        f.close()
    else:
        print "Error : upload exported data into hdfs failed!!!"

### do export task
class dbExport:
    lastEndTime = ''
    endTime = ''
    rows = []
    def __init__(self, cid, host, logger,interval):
        self.__lock = False
        self.__dbConn = None
        self.__recordFD = None
        self.__record = None
        self.__dbName = 'C' + str(cid)
        self.__rName = 'record_'
        self.__cid = cid
        self.__host = host
        self.__sqls = None
        self.__lName = 'lock_'
        self.__logger = logger
        self.__endTime = None

        #1. check lock file
        lf = metaDir+self.__lName+str(self.__cid)
        if os.path.exists(lf):
            self.__logger.error("import process is running and exit now, lock file="+lf)
        else:
            os.mknod(lf)
            self.__lock = True
          
        results=''
        filename=''
        #2. create db connector
        dbconfig = {'host':self.__host,
                'port':3306,
                'user':'queryuser',
                'passwd':'123456',
                'db':self.__dbName,
                'charset':'utf8'}
        self.__dbConn = MySQL(dbconfig)

        #3.check and read record file
        absRecord = metaDir+self.__rName+str(self.__cid)
        if os.path.exists(absRecord) is False or os.path.isfile(absRecord) is False:
                self.__logger.error("record file is not exists or not file. record file="+absRecord)

        fd = open(absRecord, 'r')
        self.__record = fd.readline().strip('\n').split('\t')
        self.lastEndTime = self.__record[0]
        if not self.__record:
                self.__logger.error("read no record from record file="+absRecord)
        fd.close()
        self.__logger.info("Last end time : " + str(self.__record))

        #4.open record file with write mode
        self.__recordFD = open(absRecord, 'r+')

        ###Re-calculate endTime
        self.endTime=get_newTime(self.lastEndTime,interval).strftime('%Y-%m-%d %H:%M:%S')
        self.__logger.info("This end time : " + self.endTime) 
        self.__sqls = replaceSqlTime(self.lastEndTime,self.endTime)

        self.__endTime = self.endTime

    def __dumpRecord(self):
        self.__recordFD.seek(0)
        self.__recordFD.truncate()
        self.__recordFD.write(self.__endTime)

    def __del__(self):
        self.cleanResource()
        self.__logger.info("del sqlImport instance")

    def cleanResource(self):
        if self.__recordFD :
                self.__recordFD.close()

        absLock = metaDir+self.__lName+str(self.__cid)
        if os.path.exists(absLock) and self.__lock is True:
                os.remove(absLock)

        if self.__dbConn:
                self.__dbConn.close()
    ### interval unit : minute
    def doExtractDb(self):
    	execFlag = False
    	self.rows = []
    	try:
    	    if not self.endTime:
    	        raise Exception("Time Error: already latest timer, Please wait 1 hours later to try again!")
    	    for i in range(len(self.__sqls)):
    	    #获取数据
    	        #filename = '%s/sql_%s_%s_%s.txt' %(fileDir,opers[i],self.__cid, datetime.datetime.strptime(self.__endTime).strftime('%Y-%m-%d_%H:%M:%S'))
    	        filename = '%s/sql_%s_%s_%s.txt' %(fileDir,opers[i],self.__cid, self.__endTime.replace(' ', '_'))
    	        self.__logger.info("%s, start to get %s info from db %s" %(time.strftime('%Y-%m-%d %H:%M:%S'),opers[i],self.__cid))
    	        results = self.__dbConn.fetchAllRows(self.__sqls[i])
    	        if (results == 'F'):
    	            raise Exception("SqlError : the quiery failed from DB!")
    	    #创建汇总日账单文件名称
    	      
    	        self.rows.append("%s:%s"%(opers[i],len(results)))
    	        self.__logger.info('The file %s start generating! %s'  %(filename,time.strftime('%Y-%m-%d %H:%M:%S')))
    	    #判断文件是否存在, 如果存在则删除文件,否则生成文件！
    	        if os.path.exists(filename):
    	            os.remove(filename)
    	      
    	        outfile = open(filename,'w')
    	        for result in results:
    	            newStr = ''
    	            for block in result: 
    	                if not block:
    	                	block = "''"
    	                elif isinstance(block, unicode):
    	                    block = block.encode('utf-8')
    	                else:
    	                    block = str(block)
    	                if not newStr:
    	                    newStr = block
    	                else:
    	                    newStr = newStr + "$#$" + block
    	    
    	            outfile.write('%s\n'%(newStr))
    	            
    	        outfile.flush()
    	        self.__logger.info('The file %s has been generated!  %s' %(filename,time.strftime('%Y-%m-%d %H:%M:%S')))
    	        self.__dumpRecord()
    	        execFlag = True
    	except Exception, e:
    	    self.__logger.error(traceback.format_exc())
    	finally:
    	    self.__dbConn.close()
    	    return execFlag

if __name__ == "__main__":
    workList=getTask_list()
    #workList=[('10.10.1.30',11050911),('10.10.1.30',35084121),('10.10.1.30',46130101),('10.10.1.30',45010601),('10.10.1.30',46170101)]
    workNum = len(workList)
    f = open(logDir+"export_"+time.strftime("%m%d_%H%M%S"),"a")
    try:
        saveout = sys.stdout
        saveerr = sys.stderr
        sys.stdout = f
        sys.stderr = f
        print "Start export %s cinema DBs..."%(workNum)
        print "Start export %s cinema DBs: %s"%(workNum,workList)
        start = time.strftime("%Y-%m-%d %H:%M:%S")
        processPools(workNum,2)
        end = time.strftime("%Y-%m-%d %H:%M:%S")
        print "Process(es) start times: ",start
        print "Process(es) end times: ",end
        print "load data into hdfs..."
        load_into_hdfs(hdfsNewTime)
    except Exception, e:
        print "error msg:",e
    finally:
        f.close()
