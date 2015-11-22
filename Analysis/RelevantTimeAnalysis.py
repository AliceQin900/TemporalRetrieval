#coding=utf-8
'''
Created on 2015年11月11日

@author: Administrator
'''
from Common.ParseQrels import relevantGet
from Common.GetQueryEpoch import getQueriesEpoch
from Common.GetDocEpoch import getTweetsEpoch
from Common.ParseRelevantCountByDay import getMaxDay, getRelevantCountByDay
from Common.PickleData import getPickleData, writePickleData


#===============================================================================
# calculate the relevant tweet count by day before the query time
#===============================================================================
def relTweetCountByDayBeforeQuery(relevantTweets, queriesTime, tweetsTime):
    secondsInDay = 3600 * 24
    daysBeforeQuery = {}
    for qid in relevantTweets.keys():
        daysBeforeQuery.setdefault(qid,{})
        queryEpoch = queriesTime[qid]
        tweetsDict = relevantTweets[qid]
        for tweetId in tweetsDict.keys():
            if tweetsTime.has_key(tweetId):
                tweetEpoch = tweetsTime[tweetId]
                if tweetEpoch <= queryEpoch:
                    days = int (1.0 * (queryEpoch - tweetEpoch) / secondsInDay)
                    daysBeforeQuery[qid].setdefault(days, 0)
                    daysBeforeQuery[qid][days] += 1
                else:
                    print 'Error: tweetEpoch > queryEpoch'
            else:
                print 'relevant tweet of ' + tweetId + 'does not exist in the database'
                
    return daysBeforeQuery


#===============================================================================
# write the daysBeforeQuery dictionary to resFile
#===============================================================================
def writeRelCountByDayBeforeQuery(daysBeforeQuery, resFile):
    handle = open(resFile, 'w')
    for qid in daysBeforeQuery.keys():
        handle.write(qid + '\t')
        daysDict = daysBeforeQuery[qid]
        keyList = daysDict.keys()
        keyList.sort()
        for day in keyList:
            count = daysDict[day]
            handle.write(str(day) + ':' + str(count) + '\t')
        handle.write('\n')
    handle.close()
            

#===============================================================================
# write the daysBeforeQueryFile to matrixFile
#===============================================================================
def writeToMatrix(relevantCountByDayFile, matrixFile):
    maxDay = getMaxDay(relevantCountByDayFile)
    handle = open(matrixFile, 'w')
    handle.write('qid, relevantCountBydayBeforeQuery\n')
    handle.write('day' + '\t')
    for i in range(0, maxDay + 1):
        handle.write(str(i) + '\t')
    handle.write('\n')
    
    daysBeforeQuery = getRelevantCountByDay(relevantCountByDayFile)
    keyList = daysBeforeQuery.keys() 
    keyList.sort()
    for qid in keyList:
        handle.write(qid.strip('MB') + '\t')
        daysCountDict = daysBeforeQuery[qid]
        for i in range(0, maxDay + 1):
            if daysCountDict.has_key(i):
                handle.write(str(daysCountDict[i]) + '\t')
            else:
                handle.write('0' + '\t')
        handle.write('\n')
        
    handle.close()  
              


if __name__=='__main__':
    year = '2011'
    qrelFile = 'E:\\eclipse\\QueryExpansion\\data\\qrels\\' + 'qrels.microblog' + year + '_new.txt'
    queryTimeFile = 'E:\\eclipse\\QueryExpansion\\data\\QueryTime\\' + year + '.MBid_query_time.txt'
    relevantCountByDayFile = '../data/relevantCountByDay/relevantCountByDay_' + year + '.txt'
    tweetsEpochFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\tweetsEpoch_'+ year + '.pkl'
    matrixFile = '../data/relevantCountByDay/relevantCountByDayMatrix_' + year + '.txt'
    
#     relevantTweets = relevantGet(qrelFile)
#     queriesEpoch = getQueriesEpoch(queryTimeFile, year)
#     tweetsEpoch = getPickleData(tweetsEpochFile)
#     relevantCountByDay = relTweetCountByDayBeforeQuery(relevantTweets, queriesEpoch, tweetsEpoch)
#     writeRelCountByDayBeforeQuery(relevantCountByDay, relevantCountByDayFile)
    
    writeToMatrix(relevantCountByDayFile, matrixFile)
    
    
            