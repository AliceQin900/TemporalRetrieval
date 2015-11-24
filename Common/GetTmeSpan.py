#coding=utf-8
'''
Created on 2015年11月23日

@author: Administrator
'''


def getTimeSpan(queryEpoch, tweetEpoch ):
    secondsInDay = 3600 * 24
    if tweetEpoch <= queryEpoch:
        timeSpan = 1.0 * (queryEpoch - tweetEpoch) / secondsInDay
        return timeSpan
    else:
        print 'Error: tweetEpoch > queryEpoch'