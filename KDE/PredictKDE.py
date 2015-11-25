#coding=utf-8
'''
Created on 2015年11月24日

@author: Administrator
'''

from Common.GetTmeSpan import getTimeSpan
from PrfTimeKDE import prediction
from Common.PickleData import getPickleData, writePickleData
from Common.GetQueryEpoch import getQueriesEpoch
from Common.GetDocEpoch import getTweetsEpoch
from Common.GetRetrievalResults import getResults
from Common.WriteUtils import writeResults


#===============================================================================
# get the time based probability density of the retrieval results
# retrievalResults[qid] = results list
# return probDens[qid][docId] = probDen
#===============================================================================
def predictResultsProbDens(retrievalResults, queriesEpoch, tweetsEpoch, kdeDict):
    probDens = {}
    for qid in retrievalResults.keys():
        probDens.setdefault(qid, {})
        kde = kdeDict[qid]
        queryEpoch = queriesEpoch[qid]
        
        resultsList = retrievalResults[qid]
        for result in resultsList:
            docId = result.docId
            tweetEpoch = tweetsEpoch[docId]
            if queryEpoch >= tweetEpoch:
                timeSpan = getTimeSpan(queryEpoch, tweetEpoch )
                probDen = prediction(kde, [timeSpan])
                probDens[qid][docId] = probDen[0]
            else:
                probDens[qid][docId] = 0
        print qid        
    return probDens



if __name__=='__main__':
    year = '2011'
    topN = 100
    
    resultFile = 'E:\\eclipse\\QueryExpansion\\data\\BM25\\BM25_' + year + '.txt'
    queryTimeFile = 'E:\\eclipse\\QueryExpansion\\data\\QueryTime\\' + year + '.MBid_query_time.txt'
    tweetsEpochFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\tweetsEpoch_'+ year + '.pkl'
    kdePrfTimeFile ='E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\KDE\\kde_prf' + str(topN) +'_' + year + '.pkl'
    kdeBasedRankFile = '../data/rank_KDE/rank_KDE' + str(topN) + '_' +  year + '.txt'
    tag = 'PRF_Time_KDE'
    
    kdeDict = getPickleData(kdePrfTimeFile)
    retrievalResults = getResults(resultFile)
    queriesEpoch = getQueriesEpoch(queryTimeFile, year)
    tweetsEpoch = getPickleData(tweetsEpochFile)
    probDens = predictResultsProbDens(retrievalResults, queriesEpoch, tweetsEpoch, kdeDict)
    writeResults(probDens, kdeBasedRankFile, tag)
    
    
    
    