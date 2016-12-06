#coding:utf-8
import pymongo
import os
import codecs
import re
import csv
from config import getconfig
import DirOperator
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

def extract_names_from_text(text):
	'''
	#函数作用是从text中提取出昵称字段，存放在列表中返回
	#输入：文本text
	#输出：昵称列表
	'''
	namelist = {}
	nick_pattern = re.compile(r'@([0-9a-zA-Z\u4e00-\u9fa5_-]*)')
	if nick_pattern.search(text) != None:
		names = nick_pattern.findall(text)
		for name in names:
			if len(name) > 15:
				continue
			if name not in namelist.keys():
				namelist[name] = 1
				# namelist.append(name)
			else:
				namelist[name] += 1
	NickName_list_sorted = sorted(namelist.items(), key=lambda d: d[1], reverse = True)
	return NickName_list_sorted

#函数作用是从数据库中提取昵称，存放在文件中
#输入：数据库的集合collection名称,源UserId
#输出：昵称列表文件namelsit.txt
def ExtractNickNamesfromDB(coll,UserList,db_name):
	cursor = coll.find({},{"userId":1,"text": 1,"oUserId":1})
	NickName_list = list()
	UserList_len = len(UserList)

	output_dir = 'DATA//' + db_name 
	DirOperator.DirOperator(output_dir)

	output_filename =  output_dir + '//extend_users_nick.csv'
	csvfile = open(output_filename,'w',newline="")
	writer = csv.writer(csvfile,dialect='excel')
	writer.writerow(['用户昵称', '权重'])
	# f = open('DATA\\namelsit.txt','w')

	output_filename1 =  output_dir + '//extend_users_uid.csv'
	csvfile1 = open(output_filename1,'w',newline="")
	writer1 = csv.writer(csvfile1,dialect='excel')
	writer1.writerow(['uid', '权重'])
	# f = open('DATA\\namelsit.txt','w')
	text = ""
	oUserId_dic = {}
	for c in cursor:
		userId = c['userId']
		if userId in UserList or UserList_len == 0:
			text += c['text']
		oUserId = c.get('oUserId',"")
		if(oUserId == ""):
			continue
		if oUserId in oUserId_dic.keys():
			oUserId_dic[oUserId] += 1
		else:
			oUserId_dic[oUserId] = 1
	namelist = extract_names_from_text(text)
	for name in namelist:
		writer.writerow([str(name[0]), str(name[1])])
	print("发现用户昵称已存储至"+output_filename+'文件\n')
	csvfile.close()
	oUserId_dic = sorted(oUserId_dic.items(),key = lambda d:d[1],reverse = True)
	for oUserId in oUserId_dic:
		writer1.writerow([str(oUserId[0]),str(oUserId[1])])
	print("发现用户uid已存储至"+output_filename1+'文件\n')
	csvfile1.close()

def main():
	conn = pymongo.MongoClient(port = 27017)

	cfg = getconfig()
	dbname = cfg['MongoDBConnection']['db']
	weibodb = Dboperator(conn, dbname)
	collname = "UserTimelines"

	coll = weibodb.db[collname]
	UserList = list()
	UserList = []
	# text = '嘻嘻] //@DJ小强:哈哈 @韩寒： //@owen： 等嘻] //@DJ小强:哈哈 欢迎郭伯雄和吴敦义，郭伯瑜 @郭靜Claire [偷笑]//@DJ小强全球后援会:帅哥美女的对话，你们都听了吗'
	# list1 = ExtractNamesfromText(text)
	print("开始提取用户\n")
	ExtractNickNamesfromDB(coll,UserList,dbname)
	print("结束提取用户\n")
	# ExtractAllNickNamesfromDir(weibocontentDir)
	# ExtractNickNamesfromDir(weibocontentDir,UserList)

main()