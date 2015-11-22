#coding=utf-8
'''
Created on 2015年11月12日

@author: Administrator
'''
import pickle
from Common.PickleData import writePickleData

#===============================================================================
# build the inverted index for docs in the filePath
# filePath: each line corresponding to a tweet which has been processed in advance
#===============================================================================
def invertedIndexing(filePath):
    wordsIndex = {}
    handle = open(filePath)
    i = 0
    for line in handle:
        entry = line.strip().split('-->')
        docId = entry[0]
        text = entry[1]
        words = text.split()
        for word in words:
            wordsIndex.setdefault(word, {})
            wordsIndex[word].setdefault(docId, 0)
            wordsIndex[word][docId] += 1
        i += 1
        if i % 10000 == 0:
            print i
    
    print 'total documents indexed: ' + str(i)        
    wordsCount = len(wordsIndex.keys()) 
    print 'total words: ' + str(wordsCount)     
    return wordsIndex



if __name__=='__main__':
    year = '2011'
#     filePath = 'E:\\eclipse\\QueryExpansion\\dataset\\processed\\test.txt'
    filePath = 'E:\\eclipse\\QueryExpansion\\dataset\\processed\\' + 'tweet' + year + '_processed.txt'
    indexedFile = 'E:\\eclipse\\TemporalRetrieval\\data\\pickle_data\\index\\' + 'tweet_index_' + year + '.pkl'
    
    wordsIndex = invertedIndexing(filePath)
    writePickleData(wordsIndex, indexedFile)
    
    



            