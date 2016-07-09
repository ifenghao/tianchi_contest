__author__ = 'zfh'

import cPickle
import numpy as np
from sklearn import svm,covariance
import matplotlib.pyplot as plt
import pandas as pd
import random
import os
import utils

def movingAverage(array,span):
    array = np.array(array, dtype=float)
    result=[]
    for row in array:
        row=pd.Series(row)
        row=pd.ewma(row,span=span)
        row=np.array(row)
        rowmean=np.mean(row)
        rowvar=np.var(row)
        prob=1/(np.sqrt(2*np.pi*rowvar))*np.exp(-(row-rowmean)**2/(2*rowvar))
        outliers=np.where(prob<1e-18)
        smoothOutliers(row,outliers,3)
        result.append(row)
    return np.array(result)


def uniform(array):
    array = np.array(array, dtype=float)
    mean=np.mean(array,axis=1)
    std=np.std(array,axis=1)
    result=[]
    for row,rowmean,rowstd in zip(array,mean,std):
        result.append((row-rowmean)/rowstd)
    result=np.array(result)
    result[np.isnan(result)] = 0
    result[np.isinf(result)] = 0
    return result,mean[0],std[0]

def smoothOutliers(rowdata,outliers,winsize):
    halfsize=winsize//2
    length=len(rowdata)
    window=[]
    for i in outliers[0]:
        if i<halfsize:
            for j in range(-i,halfsize+1):
                window.append(rowdata[i+j])
        elif i>length-1-halfsize:
            for j in range(-halfsize,length-i):
                window.append(rowdata[i+j])
        else:
            for j in range(-halfsize,halfsize+1):
                window.append(rowdata[i+j])
        windowmean=np.mean(window)
        rowdata[i]=windowmean


artistsObjectDict=cPickle.load(open('/home/zfh/allresults/artistsObjectDict.pkl','r'))
# artist=artistsObjectDict['8fb3cef29f2c266af4c9ecef3b780e97']
# song=artist.getSongsOwned()['7ec488fc483386cdada5448864e82990']
artist=artistsObjectDict['1731019fbaa825714d5f8e61ad1bb7ff']
song=artist.getSongsOwned()['80c5be31daac4db1896013567167d92d']

# trace=song.getTrace()
# result=movingAverage(trace,3)
# result,mean,var= uniform(result)
# print result
# mean=np.mean(trace,axis=1)
# max=np.max(trace,axis=1)
# var=np.var(trace,axis=1)
# p=np.exp(-(trace[0]-mean[0])**2/(2*var[0]))
# print max[0],mean[0],p
# for row in trace:
#     x=pd.Series(row)
#     x1=pd.ewma(x,span=3)
#     x1=np.array(x1)
#     mean=np.mean(x1)
#     var=np.var(x1)
#     p=1/(np.sqrt(2*np.pi*var))*np.exp(-(x1-mean)**2/(2*var))
#     plt.plot(x1,'b-',x,'y-')
#     plt.show()
#     print(mean,var,p)
# plt.plot(result[0],'b-')
# plt.plot(result[1],'r-')
# plt.plot(result[2],'g-')
# plt.plot(result[3],'y-')
# plt.show()

# plt.figure(figsize=(10,10))
# for artistId,artist in artistsObjectDict.items():
#     savePath = os.path.join(utils.resultPath, artistId)
#     if not os.path.exists(savePath):
#         os.makedirs(savePath)
#     for song in utils.clusterSongs(artist):
#         song.plotTrace([0,0,0,0])
#         plt.savefig(os.path.join(savePath,''.join(list(song.getId())[:32])+'.png'))
#         plt.clf()

for artist in artistsObjectDict.values():
    for song in utils.clusterSongs(artist):
        try:
            print utils.findSuddenPoint(song.getTrace()),song.getId()
        except IndexError:
            print song.getId()
# print utils.findSuddenPoint(song.getTrace())