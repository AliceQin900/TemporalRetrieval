#coding=utf-8
'''
Created on 2015年8月28日

@author: Administrator
'''
class TrecResult:
    def __init__(self, queryId, docId, rank, score):
        self.queryId = queryId
        self.docId = docId
        self.rank = rank
        self.score = score


def parseResultLine(resultLine):
    entry = resultLine.strip().split()
    queryId = entry[0]
    docId = entry[2]
    rank = int(entry[3])
    score = float(entry[4])
    return TrecResult(queryId, docId, rank, score)
    
    
    
    
def getTopNDocIds(resultFile, topN):
    topNDocIds = {}
    handle = open(resultFile)
    for line in handle:
        result = parseResultLine(line)
        docId = result.docId
        rank = result.rank
        if rank <= topN:
            topNDocIds[docId] = 1
    return topNDocIds


def getTopNResults(resultFile, topN):
    topNResults = {}
    handle = open(resultFile)
    for line in handle:
        result = parseResultLine(line)
        qid = result.queryId
        docId = result.docId
        rank = result.rank
        score = result.score
        if rank <= topN:
            topNResults.setdefault(qid, {})
            topNResults[qid][docId] = score
    return topNResults


def getResults(resultFile):
    results = {}
    handle = open(resultFile)
    for line in handle:
        result = parseResultLine(line)
        qid = result.queryId
        results.setdefault(qid, list())
        results[qid].append(result)
    return results





        