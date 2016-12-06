# -*- coding: utf-8 -*-
import jieba
import jieba.analyse
import glob
import re
from config import getconfig
import DirOperator
def get_all_weibo_keywords(file_name):
    txt_filenames = glob.glob(file_name+'微博内容\\*.txt')
    txt = ''
    for txt_filename in txt_filenames:
        content = open(txt_filename,'r',encoding = 'utf-8').read()
        num = re.findall(r'\d+|\.+',content)
        for everynum in num:
            content = content.replace(everynum,'')
        txt += content 
    topK = 100
    withWeight = True
    jieba.analyse.set_stop_words('stopwords')
    tags = jieba.analyse.extract_tags(txt, topK=topK,withWeight=withWeight)
    keywords = ''
    for tag in tags:
        print ("tag: %s\t\t weight: %f" % (tag[0],tag[1]))
        # tag0 = tag[0].encode('UTF-8')
        tag1 = str(round(tag[1],6))
        keywords += tag[0] + '\t' + tag1 + '\n'
        
    filename_w = file_name + 'All_User_Keywords.txt'
    f = open(filename_w,'w',encoding = 'utf-8')
    f.write(keywords)
    f.close()

def main():
    cfg = getconfig()
    dbname = cfg['MongoDBConnection']['db']
    file_name = 'DATA\\' + dbname + '\\'
    get_all_weibo_keywords(file_name)

main()