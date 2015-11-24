#coding=utf-8
'''
Created on 2015年11月22日

@author: Administrator
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.neighbors import KernelDensity
from sklearn.grid_search import GridSearchCV

from Common.GetRetrievalResults import getTopNResults
from Analysis.RelevantTimeAnalysis import relTweetCountByDayBeforeQuery
from Common.GetQueryEpoch import getQueriesEpoch
from Common.GetDocEpoch import getTweetsEpoch
from Common.PickleData import getPickleData, writePickleData
from Common.ParseRelevantCountByDay import getMaxDay1
from Common.GetTmeSpan import getTimeSpan

#===============================================================================
# for each query, generate the timeSpan list of the PRF documents as the training data
# topNResults[qid][docId] = score
# output: trainData[qid] = timeSpan list:
#===============================================================================
def generateTrainData(topNResults, tweetsEpoch, queriesEpoch):
    trainData = {}
    for qid in topNResults.keys():
        queryEpoch = queriesEpoch[qid]
        trainData.setdefault(qid, list())
        docDict = topNResults[qid] 
        for docId in docDict.keys():
            tweetEpoch = tweetsEpoch[docId]
            if tweetEpoch <= queryEpoch:
                timeSpan = getTimeSpan(queryEpoch, tweetEpoch )
                trainData[qid].append(timeSpan)
                
    return trainData 
            
        

#===============================================================================
# Each query has its time based KDE.
# For the trainData for a specific query, obtain the best KDE estimator via cross validation
# input:
# trainData: the timeSpan array of the PRF documents for a certain query 
# output: 
# bandwidth : the best bandwidth, which is obtianed via cross validation
# kde: the KDE estimator
#===============================================================================
def gaussianKDE(trainData):
    # Gaussian KDE
    grid = GridSearchCV(KernelDensity(kernel='gaussian'),
                    {'bandwidth': np.linspace(0.01, 1.0, 30)},
                    cv = 5)   # 5 cross-validation
    trainData = np.array(trainData)
    grid.fit(trainData[:, None])
    print grid.best_params_
    kde = grid.best_estimator_
    # kde = KernelDensity(kernel='gaussian', bandwidth).fit(trainData)
    return (grid.best_params_['bandwidth'], kde)

def prediction(kde, testSamples):
    testSamples = np.array(testSamples)
    logDens = kde.score_samples(testSamples)
    probDens = np.exp(logDens)
    return probDens


# maxDay = getMaxDay1(countByDayBeforeQuery)
# testDays = [i for i in range(0, maxDay + 1)]

#===============================================================================
# For each query, obtain the corresponding best bandwidthDict and kdeDict based on the topN retrieval results
#===============================================================================
def prfTimeKDE(topNResults, queriesEpoch, tweetsEpoch):  
    trainData = generateTrainData(topNResults, tweetsEpoch, queriesEpoch)
    kdeDict = {}
    bandwidthDict = {}
    for qid in trainData.keys():
        timeSpanList = trainData[qid]
        (bandwidth, kde) = gaussianKDE(timeSpanList)
        bandwidthDict[qid] = bandwidth
        kdeDict[qid] = kde
        
    return (bandwidthDict, kdeDict)



#===============================================================================
# get the time based probability density of the retrieval results
# retrievalResults[qid] = results list
# return probDens[qid][docId] = probDen
#===============================================================================
def getResultsProbDens(retrievalResults, kdeDict):
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
                probDen = prediction(kde, timeSpan)
                probDens[qid][docId] = probDen[0]
            else:
                probDens[qid][docId] = 0
                
    return probDens
    
    
    

if __name__=='__main__' :
    year = '2011'
    topN = 50
   
    queryTimeFile = 'E:\\eclipse\\QueryExpansion\\data\\QueryTime\\' + year + '.MBid_query_time.txt'
    tweetsEpochFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\tweetsEpoch_'+ year + '.pkl'
    resultFile = 'E:\\eclipse\\QueryExpansion\\data\\BM25\\BM25_' + year + '.txt'
     
    topNResults = getTopNResults(resultFile, topN)
    queriesEpoch = getQueriesEpoch(queryTimeFile, year)
    tweetsEpoch = getPickleData(tweetsEpochFile)
    
    



