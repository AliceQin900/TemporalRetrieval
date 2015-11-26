#coding=utf-8
'''
Created on 2015年11月24日

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
# draw histogram and line chart in the same figure
# x: for drawing histogram;
# x1, y1: for drawing line chart;
# maxDay: limit of x axis
#===============================================================================
def drawHistLine(x, x1, y1, maxDay, qid):
    bins = np.arange(0, maxDay + 1, 1)
    fig, ax = plt.subplots()
    ax.plot(x1, y1, 'bo-', linewidth=2, label='KDE')
    ax.hist(x, bins, fc='gray', align='left', histtype='stepfilled', normed=True, label='true distribution')
    
    ax.set_xlim(-1, maxDay + 1);  # 设置x轴坐标范围
    ax.set_xticks(bins)   # 设置x轴坐标刻度
    ax.set_yticks(np.arange(0, 1.1, 0.1)) # 设置y轴坐标刻度
    ax.legend(loc='best') 
    ax.set_ylabel('probability')  
    ax.set_xlabel('days before the query time')
    plt.title(qid)  # 设置图标题
    


if __name__=='__main__':
    year = '2012'
    topN = 100
    maxDay = 16   # 2011,2012: 16  ; 2013, 2014: 58
    daysList = [i for i in range(0, maxDay + 1)]
    
    queryTimeFile = 'E:\\eclipse\\QueryExpansion\\data\\QueryTime\\' + year + '.MBid_query_time.txt'
    tweetsEpochFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\tweetsEpoch\\tweetsEpoch_'+ year + '.pkl'
    qrelFile = 'E:\\eclipse\\QueryExpansion\\data\\qrels\\' + 'qrels.microblog' + year + '_new.txt'
    kdePrfTimeFile ='E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\KDE\\' + year + '\\kde_prf' + str(topN) +'_' + year + '.pkl' 
    
    kdeDict = getPickleData(kdePrfTimeFile)
    queriesEpoch = getQueriesEpoch(queryTimeFile, year)
    tweetsEpoch = getPickleData(tweetsEpochFile)
    relevantResults = relevantGet(qrelFile)
    relevantTimeSpan = getResultsTimeSpan(relevantResults, tweetsEpoch, queriesEpoch)
    
    x1 = np.array(daysList, dtype=np.float)
    for qid in kdeDict.keys():
        probDens = prediction(kdeDict[qid], x1)
        y1 = probDens
        drawHistLine(relevantTimeSpan[qid], x1, y1, maxDay, qid)
        figPath = 'E:\eclipse\TemporalRetrieval\data\img\\' + qid + '.png'
        plt.savefig(figPath)
        plt.close()
        print  'draw for ' + qid 
        
    
    
    
    
    
    
    