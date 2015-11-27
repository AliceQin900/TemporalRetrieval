#coding=utf-8
'''
Created on 2015年11月27日

@author: Administrator
'''

k1 = 0.75
b = 0.05

import math

from Common.GetQuery import getProcessedQueries
from Common.TextPreprocess import stopWordsGet
from Common.PickleData import getPickleData, writePickleData
from Common.WriteUtils import getTopNResults, writeTopNResults



def getDocsLength(filePath):
    docsLength = {}
    handle = open(filePath)
    for line in handle:
        entry = line.strip().split('-->')
        docId = entry[0]
        content = entry[1]
        docLength = len(content.split())
        docsLength[docId] = docLength
    return docsLength


def getDocsCount(docsLength):
    count = len(docsLength.keys())
    print 'total documents count : ' + str(count)
    return count
        


def getAvgDocsLenth(docsLength):
    totalLength = 0
    count = 0
    for docId in docsLength.keys():
        totalLength += docsLength[docId]
        count += 1    
    avgDocsLength = 1.0 * totalLength / count
    return avgDocsLength    



def dtfWeighting(qword, docId, wordsIndex, docsLength, avgDocsLength, k1, b):
    count = wordsIndex[qword][docId]
    docLength = docsLength[docId]
    numerator = (k1 + 1) * count
    denominator = k1 * (1 - b + b * docLength / avgDocsLength) + count
    dtf = 1.0 * numerator / denominator
    return dtf


def idfWeighting(qword ,docsCount, wordsIndex):
    docsDict = wordsIndex[qword]
    df = len(docsDict.keys())
    idf = math.log((docsCount + 1) / (df + 0.5))
    return idf   


def scoreBM25(queriesDict, wordsIndex, docsLength, k1, b):
    scores = {}
    avgDocsLength =  getAvgDocsLenth(docsLength)
    docsCount = getDocsCount(docsLength)
    for qid in queriesDict.keys():
        print qid
        scores.setdefault(qid, {})
        queryStr = queriesDict[qid]
        qwords = queryStr.split()
        for qword in qwords:
            docsDict = wordsIndex[qword]
            for docId in docsDict.keys():
                dtf = dtfWeighting(qword, docId, wordsIndex, docsLength, avgDocsLength, k1, b)
                idf = idfWeighting(qword, docsCount, wordsIndex)
                s = dtf * idf
                scores[qid].setdefault(docId, 0)
                scores[qid][docId] += s
    return scores
                
            

if __name__=='__main__':
    year = '2011'
    topN = 1000
    tag = 'myBM25'
    k1 = 0.3
    b = 0.05
    
    stopFilePath = 'E:\\eclipse\\QueryExpansion\\data\\english.stop'
    indexedFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\index\\' + 'tweet_index_' + year + '.pkl'
    queryTimeFile = 'E:\\eclipse\\QueryExpansion\\data\\QueryTime\\' + year + '.MBid_query_time.txt'
    docsFilePath = 'E:\\eclipse\\QueryExpansion\\dataset\\processed\\tweet' + year + '_processed.txt'
    resultFilePath = '../data/rank_BM25/2011/myBM25.txt'   
      
    stopWords = stopWordsGet(stopFilePath)
    queriesDict = getProcessedQueries(queryTimeFile, stopWords)
    wordsIndex = getPickleData(indexedFile)
    docsLength = getDocsLength(docsFilePath)
    scores = scoreBM25(queriesDict, wordsIndex, docsLength, k1, b)
    topNResults = getTopNResults(scores, topN)
    writeTopNResults(topNResults, resultFilePath, tag)
    
    