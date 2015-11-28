#coding=utf-8
'''
Created on 2015年11月28日

@author: Administrator
'''


import math

from Common.GetQuery import getProcessedQueries
from Common.TextPreprocess import stopWordsGet
from Common.PickleData import getPickleData, writePickleData
from Common.WriteUtils import getTopNResults, writeTopNResults
from KDE.PrfTimeKDE import prediction
from Common.GetTmeSpan import getTimeSpan
from Retrieval.BM25 import getDocsLength, getAvgDocsLenth, getDocsCount, dtfWeighting
from Common.GetQueryEpoch import getQueriesEpoch

#===============================================================================
# temporal based dtfWeighting
#===============================================================================
def dtfWeightingT(queriesEpoch, tweetsEpoch, kdeQwordDict, qid, qword, docId, wordsIndex, docsLength, avgDocsLength, k1, b):
    kde = kdeQwordDict[qid + '_' + qword]
    queryEpoch = queriesEpoch[qid]
    tweetEpoch = tweetsEpoch[docId]
    if queryEpoch >= tweetEpoch:
        timeSpan = getTimeSpan(queryEpoch, tweetEpoch )
        probDens = prediction(kde, [timeSpan])
        probDen = probDens[0]
        count = wordsIndex[qword][docId]
        docLength = docsLength[docId]
        numerator = (k1 + 1) * count * probDen
        denominator = k1 * (1 - b + b * docLength / avgDocsLength) + count * probDen
        dtf = 1.0 * numerator / denominator
    else:
        dtf = 0
        
    return dtf


def idfWeighting(qword ,docsCount, wordsIndex):
    docsDict = wordsIndex[qword]
    df = len(docsDict.keys())
    idf = math.log((docsCount + 1) / (df + 0.5))
    return idf   


def scoreBM25T(queriesEpoch, tweetsEpoch, kdeQwordDict, queriesDict, wordsIndex, docsLength, k1, b):
    scores = {}
    avgDocsLength =  getAvgDocsLenth(docsLength)
    docsCount = getDocsCount(docsLength)
    for qid in queriesDict.keys():
        print qid
        scores.setdefault(qid, {})
        queryStr = queriesDict[qid]
        qwords = queryStr.split()
        for qword in qwords:
            idf = idfWeighting(qword, docsCount, wordsIndex)
            if wordsIndex.has_key(qword):
                docsDict = wordsIndex[qword]
                if kdeQwordDict.has_key(qid + '_' + qword):
                    for docId in docsDict.keys(): 
                        dtf = dtfWeightingT(queriesEpoch, tweetsEpoch, kdeQwordDict, qid, qword, docId, wordsIndex, docsLength, avgDocsLength, k1, b)
                        s = dtf * idf
                        scores[qid].setdefault(docId, 0)
                        scores[qid][docId] += s
                else:
                    for docId in docsDict.keys():
                        dtf = dtfWeighting(qword, docId, wordsIndex, docsLength, avgDocsLength, k1, b)      
                        s = dtf * idf
                        scores[qid].setdefault(docId, 0)
                        scores[qid][docId] += s
    return scores
                
            

if __name__=='__main__':
    year = '2011'
    topN = 1000
    kdeN = 100
    tag = 'myBM25T'
    k1 = 0.3
    b = 0.05
    
    stopFilePath = 'E:\\eclipse\\QueryExpansion\\data\\english.stop'
    indexedFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\index\\' + 'tweet_index_' + year + '.pkl'
    queryTimeFile = 'E:\\eclipse\\QueryExpansion\\data\\QueryTime\\' + year + '.MBid_query_time.txt'
    tweetsEpochFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\tweetsEpoch\\tweetsEpoch_'+ year + '.pkl'
    docsFilePath = 'E:\\eclipse\\QueryExpansion\\dataset\\processed\\tweet' + year + '_processed.txt'
    resultFilePath = '../data/rank_BM25/' + year + '/' + tag +'_k'+ str(k1) + '_b' + str(b)  + '.txt'
    kdeQwordTimeFile = '../data/pickle_data/KDE/' + year + '/qword_time/kde_qword' + str(kdeN) + '_' + year + '.pkl'   
      
    stopWords = stopWordsGet(stopFilePath)
    queriesDict = getProcessedQueries(queryTimeFile, stopWords)
    wordsIndex = getPickleData(indexedFile)
    docsLength = getDocsLength(docsFilePath)
    queriesEpoch = getQueriesEpoch(queryTimeFile, year)
    tweetsEpoch = getPickleData(tweetsEpochFile)
    kdeQwordDict = getPickleData(kdeQwordTimeFile)
    scores = scoreBM25T(queriesEpoch, tweetsEpoch, kdeQwordDict, queriesDict, wordsIndex, docsLength, k1, b)
    topNResults = getTopNResults(scores, topN)
    writeTopNResults(topNResults, resultFilePath, tag)
    
    



    