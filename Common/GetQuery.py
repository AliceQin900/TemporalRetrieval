#coding=utf-8
'''
Created on 2015年11月12日

@author: Administrator
'''
from Common.TextPreprocess import textProcess

#===============================================================================
# get the processed queries
#===============================================================================
def getProcessedQueries(queryTimeFile, stopWords):
    processedQueries = {}
    handle = open(queryTimeFile)
    for line in handle:
        entry = line.strip().split('\t')
        qid = entry[0]
        query = entry[1]
        proQuery = textProcess(query,stopWords)
        processedQueries[qid] = proQuery
        
    if len(processedQueries.keys()) < len(handle.readlines()):
        print 'some queries are missing !'
    return processedQueries



