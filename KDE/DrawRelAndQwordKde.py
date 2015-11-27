#coding=utf-8
'''
Created on 2015年11月26日

@author: Administrator
'''


import numpy as np
import matplotlib.pyplot as plt

from Common.ParseQrels import relevantGet
from KDE.PrfTimeKDE import getResultsTimeSpan
from Common.GetQueryEpoch import getQueriesEpoch
from Common.GetDocEpoch import getTweetsEpoch
from Common.PickleData import getPickleData, writePickleData
from Common.GetRetrievalResults import getTopNResults,getResults
from KDE.PrfTimeKDE import prfTimeKDE, prediction





#===============================================================================
# predict the relevant probability for the days based on different kdes
# kdeDict: provide various kdes 
# kdeDict[key] = kde
#===============================================================================
def predictDaysProbDens(kdeDict, maxDay):
    daysProbDens = {}
    daysList = [i for i in range(0, maxDay + 1)]
    for key in kdeDict.keys():
        probDens = prediction(kdeDict[key], daysList)
        daysProbDens[key] = probDens
    return daysProbDens




#prfProbDens = predictDaysProbDens(prfKdeDict, maxDay)
# qwordsProbDens = predictDaysProbDens(qwordsKdeDict, maxDay)
#===============================================================================
# draw histogram and line chart in the same figure
# relevantTimeSpans: for drawing histogram;
# prfProbDens, qwordsProbDens: for drawing line chart;
# maxDay: limit of x axis
#===============================================================================
def drawHistLine(relevantTimeSpans, prfProbDens, qwordsProbDens, maxDay, qid):
    daysList = [i for i in range(0, maxDay + 1)]
    daysList = np.array(daysList, dtype = np.float)
      
    fig, ax = plt.subplots()
    # ture distribution based on relevance judgements
    ax.hist(relevantTimeSpans[qid], daysList, fc='gray', align='left', histtype='stepfilled', normed=True, label='true distribution')
    # kde  based on prf docs epochs
    ax.plot(daysList, prfProbDens[qid], 'bo-', linewidth=2, label='prf_KDE') 
   # kde based on qwords epochs
    for qid_qword in qwordsProbDens.keys():
        entry = qid_qword.split('_')
        qid1 = entry[0]
        qword = entry[1]
        if qid == qid1:
            ax.plot(daysList, qwordsProbDens[qid_qword], linewidth=2, label= qword + '_KDE') 
   
    ax.set_xlim(-1, maxDay + 1);  # 设置x轴坐标范围
    ax.set_xticks(daysList)   # 设置x轴坐标刻度
    ax.set_yticks(np.arange(0, 1.1, 0.1)) # 设置y轴坐标刻度
    ax.legend(loc='best') 
    ax.set_ylabel('probability')  
    ax.set_xlabel('days before the query time')
    plt.title(qid)  # 设置图标题
    


if __name__=='__main__':
    year = '2011'
    topN = 100
    maxDay = 16   # 2011,2012: 16  ; 2013, 2014: 58
    
    queryTimeFile = 'E:\\eclipse\\QueryExpansion\\data\\QueryTime\\' + year + '.MBid_query_time.txt'
    tweetsEpochFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\tweetsEpoch\\tweetsEpoch_'+ year + '.pkl'
    qrelFile = 'E:\\eclipse\\QueryExpansion\\data\\qrels\\' + 'qrels.microblog' + year + '_new.txt'
    kdePrfTimeFile ='E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\KDE\\' + year + '\\prf_time\\kde_prf' + str(topN) +'_' + year + '.pkl' 
    kdeQwordTimeFile = '../data/pickle_data/KDE/' + year + '/qword_time/kde_qword' + str(topN) + '_' + year + '.pkl'
    
    queriesEpoch = getQueriesEpoch(queryTimeFile, year)
    tweetsEpoch = getPickleData(tweetsEpochFile)
    relevantResults = relevantGet(qrelFile)
    relevantTimeSpans = getResultsTimeSpan(relevantResults, tweetsEpoch, queriesEpoch)
    kdePrfDict = getPickleData(kdePrfTimeFile)
    prfProbDens = predictDaysProbDens(kdePrfDict, maxDay)
    kdeQwordDict = getPickleData(kdeQwordTimeFile)
    qwordsProbDens = predictDaysProbDens(kdeQwordDict, maxDay)
    keyList = kdePrfDict.keys()
#     keyList = ['MB1']
    for qid in keyList:
        drawHistLine(relevantTimeSpans, prfProbDens, qwordsProbDens, maxDay, qid)
        figPath = 'E:\eclipse\TemporalRetrieval\data\img\\rel_prf_qword\\' + qid + '.png'
        plt.savefig(figPath)
        plt.close()
        print  'draw for ' + qid 
        
        
        
        