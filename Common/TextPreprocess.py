#coding=utf-8
'''
Created on 2015年11月12日

@author: Administrator
'''

import re
import nltk
from nltk.stem import *

NON_ENGLISH = re.compile("[^a-zA-Z0-9]+") 


#===============================================================================
# textProcess: nonEnglish characters filtering; lowerCase; segmentation; stopWords removal; stemming
#===============================================================================
def textProcess(text,stopWords):
    stemmer = nltk.PorterStemmer()
    oneline = text.replace('\n', ' ')
    oneline = NON_ENGLISH.sub(' ', oneline)  
    toks   = oneline.strip().lower().split()
    wordList=list()
    for t in toks:  
        if stopWords.has_key(t):
            pass
        else:
            stemedWord=stemmer.stem(t)
            wordList.append(stemedWord)
    s=" ".join(wordList)
    return s

def stopWordsGet(stopFilePath):
    stopFile=open(stopFilePath)
    dictStop={}
    for line in stopFile.readlines():
        stopWord=line.strip()
        dictStop[stopWord]=1
    stopFile.close()
    return dictStop


if __name__=='__main__':
    stopFilePath = 'E:\\eclipse\\QueryExpansion\\data\\english.stop'
    text = 'How MOOCs will shape the future of higher education . | LinkedIn :'
    stopWords = stopWordsGet(stopFilePath)
    s=textProcess(text,stopWords)
    print s
    
    