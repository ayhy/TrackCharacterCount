# -*- coding: utf-8 -*-
#Logger

import sys
import re
from datetime import datetime
from functools import reduce
import math

def getCurrentCharacterCount(targetFileName):
    totalchar=0
    totalmainchar=0
    with open(targetFileName, 'r', encoding='utf-8') as readfile:
        text=readfile.read().strip("/n")
        main_char = re.sub("(<!--.*?-->)", "", text, flags=re.DOTALL) #remove  <!--comment-->
        main_char = re.sub("(/\*.*?\*/)", "", main_char, flags=re.DOTALL) #remove  /* comment */
        totalchar= len(text.strip("#"))
        totalmainchar=len((main_char.strip("#"))) # stripped markdown syntax
    return {"total":totalchar,"main":totalmainchar}

    return 
def updatelog(fullfilename):
    targetFiles=[]
    targetChars=[]
    targetDates=[]
    track_separate=False
    lastLine=[]

    now = datetime.now()
    today = now

    with open(fullfilename, 'r', encoding='utf-8') as infile:
        is_in_ini=False
        for line in infile:
            if line.startswith("----startini"):
                is_in_ini=True
            if line.startswith("----endini"):
                is_in_ini=False
                break
            if is_in_ini:
                if line.startswith("track_separate"):
                    tracks_separate = (line == "True")
                if line.startswith("fullfilepath"):
                    targetFiles.append(line.split("\t")[1].strip("\n").replace("\\", "/") )
                if line.startswith("deadline"):
                    deadline=line.split("\t")[1].strip("\n")
                    deadline=datetime.strptime(deadline,'%Y/%m/%d')
                    targetDates.append(deadline)
                if line.startswith("totalchar"):
                    char=line.split("\t")[1].strip("\n")
                    targetChars.append(int(char))
        print("retrieve last line")
        lastLine = (list(infile)[-1])
        print(lastLine)

    todaysprogress = now.strftime('%Y/%m/%d')

    targetNum=len(targetFiles)
    countlist=[]
    previousTotalChars=[0]*targetNum
    previousMainChars=[0]*targetNum
    remaining = [date - today for date in targetDates]

    scanrows=targetNum
    if track_separate==False:
        scanrows=1
    print(str(targetNum))
    if not lastLine.startswith("//"):
        print("get comparison data")
    #format:0日付 1全文 2本文 3本文+ 4補稿+ 5速度 6-- 7全文 8本文 9本文+ 10補稿+ 11速度 12-- .....
        lastLine=lastLine.split("\t")
        print(lastLine)
        for i in range(scanrows):
            previousTotalChars[i]=int(lastLine[i*6+1])
            previousMainChars[i]=int(lastLine[i*6+2])
    for i, targetFile in enumerate(targetFiles):
        with open(targetFile, 'r', encoding='utf-8') as readfile:
            counts = getCurrentCharacterCount(targetFile)
        counts["deltaMain"]=counts["main"] - previousMainChars[i]
        counts["deltaComment"]=counts["total"] - previousTotalChars[i] - counts["main"]
        counts["deltaDate"]=targetDates[i] - today
        counts["charRate"]=math.ceil( (targetChars[i]- counts["main"])/remaining[i].days) 
        countlist.append(counts)

    if track_separate:
        for i, targetFile in enumerate(targetFiles):
            progressparFile = "\t" + str(countlist[i]["total"]) + "\t" + str(countlist[i]["main"]) + "\t" \
                                   + str(countlist[i]["deltaMain"]) + "\t" + str(countlist[i]["deltaComment"]) + "\t" \
                                   + str(advisedrates[i]) + "\t"
            todaysprogress +=progressparFile
        todaysprogress +="\n"
    else:
        print(countlist)
        counted = reduce(lambda x, y: dict((k, v + y[k]) for k, v in x.items()), countlist)
        advisedrate =math.ceil( (sum(targetChars) - counted["main"]) / min(remaining).days)
        progressMerged = "\t" + str(counted["total"]) + "\t" + str(counted["main"]) + "\t" \
                              + str(counted["deltaMain"]) + "\t" + str(counted["deltaComment"]) + "\t" \
                              + str(advisedrate) + "\t"
        todaysprogress += progressMerged + "\n"

    with open(fullfilename, 'a', encoding='utf-8') as outfile:
        outfile.write(todaysprogress)
        print(todaysprogress)
    return 

if __name__=='__main__':
    updatelog(sys.argv[1])