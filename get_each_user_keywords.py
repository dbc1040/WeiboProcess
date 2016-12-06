# -*- coding: utf-8 -*-
import jieba
import jieba.analyse
import glob
import re
from config import getconfig
import DirOperator
def get_keywords(file_dir):
    txt_filenames = glob.glob(file_dir+'微博内容\\*.txt')
    alltext = ''
    count  = 0
    for txt_filename in txt_filenames:
        userid = re.findall(r'\d{10}',txt_filename)
        if len(userid) == 0:
            continue
        userid = userid[0]
        f = open(txt_filename,'r',encoding = 'utf-8')
        content = f.read()
        f.close()
        '''过滤没用的关键词'''
        num = re.findall(r'\d+|\.+',content)
        for everynum in num:
            content = content.replace(everynum,'')
        topK = 20
        jieba.analyse.set_stop_words('stopwords')
        tags = jieba.analyse.extract_tags(content, topK=topK)
        keywords = '\t'.join(tags)
        text = userid+'\t'+keywords+'\n'
        alltext += text
        count += 1
        print (userid + '---->'+str(count))
    filename = file_dir+'Each_User_Keywords.txt'
    f = open(filename,'w',encoding = 'utf-8')
    f.write(alltext)
    f.close()

def main():
    cfg = getconfig()
    dbname = cfg['MongoDBConnection']['db']
    file_name = 'DATA\\' + dbname + '\\'
    get_keywords(file_name)

main()