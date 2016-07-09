__author__ = 'zfh'
import os
import utils
import matplotlib.pyplot as plt

artistList=set()
dir=os.path.join(utils.allResultPath,'bestanalysis')
files = os.listdir(dir)
for file in files:
    with open(os.path.join(dir,file),'r') as csvfile:
        while True:
            line=csvfile.readline().strip('\n')
            if not line:
                break
            line=line.split(',')
            artistId=line[0]
            artistList.add(artistId)
    break

fileDict={}
dir=os.path.join(utils.allResultPath,'bestanalysis')
files = os.listdir(dir)
for file in files:
    fileDict[str(file)]={}
    with open(os.path.join(dir,file),'r') as csvfile:
        while True:
            line=csvfile.readline().strip('\n')
            if not line:
                break
            line=line.split(',')
            artistId=line[0]
            play=int(line[1])
            if artistId not in fileDict[str(file)].keys():
                fileDict[str(file)][artistId]=[]
            fileDict[str(file)][artistId].append(play)

resultPath=os.path.join(dir,'result')
if not os.path.exists(resultPath):
    os.makedirs(resultPath)
plt.figure(figsize=(10,10))
for artistId in artistList:
    for file,artistDict in fileDict.items():
        plt.plot(artistDict[artistId],label=file)
    plt.legend()
    plt.savefig(os.path.join(resultPath,artistId))
    plt.clf()