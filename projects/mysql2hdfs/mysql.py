#!/usr/bin/python
#coding:utf8

import MySQLdb
import time
import traceback

class MySQL:
    error_code = ''
    _instance = None
    _conn = None
    _cur = None
    _TIMEOUT = 30
    _timecount = 0

    def __init__(self,dbconfig):
        try:
            self._conn = MySQLdb.connect(host=dbconfig['host'],
                            port=dbconfig['port'],
                            user=dbconfig['user'],
                            passwd=dbconfig['passwd'],
                            db=dbconfig['db'],
                            charset=dbconfig['charset'])
        except MySQLdb.Error,e:
            self.error_code = e.args[0]
            error_msg = 'MySQL error!',e.args[0], e.args[1]
            print error_msg

        self._cur = self._conn.cursor()
        self._instance = MySQLdb

    def query(self,sql):
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
        except MySQLdb.Error,e:
            self.error_code = e.args[0]
            print traceback.format_exc()
            result = False
        return result

    ### for UPDATE and DELETE sql
    def update(self,sql):
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
            self._conn.commit()
        except MySQLdb.Error,e:
            self.error_code = e.args[0]
            print traceback.format_exc()
            result = False
        return result

    def insert(self,sql):
        result = True
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            self._conn.commit()
        except MySQLdb.Error,e:
            self.error_code = e.args[0]
            print traceback.format_exc()
            result = False
        return result

    def fetchAllRows(self,sql):
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            return self._cur.fetchall()
        except MySQLdb.Error,e:
            self.error_code = e.args[0]
            print traceback.format_exc()
            result = False
            return result

    def fetchOneRow(self,sql):
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            return self._cur.fetchone()
        except MySQLdb.Error,e:
            self.error_code = e.args[0]
            print traceback.format_exc()
            result = False
            return result

    def getRowCount(self):
        return self._cur.rowcount

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def __del__(self):
        try:
            self._cur.close()
            self.conn.close()
        except:
            pass
    def close(self):
        self.__del__()

