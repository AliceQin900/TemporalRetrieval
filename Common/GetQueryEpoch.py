#coding=utf-8
'''
Created on 2015年11月11日

@author: Administrator
'''

import time, datetime
from dateutil import parser
import warnings
warnings.filterwarnings("ignore", category=UnicodeWarning)


#===============================================================================
# parse queryTime to epoch (query 2011-2013)
# input: dateStr: utc date format 
# output: timeStamp: the epoch ( the seconds from 1970-01-01 00:00:00 utc)
#===============================================================================
def utcDateToEpoch(utcDate):
    timeArray = time.strptime(utcDate,'%a %b %d %H:%M:%S +0000 %Y')
    timeStamp = long(time.mktime(timeArray)) - time.timezone  # time.timezone: the local time zone, timeStamp,i.e., epoch
    return timeStamp

#===============================================================================
# # parse queryTime to epoch (query 2014)
#===============================================================================
def nonUtcDateToEpoch(dateStr):
    d = parser.parse(dateStr)  # d: datetime object (does not parse the timezone)
    entry = dateStr.split()
    timeZone = entry[len(entry) - 2]
    if timeZone == 'EST':
        utcDate = d + datetime.timedelta(hours = 5)
    elif timeZone == 'EDT':
        utcDate = d + datetime.timedelta(hours = 4)
        
    timeArray = utcDate.timetuple()
    timeStamp = long(time.mktime(timeArray)) - time.timezone  # timeStamp,i.e., epoch
    return timeStamp


def getQueriesEpoch(queryTimeFile, year):
    queriesEpoch = {}
    handle = open(queryTimeFile)
    for line in handle:
        entry = line.strip().split('\t')
        qid = entry[0]
        qtime = entry[2]
        if year != '2014':
            qEpoch = utcDateToEpoch(qtime)
            queriesEpoch[qid] = qEpoch
        else:
            qEpoch = nonUtcDateToEpoch(qtime)
            queriesEpoch[qid] = qEpoch
            
    return queriesEpoch  




if __name__=='__main__':
    dateStr = 'Mon Jan 31 21:02:33 +0000 2011'
    timeStamp = utcDateToEpoch(dateStr)
    print timeStamp
    
#     dateStr = 'Sat Mar 02 10:43:45 EST 2013'
#     timeStamp = nonUtcDateToEpoch(dateStr)
#     print timeStamp
#     
#     year = '2014'
#     queryTimeFile = 'E:\\eclipse\\QueryExpansion\\data\\QueryTime\\' + year + '.MBid_query_time.txt'
#     queriesTime = getQueriesEpoch(queryTimeFile, year)
#     print queriesTime['MB171']
    
    
    
    