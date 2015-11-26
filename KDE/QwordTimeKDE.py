#coding=utf-8
'''
Created on 2015年11月26日

@author: Administrator
'''
from Common.GetTmeSpan import getTimeSpan
from KDE.PrfTimeKDE import gaussianKDE

#===============================================================================
# obtain the timespan list of a qword in the topN retrieval resutls
#===============================================================================
def getQwordTimeSpan(qid, qword, topNResults, wordsIndex, tweetsEpoch, queriesEpoch):
    qwordTimeSpans = list()
    queryEpoch = queriesEpoch[qid]
    qidTopNDocs = topNResults[qid].keys()
    qwordAllDocs = wordsIndex[qword].keys()
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
    for qid in queriesDict.keys():
        queryStr = queriesDict[qid]
        qwords = queryStr.split()
        for qword in qwords:
            qwordTimeSpans = getQwordTimeSpan(qid, qword, topNResults, wordsIndex, tweetsEpoch, queriesEpoch)
            (bandwidth, kde) = gaussianKDE(qwordTimeSpans)
            key = qid + '_' + qword
            bandwidthDict[key] = bandwidth
            kdeDict[key] = kde
            print key + ', best bandwidth: ' +  str(bandwidth) 
    return (bandwidthDict, kdeDict)
            
            
            
    
    
    
        







            