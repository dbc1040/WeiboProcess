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

def print_weibo_content(coll,db_name):

	output_dir = 'DATA//' + db_name 
	DirOperator.DirOperator(output_dir)
	output_dir = output_dir + '//微博内容'
	DirOperator.DirOperator(output_dir)

	cursor = coll.find()
	content_dic = {}
	for c in cursor:
		userId = c['userId']
		if userId in content_dic.keys():
			content_dic[userId]['content'] += c["text"].strip()+'\n'
		else:
			content_dic[userId] = {}
			content_dic[userId]['content'] = c["text"].strip()+'\n'
	# rent_weibo = ''
	for user in content_dic.keys():
		filename = output_dir + os.sep + user + '.txt'
		f = codecs.open(filename,'w','utf-8')
		
		write_con = content_dic[user]['content']

		f.write(write_con)
		print('微博内容输出完毕至'+filename+'文件')
		f.close()

	return

def main():
	# 这个代码作用的将制定数据库中的用户微博导出到“微博内容”文件夹中
	# 以uid作为txt名字
	conn = pymongo.MongoClient(port = 27017)
	cfg = getconfig()
	dbname = cfg['MongoDBConnection']['db']
	weibodb = Dboperator(conn, dbname)
	collname = "UserTimelines"
	coll = weibodb.db[collname]
	WeiboContent_dir = ''
	print_weibo_content(coll,dbname)

main()
