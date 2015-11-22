#coding=utf-8
'''
Created on 2015年5月6日

@author: Administrator
'''
#===============================================================================
# get the official relevant judgments
# return relevant[qid][docId] = rel
#===============================================================================
def relevantGet(qrelFile):
    relevant = {}
    count = 0
    
    qrFile = open(qrelFile)
    for line in qrFile:
        entry = line.strip().split()
        qid = entry[0]
        docId = entry[2]
        rel = int(entry[3])
        if rel != 0:
            relevant.setdefault(qid, {})
            relevant[qid][docId] = rel
            count += 1
    print 'total queries: ' + str(len(relevant.keys()))
    print 'num of relevant docs: ' + str(count)
    return relevant

def relevantWrite(relevant, relFile):
    rFile = open(relFile, 'w') 
    keyList = relevant.keys()
    keyList.sort()
    for qid in keyList:
        docDict = relevant[qid]
        for docId in docDict.keys():
            rFile.write(qid + '\t' + docId + '\t' + str(docDict[docId]) + '\n')
    rFile.close()
    
            
#====================================================================
# get the relCount for each query
# input : relevant[qid][docId] = rel
#====================================================================
def relCountPerQ(relevant):
    relCount = {}
    for qid in relevant.keys():
        relCount[qid] = len(relevant[qid].keys())
    return relCount
            
                

    
    
            
            