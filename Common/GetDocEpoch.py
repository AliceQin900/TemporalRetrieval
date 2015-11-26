#coding=utf-8
'''
Created on 2015年11月12日

@author: Administrator
'''
import MySQLdb 
import pickle
from Common.PickleData import writePickleData, getPickleData

def getTweetsEpoch(year):
    if year == '2013':
        dbName = 'microblog_track'
    else:
        dbName = 'microblog_track_' + year[2:4]
    db = MySQLdb.connect(host="192.168.10.63",user='root',db=dbName, charset='utf8')
    cur = db.cursor()  
    tweetNum = 0
    tweetsEpoch = {}

#     cur.execute("SELECT id, epoch FROM microblog_track.tweet")
    cur.execute("SELECT id, epoch FROM " + dbName + ".tweet")
    data = cur.fetchone()
    while data != None:
        tweetId = str(data[0])
        epoch = long(data[1])
        tweetsEpoch[tweetId] = epoch
        tweetNum += 1 
        if tweetNum % 10000 == 0:
            print tweetNum 
        data = cur.fetchone()
    print tweetNum  
          
    db.close()
    return tweetsEpoch




if __name__=='__main__':
    year = '2012'
    tweetsEpochFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\tweetsEpoch\tweetsEpoch_'+ year + '.pkl'
    
    tweetsEpoch = getTweetsEpoch(year)
    print len(tweetsEpoch.keys())
    writePickleData(tweetsEpoch, tweetsEpochFile)
    
    
  
    