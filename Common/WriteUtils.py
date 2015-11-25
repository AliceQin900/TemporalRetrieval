#coding=utf-8
'''
Created on 2015年11月24日

@author: Administrator
'''

#===============================================================================
# resultsDict[qid][docId] = score
#===============================================================================
def writeResults(resultsDict, filePath, tag):
    handle = open(filePath, 'w')
    keyList = resultsDict.keys()
    keyList.sort()
    for qid in keyList:
        docsDict =  resultsDict[qid]
        sortedList = sorted(docsDict.iteritems(), key= lambda d : d[1], reverse = True)
        rank = 0
        for l in sortedList:
            docId = l[0]
            score = l[1]
            rank += 1
            handle.write(qid + ' ' + 'Q0' + ' ' + docId + ' ' + str(rank) + ' ' + str(score) + ' ' + tag + '\n')
    handle.close()
    
    
    
    