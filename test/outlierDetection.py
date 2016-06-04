__author__ = 'zfh'

import cPickle
import numpy as np
from sklearn import svm,covariance
import matplotlib.pyplot as plt
import pandas as pd
import random

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
# artist=artistsObjectDict['3e395c6b799d3d8cb7cd501b4503b536']
# song=artist.getSongsOwned()['d80b89ec5ed3821e3661dfc8804ff762']
# artist=artistsObjectDict['2e14d32266ee6b4678595f8f50c369ac']
# song=artist.getSongsOwned()['3dcfcb7f74fb08a3fcc7db6da5316bc0']
artist=artistsObjectDict['b7522cc91cf57ada15de2298bfd6a3ee']
song=artist.getSongsOwned()['720313f19ec784dd7bbae343190ae71a']

trace=song.getTrace()
result=movingAverage(trace,3)
result,mean,var= uniform(result)
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
plt.plot(result[0],'b-')
plt.plot(result[1],'r-')
plt.plot(result[2],'g-')
plt.plot(result[3],'y-')
plt.show()
