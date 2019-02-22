# -*- coding: utf-8 -*-
#Logger

import sys
import re
from datetime import datetime
from collections import Counter
import math

def updatelog(fullfilename):
    targetFiles=[]
    targetChars=[]
    targetDates=[]
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
                if line.startswith("fullfilepath"):
                    targetFiles.append(line.split("\t")[1].strip("\n").replace("\\", "/") )
                if line.startswith("deadline"):
                    date=line.split("\t")[1].strip("\n")
                    date=datetime.strptime(date,'%Y/%m/%d')
                    targetDates.append(date)
                if line.startswith("totalchar"):
                    char=line.split("\t")[1].strip("\n")
                    targetChars.append(int(char))
        print("retrieve last line")
        lastLine = (list(infile)[-1])
        print(lastLine)


    targetNum=len(targetFiles)
    previousTotalChars=[0]*targetNum
    previousMainChars=[0]*targetNum
    print(str(targetNum))
    if not lastLine.startswith("//"):
        print("get comparison data")
    #format:0日付 1全文 2本文 3本文+ 4補稿+ 5速度 n6empty 7全文 8本文 9本文+ 10補稿+ 11速度 12empty .....
        lastLine=lastLine.split("\t")
        print(lastLine)
        for i in range(targetNum):
            previousTotalChars[i]=int(lastLine[i*6+1])
            previousMainChars[i]=int(lastLine[i*6+2])
    todaysprogress = now.strftime('%Y/%m/%d')
    for i, targetFile in enumerate(targetFiles):
        with open(targetFile, 'r', encoding='utf-8') as readfile:
            text=readfile.read().strip("/n")
            main_char = re.sub("(<!--.*?-->)", "", text, flags=re.DOTALL) #remove  <!--comment-->
            main_char = re.sub("(/\*.*?\*/)", "", main_char, flags=re.DOTALL) #remove  /* comment */
            totalchar= len(text.strip("#"))
            totalmainchar=len((main_char.strip("#"))) # stripped markdown syntax

        addedmainchar = totalmainchar - previousMainChars[i]
        addedcommentchar = totalchar - previousTotalChars[i] - addedmainchar
        remaining = targetDates[i] - today
        advisedrate = math.ceil( (targetChars[i]- totalmainchar)/remaining.days) 
        progressparFile = "\t" + str(totalchar) + "\t" + str(totalmainchar) + "\t" \
                                    + str(addedmainchar) + "\t" + str(addedcommentchar) + "\t" \
                                    + str(advisedrate) + "\t"
        todaysprogress +=progressparFile
    todaysprogress +="\n"
    with open(fullfilename, 'a', encoding='utf-8') as outfile:
        outfile.write(todaysprogress)
        print(todaysprogress)
    return 

if __name__=='__main__':
    updatelog(sys.argv[1])