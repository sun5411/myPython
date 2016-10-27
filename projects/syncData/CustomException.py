class CustomException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class DB_cinema_movie_show_seat_stat(Exception):
	def __init__(self):
		self.value = 'cinema_movie_show_seat_stat'

	def __str__(self):
		return repr(self.value)

class Shell_RUN_EXCEPTION(Exception):
	def __init__(self, value):
		self.value = 'run shell err:'+value
	def __str__(self):
		return repr(self.value)

class MD5_NOT_SAME_EXCEPTION(Exception):
	def __init__(self):
		self.value = 'check md5 err'
	def __str__(self):
		return repr(self.value)

class LOCAL_NOT_EQUAL_DX(Exception):
	def __init__(self):
		self.value = 'local data is not equal with DX'
	def __str__(self):
		return repr(self.value)
	
class SQL_2014(Exception):
	def __init__(self,value):
		self.value = 'Commands out of sync, SQL err code: 2014' + value
	def __str__(self):
		return repr(self.value)
	
class SQL_1062(Exception):
	def __init__(self,value):
		self.value = 'Duplicate entry, SQL err code : 1062' + value
	def __str__(self):
		return repr(self.value)
class SQL_1064(Exception):
	def __init__(self,value):
		self.value = 'You have an error in your SQL syntax, SQL err code : 1064' +value
	def __str__(self):
		return repr(self.value)
class SQL_2013(Exception):
	def __init__(self,value):
		self.value = 'Lost connection to MySQL server during query, SQL err code : 2013' +value
	def __str__(self):
		return repr(self.value)
class SQL_1609(Exception):
	def __init__(self,value):
		self.value = 'The BINLOG statement of type `Table_map` was not preceded by a format description BINLOG statement, SQL err code : 1609' + value
	def __str__(self):
		return repr(self.value)
