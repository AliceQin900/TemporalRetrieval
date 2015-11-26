#coding=utf-8
'''
Created on 2015年11月12日

@author: Administrator
'''
from pprint import pprint
from Common.GetDocEpoch import getTweetsEpoch
from Common.GetQueryEpoch import getQueriesEpoch
from Common.GetQuery import getProcessedQueries
from Common.TextPreprocess import stopWordsGet
from Common.PickleData import getPickleData, writePickleData


#===============================================================================
# calculate the df of the query word (qword) by day before the query time (before 0, 1, 2,..., days of the query)
#===============================================================================
def dfBydayBeforeQuery(qword, qid, wordsIndex, tweetsEpoch, queriesEpoch):
    secondsInDay = 3600 * 24
    dfByDays = {}
    
    queryEpoch = queriesEpoch[qid]
    if wordsIndex.has_key(qword):
        docsDict = wordsIndex[qword]
        for tweetId in docsDict.keys():    
            tweetEpoch = tweetsEpoch[tweetId]
            if tweetEpoch <= queryEpoch:
                days = int (1.0 * (queryEpoch - tweetEpoch) / secondsInDay)
                dfByDays.setdefault(days, 0)
                dfByDays[days] += 1
    else:
        print 'this query word does not exist in the corpus !'
    return dfByDays


#===============================================================================
# queriesDict: the processed queries
#===============================================================================
def queryWordsDfByDayBeforeQuery(queriesDict, wordsIndex, tweetsEpoch, queriesEpoch): 
    qwordsDfByDay = {} 
    for qid in queriesDict.keys():
        queryStr = queriesDict[qid]
        qwords = queryStr.split()
        for qword in qwords:
            dfByDays = dfBydayBeforeQuery(qword, qid, wordsIndex, tweetsEpoch, queriesEpoch)
            key = qid + '_' + qword
            qwordsDfByDay[key] = dfByDays
    return qwordsDfByDay 



def getMaxDay(qwordsDfByDayFile):
    dayDict = {}
    qwordsDfByDay = getPickleData(qwordsDfByDayFile)
    for key in qwordsDfByDay.keys():
        qwordDfByDay = qwordsDfByDay[key]
        for day in qwordDfByDay.keys():
            if not dayDict.has_key(day):
                dayDict[day] = 1
    dayList = dayDict.keys()
    maxDay = max(dayList)
    return maxDay
            
        
                           

def writeQwordsDfByDayToMatrix(qwordsDfByDayFile, queriesDict, maxDay, matrixFile):
    handle = open(matrixFile, 'w')
    handle.write('qid_qword, qwordDfByDayBeforeQuery \n')
    handle.write('day' + '\t')
    for i in range(0, maxDay + 1):
        handle.write(str(i) + '\t')
    handle.write('\n')
    
    qwordsDfByDay = getPickleData(qwordsDfByDayFile)
    keyList = queriesDict.keys()
    keyList.sort()
    for qid in keyList:
        queryStr = queriesDict[qid]
        qwords = queryStr.split()
        for qword in qwords:
            key = qid + '_' + qword
            if qwordsDfByDay.has_key(key):
                handle.write(key + '\t')
                dfByDays = qwordsDfByDay[key]
                for i in range(0, maxDay + 1):
                    if dfByDays.has_key(i):
                        handle.write(str(dfByDays[i]) + '\t')
                    else:
                        handle.write('0' + '\t')
                handle.write('\n')
        
    handle.close()
                
    

                  

if __name__=='__main__':
    year = '2011'
    queryTimeFile = 'E:\\eclipse\\QueryExpansion\\data\\QueryTime\\' + year + '.MBid_query_time.txt'
    stopFilePath = 'E:\\eclipse\\QueryExpansion\\data\\english.stop'
    indexedFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\index\\' + 'tweet_index_' + year + '.pkl'
    tweetsEpochFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\tweetsEpoch\\tweetsEpoch_'+ year + '.pkl'
    qwordsDfByDayFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\qwordsDfByDay\\qwordsDfByDay_' + year + '.pkl'
    matrixFile = 'E:\\eclipse\\TemporalRetrieval\\data\\qwordsDfByDay\\qwordsDfByDay_' + year + '.txt'
    
    stopWords = stopWordsGet(stopFilePath)
    queriesDict = getProcessedQueries(queryTimeFile, stopWords)
#     wordsIndex = getPickleData(indexedFile)
#     tweetsEpoch = getPickleData(tweetsEpochFile)
#     queriesEpoch = getQueriesEpoch(queryTimeFile, year)
#     qwordsDfByDay = queryWordsDfByDayBeforeQuery(queriesDict, wordsIndex, tweetsEpoch, queriesEpoch)
#     writePickleData(qwordsDfByDay, qwordsDfByDayFile)
    
    maxDay = getMaxDay(qwordsDfByDayFile)
    print 'maxDay: ' + str(maxDay) 
    writeQwordsDfByDayToMatrix(qwordsDfByDayFile, queriesDict, maxDay, matrixFile)
    
                      
                      
                    
            