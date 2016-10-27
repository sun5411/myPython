#!/usr/bin/env python
import dbconf
from mysql import MySQL

f = open("./alldbs")
alldbs = f.readlines()
list = [x.strip('\n').strip('C') for x in alldbs]

dbconfig = {'host':dbconf.g_resultDBHost,
        'port':dbconf.g_resultDBPort,
        'user':dbconf.g_resultDBUser,
        'passwd':dbconf.g_resultDBPwd,
        'db':dbconf.g_resultDBName,
        'charset':'utf8'}
db = MySQL(dbconfig)
sql = "select cID from available_CID;"
existDbs=db.fetchAllRows(sql)
for existDB in existDbs:
	if str(existDB[0]) in list:
		list.remove(str(existDB[0]))
print "Get %s new cids"%len(list)
print list
