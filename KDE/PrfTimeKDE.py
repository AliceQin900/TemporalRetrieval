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

from Common.GetRetrievalResults import getTopNResults,getResults
from Analysis.RelevantTimeAnalysis import relTweetCountByDayBeforeQuery
from Common.GetQueryEpoch import getQueriesEpoch
from Common.GetDocEpoch import getTweetsEpoch
from Common.PickleData import getPickleData, writePickleData
from Common.ParseRelevantCountByDay import getMaxDay1
from Common.GetTmeSpan import getTimeSpan

#===============================================================================
# for each query, generate the timeSpan list of the PRF documents as the training data
# topNResults[qid][docId] = score
# output: trainData[qid] = timeSpan list
#===============================================================================
def getResultsTimeSpan(topNResults, tweetsEpoch, queriesEpoch):
    resultsTimeSpan = {}
    for qid in topNResults.keys():
        queryEpoch = queriesEpoch[qid]
        resultsTimeSpan.setdefault(qid, list())
        docDict = topNResults[qid] 
        for docId in docDict.keys():
            tweetEpoch = tweetsEpoch[docId]
            if tweetEpoch <= queryEpoch:
                timeSpan = getTimeSpan(queryEpoch, tweetEpoch )
                resultsTimeSpan[qid].append(timeSpan)
                
    return resultsTimeSpan 
            
        

#===============================================================================
# Each query has its time based KDE.
# For the trainData of a specific query, obtain the best KDE estimator via cross validation
# input:
# trainData: the timeSpan array of the PRF documents for a certain query 
# output: 
# bandwidth : the best bandwidth, which is obtianed via cross validation
# kde: the KDE estimator
#===============================================================================
def gaussianKDE(trainData):
    # Gaussian KDE
    trainData = np.array(trainData)
    grid = GridSearchCV(KernelDensity(kernel='gaussian'),
                    {'bandwidth': np.linspace(0.01, 1.0, 30)},
                    cv = 5)   # 5 cross-validation
    grid.fit(trainData[:, None])
    parameters =  grid.best_params_
    kde = grid.best_estimator_
    # kde = KernelDensity(kernel='gaussian', bandwidth).fit(trainData)  no cross-validation
    return (parameters['bandwidth'], kde)

def prediction(kde, testSamples):
    testSamples = np.array(testSamples)
    logDens = kde.score_samples(testSamples[:, None])
    probDens = np.exp(logDens)
    return probDens


# maxDay = getMaxDay1(countByDayBeforeQuery)
# testDays = [i for i in range(0, maxDay + 1)]

#===============================================================================
# training: For each query, obtain the corresponding best bandwidthDict and kdeDict based on
# the topN retrieval results
#===============================================================================
def prfTimeKDE(topNResults, queriesEpoch, tweetsEpoch):  
    trainData = getResultsTimeSpan(topNResults, tweetsEpoch, queriesEpoch)
    kdeDict = {}
    bandwidthDict = {}
    for qid in trainData.keys():
        timeSpanList = trainData[qid]
        (bandwidth, kde) = gaussianKDE(timeSpanList)
        bandwidthDict[qid] = bandwidth
        kdeDict[qid] = kde
        print qid + ', best bandwidth: ' +  str(bandwidth)        
    return (bandwidthDict, kdeDict)


  


if __name__=='__main__' :
    year = '2012'
    topNList = [i for i in range(50, 501, 50)]
    
    for topN in topNList:
        queryTimeFile = 'E:\\eclipse\\QueryExpansion\\data\\QueryTime\\' + year + '.MBid_query_time.txt'
        tweetsEpochFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\tweetsEpoch\\tweetsEpoch_'+ year + '.pkl'
        resultFile = 'E:\\eclipse\\QueryExpansion\\data\\BM25\\BM25_' + year + '.txt'
        bandwidthPrfTimeFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\KDE\\' + year + '\\band_prf' + str(topN) +'_' + year + '.pkl' 
        kdePrfTimeFile ='E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\KDE\\' + year + '\\kde_prf' + str(topN) +'_' + year + '.pkl' 
        
        # train the kde estimator
        topNResults = getTopNResults(resultFile, topN)
        queriesEpoch = getQueriesEpoch(queryTimeFile, year)
        tweetsEpoch = getPickleData(tweetsEpochFile)
        (bandwidthDict, kdeDict) = prfTimeKDE(topNResults, queriesEpoch, tweetsEpoch)
        writePickleData(bandwidthDict, bandwidthPrfTimeFile)
        writePickleData(kdeDict, kdePrfTimeFile)
    
    



