#coding=utf-8
'''
Created on 2015年11月12日

@author: Administrator
'''

def getRelevantCountByDay(relevantCountByDayFile):
    relevantCountByDay = {}
    handle = open(relevantCountByDayFile)
    for line in handle:
        entry = line.strip().split('\t')
        qid = entry[0]
        relevantCountByDay.setdefault(qid, {})
        for i in range(1, len(entry)):
            daysCount = entry[i].split(':')
            day = int(daysCount[0])
            count = int(daysCount[1])
            relevantCountByDay[qid][day] = count
            
    handle.close()
    return relevantCountByDay
    


def getMaxDay(relevantCountByDayFile):
    daysDict = {}
    handle = open(relevantCountByDayFile)
    for line in handle:
        entry = line.strip().split('\t')
        for i in range(1, len(entry)):
            daysCountStr = entry[i]
            day = int(daysCountStr.split(':')[0])
            if not daysDict.has_key(day):
                daysDict[day] = 1
    daysList = daysDict.keys()
    maxDay = max(daysList)
    handle.close()
    return maxDay



def getMaxDay1(relevantCountByDay):
    dayDict = {}
    for qid in relevantCountByDay.keys():
        countDict = relevantCountByDay[qid]
        for day in countDict.keys():
            if not dayDict.has_key(day):
                dayDict[day] = 1
    dayList = dayDict.keys()
    maxDay = max(dayList)
    return maxDay

if __name__=='__main__':
    year = '2014'
    relevantCountByDayFile = '../data/relevantCountByDay/relevantCountByDay_' + year + '.txt'
    maxDay = getMaxDay(relevantCountByDayFile)
    print maxDay
    
    
    
    
                
                