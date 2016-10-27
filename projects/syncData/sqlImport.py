#encoding=utf-8


import commands
import os, shutil
import sys
import logging
import logging.config
import MySQLdb
import traceback
from datetime import *
import re

import dbconf
from CustomException import *

#logging.config.fileConfig("logger.conf")
#logger = logging.getLogger("root")
reload(sys)
sys.setdefaultencoding("utf-8")

def getLogger(cid):
	logger = logging.getLogger(str(cid))

	todayStr = str(date.today())
	processDir = os.path.dirname(os.path.abspath(sys.argv[0]))
	fn = processDir+'/log/'+str(cid)+'_'+todayStr+'.log'
	handler = logging.FileHandler(fn)
	formatter = logging.Formatter('[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s]  %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.setLevel(logging.DEBUG)
	return logger;


class SqlImport:
	
	__binlogDir = '/data0/binlog/'
	__dataDir='./data/'  # must end with '/'

	commentFormat = re.compile('^/\*!\\\C\sutf8\s\*//\*!\*/')
	commentFormat_1 = re.compile('\/\*!40019 SET @@session.max_insert_delayed_threads=\d\*\/')
	endFormat = re.compile('/\*!\*/;$')
	binlogEnd = re.compile('SESSION.PSEUDO_SLAVE_MODE=0\*/;$')
	binlogEnd2 = re.compile('^DELIMITER ;')
	binlogEnd3 = re.compile('^DELIMITER ;DELIMITER')
	binlogEnd_1 = re.compile('^DELIMITER ;ROLLBACK \/\* added by mysqlbinlog \*\/;\/\*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE\*\/;$')
	cineFilter = re.compile('`cine`\.')
	#skipOper= re.compile(r'INSERT INTO `user` (`Host`, `User`')
	#cardSumExcept = 20000

	def __init__(self, cinemaId, logger):
		self.__lockFile = 'lock_'  # just for only one process running on single node, multi nodes need ZK lock
		self.__lock = False
		self.__errLock = False

		self.__recordFile = 'record_'
		self.__recordFD = None
		self.__record = None

		self.__signFD = None

		self.__backSqlFile = 'sql_'
		self.__backSqlFD = None

		self.__cardDX = 0.0
		self.__cardLO = 0.0

		#self.__backRDSQLFile = 'rdsql_'
		#self.__backRDSQLFD = None
		
		self.__dbConn = None
		self.__dbCurs = None
		self.__dbName = None
	
		self.__cinemaId = cinemaId
		self.__logger = logger
		#1. change work dir
		homeDir = os.getcwd()
		processDir = os.path.dirname(os.path.abspath(sys.argv[0]))  #os.path.abspath(sys.argv[0])
		if homeDir != processDir :
			self.__logger.info("cd "+processDir+" from "+homeDir)
			os.chdir(processDir)
		self.__homeDir = processDir		

		#2. check and create data dir
		if os.path.exists(self.__dataDir) is False or os.path.isdir(self.__dataDir) is False:
			os.makedirs(self.__dataDir)
		
		#3. check lock file
		absLock = self.__dataDir+self.__lockFile+str(self.__cinemaId)
		if os.path.exists(absLock):
			raise CustomException("import process is running and exit now, lock file="+absLock)
		else:
			os.mknod(absLock)
			self.__lock = True

		#4.check and read record file
		absRecord = self.__dataDir+self.__recordFile+str(self.__cinemaId)
		if os.path.exists(absRecord) is False or os.path.isfile(absRecord) is False:
			raise CustomException("record file is not exists or not file. record file="+absRecord)

		fd = open(absRecord, 'r')
		self.__record = fd.readline().strip('\n').split('\t')
		if not self.__record:
			raise CustomException("read no record from record file="+absRecord)
		fd.close()
		self.__logger.info(self.__record)
		self.__record[1] = int(self.__record[1])		


		#5. set dbName
		items = self.__record[0].split('-')
		self.__dbName = 'C'+items[0]

		#6. open record file with write mode
		self.__recordFD = open(absRecord, 'r+')

		#7. create DB connection
		self.__connDB()
		
		#8. open sql back log
		self.__backSqlFile = self.__dataDir+self.__backSqlFile+str(self.__cinemaId)+'_'+datetime.now().strftime('%Y-%m-%d')
		self.__backSqlFD = open(self.__backSqlFile, 'a')

		#self.__backRDSQLFile = self.__dataDir+self.__backRDSQLFile+str(self.__cinemaId)+'_'+datetime.now().strftime('%Y-%m-%d')
		#self.__backRDSQLFD = open(self.__backRDSQLFile, 'a')

	def __del__(self):
		self.cleanResource()
		self.__logger.info("del sqlImport instance")

	def getRecords(self):
		return self.__record

	def getCardSum(self):
		return  (round(self.__cardLO,2), round(self.__cardDX,2))

	''' 
	create db connection 
	'''
	def __connDB(self):
		if self.__dbConn:
			self.__dbConn.close()
		if self.__dbCurs:
			self.__dbCurs.close()

		self.__dbConn = MySQLdb.connect(host=dbconf.g_importDBHost, user=dbconf.g_importDBUser, passwd=dbconf.g_importDBPwd, db=self.__dbName, port=dbconf.g_importDBPort, charset="utf8")
		self.__dbCurs = self.__dbConn.cursor()
		self.__dbConn.autocommit(1)
		
	
	def countFileLine(self, fileName):
		return int(os.popen('wc -l '+ fileName).read( ).split( )[0])
	


	'''
	fileName : 51010101-2015-11-27.sql
	'''
	def __getNextFile(self, fileName):
		items = fileName.split('-')
		days = items[3].split('.')
		last = datetime.strptime(items[1]+'-'+items[2]+'-'+days[0],'%Y-%m-%d')
		nextDay = last+ timedelta(days=1)
		self.__logger.info('last='+last.strftime('%Y-%m-%d')+', nextDay='+nextDay.strftime('%Y-%m-%d'))

		prefixStr = items[0]+'-'+nextDay.strftime('%Y-%m-%d')
		fn = prefixStr+'.sql'
		return (fn, 0)
	

		
	def __checkMD5SumAndUnzip(self):
		if os.path.exists(self.__binlogDir+self.__record[0]+'.gz'):
			cmd = 'cd '+self.__binlogDir +' &&  md5sum '+self.__record[0]+'.gz'
			(status, output) = commands.getstatusoutput(cmd)
			if status != 0:
				self.__errLock = True
				raise Shell_RUN_EXCEPTION(cmd)
			self.__logger.info(cmd)
			
			
			fn = self.__record[0].split('.')[0]+'.txt'
			self.__signFD = open(self.__binlogDir+fn)
			md5Str = self.__signFD.readline()
			md5Str = md5Str.split(' ')[0]
			print "### record:",self.__record[0]
			pattern = re.compile('^'+md5Str)
			if pattern.search(output) is None:
				self.__errLock = True
				raise MD5_NOT_SAME_EXCEPTION()

			cmd = 'cd '+self.__binlogDir + ' &&  gunzip '+self.__record[0]+'.gz'
			(status, output) = commands.getstatusoutput(cmd)
			if status != 0 :
				self.__errLock = True
				raise Shell_RUN_EXCEPTION(cmd)
			self.__logger.info(cmd)
			

	'''
	check local db with DX db
	'''
	def __checkLocalDBwithDXDB(self):
		if self.__signFD is None:	
			fn = self.__record[0].split('.')[0]+'.txt'
			self.__signFD = open(self.__binlogDir+fn)
			self.__signFD.readline()

		statStr = self.__signFD.readline()
		statItems = statStr.split(' ')
		self.__logger.info(statItems)
		cardSum = statItems[0].split(':')[1]
		if cardSum == 'NULL':
			cardSum='0.0'
		sellCount = statItems[2].split(':')[1]
		consumeSum = None
		if len(statItems)==5  and statItems[4] is not None:
			consumeSum = statItems[4].split(':')[1]
			consumeSum = consumeSum.strip('\n')
			if consumeSum == 'NULL':
				consumeSum = '0.0'

		today = str(date.today())
		sellLogSql = "SELECT COUNT(1) FROM cinema_sell_log where cinema_sell_time < '%s 03:00:00'"%(today)
		self.__dbCurs.execute(sellLogSql)
		sellLogResult = self.__dbCurs.fetchone();
		sellLogResult = int(sellLogResult[0])
		cardSql = "SELECT SUM(cinema_card_balance) FROM cinema_card_info where cinema_update_time < '%s 03:00:00'"%(today)
		self.__dbCurs.execute(cardSql)
		cardResult = self.__dbCurs.fetchone();
		if cardResult[0] is None:
			cardResult = 0.0
		else:
			cardResult = float(cardResult[0])
		consSql = "SELECT SUM(cinema_card_balance) FROM cinema_card_consume where cinema_deal_time < '%s 03:00:00'"%(today)
		self.__dbCurs.execute(consSql)
		consResult = self.__dbCurs.fetchone();
		if consResult[0] is None:
			consResult = 0.0
		else:
			consResult = float(consResult[0])
		

		self.__cardDX = float(cardSum)
		self.__cardLO = cardResult

		self.__logger.info('%s\t[sellCount:%s, %s] [cardSum:%s, %s] [consumeSum:%s, %s]'%(str(self.__cinemaId), str(sellLogResult), str(sellCount), str(cardResult), str(cardSum), str(consResult), str(consumeSum)))

		#if sellLogResult != int(sellCount) or abs(cardResult - float(cardSum)) > self.cardSumExcept or (consumeSum is not None and consResult != float(consumeSum)) :	
		if sellLogResult != int(sellCount) or (consumeSum is not None and consResult != float(consumeSum)) :	
			self.__errLock = True
			raise LOCAL_NOT_EQUAL_DX()


	'''
	backup sql log
	'''
	def __backupFile(self):
		if os.path.exists(self.__dataDir+'bak') is False:
			os.mkdir(self.__dataDir+'bak')
		shutil.move(self.__backSqlFile, self.__dataDir+'bak/'+self.__record[0])


	'''
	 get last records
	'''
	def runDumpDB(self):
		if not self.__record:
			raise CustomException("no read record for record file="+self.__recordFile)
		
		##1. check record binlog file
		absData=self.__binlogDir+self.__record[0]
		print "##record:",self.__record[0]
		if os.path.exists(absData) is False:
			if os.path.exists(absData+'.gz'):
				self.__checkMD5SumAndUnzip()
			else:
				raise CustomException("data is not existsed. file="+absData)
		
		##2. compute whether or not need to open new binlog file 
		fileSize = os.path.getsize(absData)
		if fileSize < self.__record[1] :
			raise CustomException("writed bigger than file number. fileSize=%d, writed=%d"%(fileSize, self.__record[1]))
		elif fileSize == self.__record[1] :
			self.__record = list(self.__getNextFile(self.__record[0]))
			self.__checkMD5SumAndUnzip()

		##3. open binlog
		absData=self.__binlogDir+self.__record[0]
		if  os.path.exists(absData) is False:
			raise CustomException("data is not existsed. file="+absData)
		fd = open(absData, 'r')
		fd.seek(self.__record[1])
		isNeedRun = False
		tmpSql = ''
		while fd.tell()<fileSize :
			self.__logger.info("current Position: %d, %d" %(fd.tell(), fileSize))
			if isNeedRun is True:
				tmpSql = ''

			flag = False
			for line in fd.readlines(dbconf.g_importRDSize):
				#self.__backRDSQLFD.write(line)
				self.__record[1] = self.__record[1] + len(line)
				if self.commentFormat.search(line) or self.commentFormat_1.search(line):
					self.__logger.info("================"+line)
					continue
				elif self.endFormat.search(line):
					isNeedRun = True
				else:
					isNeedRun = False

				line = line.strip('\n')
				line=self.cineFilter.sub('', line)
				tmpSql = tmpSql + line
				if isNeedRun is True :
					if r'INSERT INTO `user` (`Host`, `User`'.lower() in tmpSql.lower():
						tmpSql = ''
						continue
                                	# zhenliang add 
                                	elif r'DROP TABLE IF EXISTS'.lower() in tmpSql.lower():
                                	        tmpSql = ''
                                	        continue
                                	elif r'DROP TEMPORARY TABLE'.lower() in tmpSql.lower():
                                	        tmpSql = ''
                                	        continue
                                	#elif r'CREATE TABLE `user` ('.lower() in tmpSql.lower():
                                	elif r'CREATE TABLE '.lower() in tmpSql.lower():
                                	        tmpSql = ''
                                	        continue
                                	elif r'UPDATE mysql.`user`'.lower() in tmpSql.lower():
                                	        tmpSql = ''
                                	        continue
                                	elif r'UPDATE `user` SET'.lower() in tmpSql.lower():
                                	        tmpSql = ''
                                	        continue
                                	elif r'CHANGE `variable_key` `variable_key` varchar'.lower() in tmpSql.lower():
                                	        tmpSql = ''
                                	        continue
                                	elif r'GRANT REPLICATION'.lower() in tmpSql.lower():
                                	        tmpSql = ''
                                	        continue
                                	# zhenliang end
					elif r'DELETE FROM `cinema_sell_log`'.lower() in tmpSql.lower() or r'DELETE FROM cinema_sell_log'.lower() in tmpSql.lower():
						self.__logger.info("DELETE FROM cinema_sell_log: %s"%(tmpSql))
						tmpSql = ''
						continue
					elif r'C gbk'.lower() in tmpSql.lower():
						tmpSql = ''
						continue
					elif r'WHERE cinema_common_info_key = '.lower() in tmpSql.lower():
						tmpSql = ''
						continue
					elif r'GRANT SELECT'.lower() in tmpSql.lower():
						tmpSql = ''
						continue
					elif re.findall(r'CREATE DEFINER=(.*) FUNCTION'.lower(),tmpSql.lower()):
						tmpSql = ''
						continue
					elif self.binlogEnd3.search(tmpSql) is None:
						tmpSql.strip('/*!*/;')
						self.__importDB(tmpSql)
						self.__dumpRecord()
					tmpSql = ''
				flag = True
			
			if flag is False :
				break
		
		self.__logger.info(tmpSql)
		if tmpSql is not None and (self.binlogEnd_1.search(tmpSql) or (self.binlogEnd2.search(tmpSql) is not None  and self.binlogEnd.search(tmpSql) is not None)):
			self.__dumpRecord()
			self.__checkLocalDBwithDXDB()
			self.__backupFile()
		

	def __dumpRecord(self):
		self.__recordFD.seek(0)
		self.__recordFD.truncate()
		self.__recordFD.write(self.__record[0]+'\t'+str(self.__record[1]))

	def __importDB(self, sql):
		try:
			self.__dbCurs.execute(sql)
			self.__dumpRecord()

			self.__backSqlFD.write(sql)
			self.__backSqlFD.write('\n#=======================\n')
		except Exception, e:
			self.__logger.info('err:'  + sql)
			errStr = str(e)
			if 'Commands out of sync' in errStr:
				raise SQL_2014(errStr)
			elif 'Duplicate entry' in errStr:
				raise SQL_1062(errStr)
			elif 'You have an error in your SQL syntax' in errStr:
				raise SQL_1064(errStr)
			elif 'Lost connection to MySQL server during query' in errStr:
				raise SQL_2013(errStr)
			elif 'The BINLOG statement of type `Table_map`' in errStr:
				self.__logger.info("SQL_1609: " + errStr)
				#raise SQL_1609(errStr)
                        elif re.findall(r'''1146, "Table (.*) doesn't exist''',errStr):
                                print errStr
                                sys.exc_clear()
                        elif re.findall(r'''1054, "Unknown column (.*) in 'field list'"''',errStr):
                                print errStr
                                sys.exc_clear()
			else:
				raise e


	def cleanResource(self):
		if self.__recordFD :
			self.__recordFD.close()
		if self.__backSqlFD:
			self.__backSqlFD.close()
		
		absLock = self.__dataDir+self.__lockFile+str(self.__cinemaId)
		if os.path.exists(absLock) and self.__lock is True and self.__errLock is False: 
			os.remove(absLock)
		
		if self.__dbConn:
			self.__dbConn.close()
		if self.__dbCurs:
			self.__dbCurs.close()

		if self.__signFD:
			self.__signFD.close()


	def runShell(self):
		(status, output)=commands.getstatusoutput('ls /bin/ls')
		return (status, output)

if  __name__ == "__main__":
	
	cid = 11010661
	logger = getLogger(cid)
	task = None
	try:
		task = SqlImport(cid, logger)
		task.runDumpDB()

	except Exception, e:
		logger.info(traceback.format_exc())
	finally:
		if task:
			del task

