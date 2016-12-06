from collections import Counter
import pymongo
import os
from config import getconfig
import DirOperator
import codecs
class Dboperator():
	def __init__(self, conn, dbName = ""):
		self.conn = conn
		self.dbName = dbName
		self.db = self.getDb(self.dbName)
	def getDb(self, dbName):
		return self.conn[dbName]
	def get_distinct_value(self, coll, key):
		arrays = self.db[coll].distinct(key)
		return arrays

def time_sort(time_list):
	a = []
	for i in time_list:

		time = i.split(' ')
		if len(time) != 2:
			continue
		time = time[1]
		s = time.split(':')
		a.append(s[0])
	c = Counter(a)
	result_str = ''
	for i in range(0,24):
		if i <= 9:
			i = str(0)+str(i)
		result_str += str(i) + '\t' + str(c[str(i)]) + '\n'
	return result_str
def find_time(coll):
	cursor = coll.find()
	time_list = []
	for c in cursor:
		dateFormart = c['dateFormart']
		time_list.append(dateFormart)
	return time_list
if __name__ == '__main__':
	conn = pymongo.MongoClient(port = 27017)
	cfg = getconfig()
	dbname = cfg['MongoDBConnection']['db']
	weibodb = Dboperator(conn, dbname)
	collname = "UserTimelines"
	coll = weibodb.db[collname]

	time_list = find_time(coll)
	result = time_sort(time_list)
	file_name = 'DATA\\' + dbname + '\\time.txt'
	f = open(file_name,"w")
	f.write(result)
	f.close()
	print(result)
