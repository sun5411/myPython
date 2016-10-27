#!/usr/bin/env python
import time,datetime
import re
import sys
import decimal
sys.path.append("../..")
import dbconf
from mysql import MySQL

dbHost=dbconf.g_importDBHost
patt = re.compile(r':(\d+.\d+)')
binDir = "/data0/binlog/"
logDir = "./log/"

def getCheckList(date):
	dbconfig = {'host':dbconf.g_resultDBHost,
	        'port':dbconf.g_resultDBPort,
	        'user':dbconf.g_resultDBUser,
	        'passwd':dbconf.g_resultDBPwd,
	        'db':dbconf.g_resultDBName,
	        'charset':'utf8'}
	db = MySQL(dbconfig)
	print date
	sql = "select cID from import_status_record where curr_sql_date='%s' and status='SUCCESSED'"%(date)
	dbs=db.fetchAllRows(sql)
	print sql
	idList=[]
	for id in dbs:
		sql = "select cID from available_CID where db_host_ip='%s' and cID='%d'"%(dbHost,id[0])
		id = db.fetchOneRow(sql)
		if id:
			idList.append(id[0])
		else:
			continue
	return idList

def getTxtValues(cid,date):
	binlog = "%s%s-%s.txt"%(binDir,cid,date)
	f = open(binlog,'r')
	content = f.read()
	return patt.findall(content)


def getDbValues(cid,date):
	dbName='C' + str(cid)
	dbconfig = {'host':dbconf.g_importDBHost,
	        'port':dbconf.g_importDBPort,
	        'user':dbconf.g_importDBUser,
	        'passwd':dbconf.g_importDBPwd,
	        'db':dbName,
	        'charset':'utf8'}
	db = MySQL(dbconfig)
	#sellLogSql = 'SELECT COUNT(1) FROM cinema_sell_log'
	sellLogSql = "SELECT COUNT(1) FROM cinema_sell_log where cinema_sell_time < '%s 03:00:00'"%(date)
	#cardSql = 'SELECT SUM(cinema_card_balance) FROM cinema_card_info'
	cardSql = "SELECT SUM(cinema_card_balance) FROM cinema_card_info where cinema_update_time < '%s 03:00:00'"%(date)
	#consSql = 'SELECT SUM(cinema_card_balance) FROM cinema_card_consume'
	consSql = "SELECT SUM(cinema_card_balance) FROM cinema_card_consume where cinema_deal_time < '%s 03:00:00'"%(date)
	cSell=db.fetchOneRow(sellLogSql)
	cCard=db.fetchOneRow(cardSql)
	consume=db.fetchOneRow(consSql)
	return [cCard[0],cSell[0],consume[0]]

def check_data(cid,txtList,dbList):
	diff = 10000
	print "--------------------- %s ------------------------"%(cid)
	if len(txtList) == len(dbList):
		if txtList[1] != str(dbList[1]) or abs(decimal.Decimal(txtList[0]) - dbList[0]) > diff or (txtList[2] is not None and str(dbList[2]) != txtList[2]):
			print "###### Check failed, cinema ID ######",cid
		 	print "Cinema ID %s --- Card_sum: %s,%s Sell_count: %s,%s Consume_sum: %s,%s" %(cid,txtList[0],dbList[0],txtList[1],dbList[1],txtList[2],dbList[2])
		else:
			print "Check is ok! cinema ID ",cid
			print "Cinema ID %s --- Card_sum: %s,%s Sell_count: %s,%s Consume_sum: %s,%s" %(cid,txtList[0],dbList[0],txtList[1],dbList[1],txtList[2],dbList[2])
	else:
		print "The data is not complete in txt file"
		print "Txt data : %s , DB data : %s"%(txtList,dbList)
		print "please check %s txt file"%(cid)

if __name__ == "__main__":
	today = datetime.date.today()
	lastDay = today - datetime.timedelta(days = 2)
	endtime = today - datetime.timedelta(days = 1)
	cList=getCheckList(lastDay)
	print "start all %s DBs check"%(len(cList))
	f = open("log/check_record"+time.strftime("%m%d_%H%M%S"),"a")
        sys.stdout = f
        sys.stderr = f
	for cid in cList:
		print "start %s check ,index %s"%(cid,cList.index(cid))
		### [card_sum,sell_count,consume_sum]
		txtList = getTxtValues(cid,lastDay)
		dbList = getDbValues(cid,endtime)
		check_data(cid,txtList,dbList)
	f.close()
