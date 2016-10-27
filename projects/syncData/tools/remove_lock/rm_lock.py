#!/usr/bin/env python
#coding:utf-8

import sys,os,time
sys.path.append("../..")
import dbconf
from mysql import MySQL

dbHost=dbconf.g_importDBHost
print dbHost
logDir = "/data0/syncdata/log/"
dataDir = "/data0/syncdata/data/"
sqlDir = "/data0/binlog/"
dbconfig = {'host':dbconf.g_resultDBHost,
        'port':dbconf.g_resultDBPort,
        'user':dbconf.g_resultDBUser,
        'passwd':dbconf.g_resultDBPwd,
        'db':dbconf.g_resultDBName,
        'charset':'utf8'}
db = MySQL(dbconfig)
sql1 = "select cID,curr_sql_file from import_status_record where imp_lock_flag=1;"
cids = db.fetchAllRows(sql1)
f=open("./log/remove_log"+time.strftime("%Y-%m-%d"),"a")
f.write("### %s, Remove the cid(s) lock ###\n"%(time.strftime("%H:%M:%S")))
if cids:
	for cid in cids:
		sql = "select cID from available_CID where cID=%d and db_host_ip='%s'"%(cid[0],dbHost)
		sqlFile = cid[1]
		id = db.fetchOneRow(sql)
		#print "Will clean the lock file for %s, current sql file %s"%(cid[0],sqlFile)
		f.write("Will clean the lock file for %s, current sql file %s\n"%(cid[0],sqlFile))
		try:
			if id is None:
				#print "%d is not in local databases!"%(cid[0])
				f.write("%d is not in local databases!\n"%(cid[0]))
				continue
			else:
				#print "%slock_%d"%(dataDir,id[0])
				f.write("%slock_%d\n"%(dataDir,id[0]))
				os.remove("%slock_%d"%(dataDir,id[0]))
		except Exception,e:
			print e
			continue
		finally:
			sql = "update import_status_record set imp_lock_flag=Null where curr_sql_file='%s'"%(sqlFile)
			f.write(sql+"\n")
			db.update(sql)
f.close()
