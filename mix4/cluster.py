__author__ = 'zfh'
# coding:utf-8
import os
import cPickle
import warnings
import time

import matplotlib.pyplot as plt
import numpy as np

import utils
import preprocess as pp
from sklearn import cluster


distance = 60
embedDim = 7
interval = 0
artistObjectFile = os.path.join(utils.allResultPath, 'artistsObjectDict.pkl')
artistsObjectDict = cPickle.load(open(artistObjectFile, 'r'))
plt.figure(figsize=(6, 4))
for artistId, artist in artistsObjectDict.items():
    array=[]
    for songId, song in artist.getSongsOwned().items():
        traceLength = np.array(song.getTrace()).shape[1]
        if traceLength < utils.days:  # 训练集长度不足10的歌曲
            print 'lack ' + str(traceLength)
            songTrace=song.getTrace()
            songTrace=np.hstack((np.zeros((4,utils.days-traceLength)),songTrace))
            song.setTrace(songTrace)
        array.append(song.getTrace()[0])
    array=np.array(array)
    # clf=cluster.KMeans(n_clusters=2, init='k-means++', n_init=10, max_iter=300, random_state=None, n_jobs=1)
    clf=cluster.AffinityPropagation(damping=0.5, max_iter=1000, convergence_iter=30, preference=None, affinity='euclidean', verbose=False)
    # clf=cluster.MeanShift(bandwidth=None, seeds=None, bin_seeding=False, min_bin_freq=1, cluster_all=True, n_jobs=1)
    # clf=cluster.SpectralClustering(n_clusters=8, eigen_solver=None, random_state=None, n_init=10, gamma=1.0, affinity='rbf',
    #                                n_neighbors=10, eigen_tol=0.0, assign_labels='kmeans', degree=3, coef0=1, kernel_params=None)
    # clf=cluster.DBSCAN(eps=0.5, min_samples=2, metric='euclidean', algorithm='auto', leaf_size=30, p=None, random_state=None)
    # clf=cluster.Birch(threshold=0.5, branching_factor=50, n_clusters=3, compute_labels=True, copy=True)
    nClusters=clf.fit_predict(array)
    savePath = os.path.join(utils.resultPath,'Birch', artistId)
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    num=0
    for row,index in zip(array,nClusters):
        plt.plot(row)
        plt.savefig(os.path.join(savePath, str(index) +' cluster '+str(num) + ".png"))
        num+=1
        plt.clf()