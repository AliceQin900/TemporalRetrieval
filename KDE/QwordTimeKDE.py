#coding=utf-8
'''
Created on 2015年11月26日

@author: Administrator
'''
from Common.GetTmeSpan import getTimeSpan
from KDE.PrfTimeKDE import gaussianKDE
from Common.GetRetrievalResults import getTopNResults
from Common.GetQueryEpoch import getQueriesEpoch
from Common.GetDocEpoch import getTweetsEpoch
from Common.PickleData import getPickleData, writePickleData
from Common.GetQuery import getProcessedQueries
from Common.TextPreprocess import stopWordsGet

#===============================================================================
# obtain the timespan list of a qword in the topN retrieval resutls
#===============================================================================
def getQwordTimeSpan(qid, qword, topNResults, wordsIndex, tweetsEpoch, queriesEpoch):
    qwordTimeSpans = list()
    queryEpoch = queriesEpoch[qid]
    qidTopNDocs = topNResults[qid].keys()
    qwordAllDocs = wordsIndex[qword]
    for tweetId in qidTopNDocs:
        if qwordAllDocs.has_key(tweetId):
            tweetEpoch = tweetsEpoch[tweetId]
            if tweetEpoch <= queryEpoch:
                timeSpan = getTimeSpan(queryEpoch, tweetEpoch )
                key = qid + '_' + qword
                qwordTimeSpans.append(timeSpan)
    return qwordTimeSpans




#===============================================================================
# training: For each query word, obtain the corresponding best bandwidthDict and kdeDict based on
# the timespan list in the topN retrieval results
#===============================================================================
def qwordTimeKDE(topNResults, queriesEpoch, tweetsEpoch, queriesDict, wordsIndex):  
    kdeDict = {}
    bandwidthDict = {}
    count = 0
    for qid in queriesDict.keys():
        queryStr = queriesDict[qid]
        qwords = queryStr.split()
        for qword in qwords:
            qwordTimeSpans = getQwordTimeSpan(qid, qword, topNResults, wordsIndex, tweetsEpoch, queriesEpoch)
            if len(qwordTimeSpans) >= 5:   # the training sample number for gaussianKDE should be larger than 5 for cross-validation
                (bandwidth, kde) = gaussianKDE(qwordTimeSpans)
                key = qid + '_' + qword
                bandwidthDict[key] = bandwidth
                kdeDict[key] = kde
                print key + ', best bandwidth: ' +  str(bandwidth) 
            else:
                print key + ', the training sample number is less thant 5'
                count += 1
    print 'total ' + str(count) + ' query words has less than 5 training samples'
    return (bandwidthDict, kdeDict)
 
            
if __name__=='__main__':
    year = '2011'
    topN = 100
    
    stopFilePath = 'E:\\eclipse\\QueryExpansion\\data\\english.stop'
    indexedFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\index\\' + 'tweet_index_' + year + '.pkl'
    queryTimeFile = 'E:\\eclipse\\QueryExpansion\\data\\QueryTime\\' + year + '.MBid_query_time.txt'
    tweetsEpochFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\tweetsEpoch\\tweetsEpoch_'+ year + '.pkl'
    resultFile = 'E:\\eclipse\\QueryExpansion\\data\\BM25\\BM25_' + year + '.txt'
    bandwidthQwordTimeFile = '../data/pickle_data/KDE/' + year + '/qword_time/band_qword' + str(topN) + '_' + year + '.pkl'
    kdeQwordTimeFile = '../data/pickle_data/KDE/' + year + '/qword_time/kde_qword' + str(topN) + '_' + year + '.pkl'
    
    topNResults = getTopNResults(resultFile, topN)
    queriesEpoch = getQueriesEpoch(queryTimeFile, year)
    tweetsEpoch = getPickleData(tweetsEpochFile)
    stopWords = stopWordsGet(stopFilePath)
    queriesDict = getProcessedQueries(queryTimeFile, stopWords)
    wordsIndex = getPickleData(indexedFile)
    (bandwidthDict, kdeDict) = qwordTimeKDE(topNResults, queriesEpoch, tweetsEpoch, queriesDict, wordsIndex)
    writePickleData(bandwidthDict, bandwidthQwordTimeFile)
    writePickleData(kdeDict, kdeQwordTimeFile)
    
    

       
            
    
    
    
        







            