import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import site
import pandas as pd
site.addsitedir('../lib')  # Always appends to end
from graph_summary_generator import mergeTime  as mt
from graph_summary_generator import overlaps  as ove
from graph_summary_generator import summary as gsg
from scipy import stats
import numpy
import scipy.stats

def timesBTC_2019():
    print("BTC 2019 Merge Times:")
    timesMaxAC = mt.mergeTime() 
    timesMaxAC.load("Times/TimesOfBTC2019MaxS_AC")
    
    timesMaxCC = mt.mergeTime() 
    timesMaxCC.load("Times/TimesOfBTC2019MaxS_CC")
    
    timesMaxACC = mt.mergeTime() 
    timesMaxACC.load("Times/TimesOfBTC2019MaxS_ACC")
    
    timesMinAC = mt.mergeTime()
    timesMinAC.load("Times/TimesOfBTC2019MinS_AC")
    
    timesMinCC = mt.mergeTime()
    timesMinCC.load("Times/TimesOfBTC2019MinS_CC")
    
    timesMinACC = mt.mergeTime()
    timesMinACC.load("Times/TimesOfBTC2019MinS_ACC")
    
    timesPAC = mt.mergeTime()
    timesPAC.load("Times/TimesOfBTC2019ParallelS_AC")
    
    timesPCC = mt.mergeTime()
    timesPCC.load("Times/TimesOfBTC2019ParallelS_CC")
    
    timesPACC = mt.mergeTime()
    timesPACC.load("Times/TimesOfBTC2019ParallelS_ACC")
    
    timesRAC = mt.mergeTime()
    timesRAC.load("Times/TimesOfBTC2019RandomS_AC")
    
    timesRCC = mt.mergeTime()
    timesRCC.load("Times/TimesOfBTC2019RandomS_CC")
    
    timesRACC = mt.mergeTime()
    timesRACC.load("Times/TimesOfBTC2019RandomS_ACC")
    
    rAC = []
    rCC = []
    rACC = []

    for i in range(10):
        rAC.append(timesRAC.timeAC[i])
        rCC.append(timesRCC.timeCC[i])
        rACC.append(timesRACC.timeACC[i])
    
        
    minAC = []
    minCC = []
    minACC = []
    
    paAC = []
    paCC = []
    paACC = []
    
    maxAC = []
    maxCC = []
    maxACC = []
    
    for i in range(1,6):
            
        minAC.append(timesMinAC.timeAC[i])
        minCC.append(timesMinCC.timeCC[i])
        minACC.append(timesMinACC.timeACC[i])
      
        paAC.append(timesPAC.timeAC[i])
        paCC.append(timesPCC.timeCC[i])
        paACC.append(timesPACC.timeACC[i])

        maxAC.append(timesMaxAC.timeAC[i])
        maxCC.append(timesMaxCC.timeCC[i])
        maxACC.append(timesMaxACC.timeACC[i])

    
    print("AC:")
    print("Max: ",numpy.mean(maxAC)/60," +- ",numpy.std(maxAC)/60 )
    print(maxAC)
    print("Min: ",numpy.mean(minAC)/60," +- ",numpy.std(minAC)/60 )
    print(minAC)
    print("Parallel: ",numpy.mean(paAC)/60," +- ",numpy.std(paAC)/60 )
    print(paAC)
    print("Random: ",numpy.mean(rAC)/60," +- ",numpy.std(rAC)/60 )
    print(rAC)
    
    print("\nCC:")
    print("Max: ",numpy.mean(maxCC)/60," +- ",numpy.std(maxCC)/60 )
    print(maxCC)
    print("Min: ",numpy.mean(minCC)/60," +- ",numpy.std(minCC)/60 )
    print(minCC)
    print("Parallel: ",numpy.mean(paCC)/60," +- ",numpy.std(paCC)/60 )
    print(paCC)
    print("Random: ",numpy.mean(rCC)/60," +- ",numpy.std(rCC)/60 )
    print(rCC)
    
    print("\nACC:")
    print("Max: ",numpy.mean(maxACC)/60," +- ",numpy.std(maxACC)/60 )
    print(maxACC)
    print("Min: ",numpy.mean(minACC)/60," +- ",numpy.std(minACC) /60)
    print(minACC)
    print("Parallel: ",numpy.mean(paACC)/60," +- ",numpy.std(paACC) /60)
    print(paACC)
    print("Random: ",numpy.mean(rACC)/60," +- ",numpy.std(rACC)/60 )
    print(rACC)
    
def code():
    plt.clf()
    viewL = ["NormalizedAST","CFG","DFG"]
    fr = open("Files/rfiles.txt")
    files = fr.read()
    files = files.replace(".R\n","\n")
    files = files.split("\n")
    files = files[:-1]
    
    timesCode = mt.mergeTime() 
    timesCode.load("Times/TimesOfCode")
    
    #AC
    timeAC_norm = []
    timeAC_cfg = []
    timeAC_dfg = []
    for n1 in viewL:
        for t1 in files:
            if n1 == "NormalizedAST":
                file1 = t1+"-.normalize"
            elif n1 == "CFG":
                file1 = t1+"-.cfg"
            elif n1 == "DFG":
                file1 = t1+"-.dfg"

            for n2 in viewL:
                if n1 != n2:   
                    file2 = ""
                    if n2 == "NormalizedAST":
                        file2 = t1+"-.normalize"
                    elif n2 == "CFG":
                        file2 = t1+"-.cfg"
                    elif n2 == "DFG":
                        file2 = t1+"-.dfg"
                        
                    if n1 == "NormalizedAST":
                        timeAC_norm.append(timesCode.timeAC[(file1,file2)])
                    elif n1 == "CFG":
                        timeAC_cfg.append(timesCode.timeAC[(file1,file2)])
                    elif n1 == "DFG":
                        timeAC_dfg.append(timesCode.timeAC[(file1,file2)])
               

    
    bar_plotAC = pd.DataFrame({'NormalizedAST':   timeAC_norm,'CFG':  timeAC_cfg,
      'DFG':  timeAC_dfg})
    # plot a bar chart
    ax = sns.barplot( data=bar_plotAC, estimator=np.mean, capsize=.2,errorbar = "sd", color='lightblue')
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('View')
    plt.ylabel ('Average merge time in s')
    plt.savefig("evaluation/codeMergeAC.pdf",dpi=300, bbox_inches = "tight")   
    plt.clf()
    
    #CC
    timeCC_norm = []
    timeCC_cfg = []
    timeCC_dfg = []
    for n1 in viewL:
        for t1 in files:
            if n1 == "NormalizedAST":
                file1 = t1+"-.normalize"
            elif n1 == "CFG":
                file1 = t1+"-.cfg"
            elif n1 == "DFG":
                file1 = t1+"-.dfg"

            for n2 in viewL:
                if n1 != n2:   
                    file2 = ""
                    if n2 == "NormalizedAST":
                        file2 = t1+"-.normalize"
                    elif n2 == "CFG":
                        file2 = t1+"-.cfg"
                    elif n2 == "DFG":
                        file2 = t1+"-.dfg"
                        
                    if n1 == "NormalizedAST":
                        timeCC_norm.append(timesCode.timeCC[(file1,file2)])
                    elif n1 == "CFG":
                        timeCC_cfg.append(timesCode.timeCC[(file1,file2)])
                    elif n1 == "DFG":
                        timeCC_dfg.append(timesCode.timeCC[(file1,file2)])
               

    
    bar_plotCC = pd.DataFrame({'NormalizedAST':   timeCC_norm,'CFG':  timeCC_cfg,
      'DFG':  timeCC_dfg})
    # plot a bar chart
    ax = sns.barplot( data=bar_plotCC, estimator=np.mean, capsize=.2,errorbar = "sd", color='lightblue')
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('View')
    plt.ylabel ('Average merge time in s')
    plt.savefig("evaluation/codeMergeCC.pdf",dpi=300, bbox_inches = "tight")   
    plt.clf()
    
    #ACC
    timeACC_norm = []
    timeACC_cfg = []
    timeACC_dfg = []
    for n1 in viewL:
        for t1 in files:
            if n1 == "NormalizedAST":
                file1 = t1+"-.normalize"
            elif n1 == "CFG":
                file1 = t1+"-.cfg"
            elif n1 == "DFG":
                file1 = t1+"-.dfg"

            for n2 in viewL:
                if n1 != n2:   
                    file2 = ""
                    if n2 == "NormalizedAST":
                        file2 = t1+"-.normalize"
                    elif n2 == "CFG":
                        file2 = t1+"-.cfg"
                    elif n2 == "DFG":
                        file2 = t1+"-.dfg"
                        
                    if n1 == "NormalizedAST":
                        timeACC_norm.append(timesCode.timeACC[(file1,file2)])
                    elif n1 == "CFG":
                        timeACC_cfg.append(timesCode.timeACC[(file1,file2)])
                    elif n1 == "DFG":
                        timeACC_dfg.append(timesCode.timeACC[(file1,file2)])
               

    
    bar_plotACC = pd.DataFrame({'NormalizedAST':   timeACC_norm,'CFG':  timeACC_cfg,
      'DFG':  timeACC_dfg})
    # plot a bar chart
    ax = sns.barplot( data=bar_plotACC, estimator=np.mean, capsize=.2,errorbar = "sd", color='lightblue')
    plt.xlabel ('View')
    plt.xticks(rotation = 45, ha='right')
    plt.ylabel ('Average merge time in s')
    plt.savefig("evaluation/codeMergeACC.pdf",dpi=300, bbox_inches = "tight")  

    
   


    
def news():
    plt.clf()
    newsL = ["Al-Jazeera","CNN","euronews"]
    topics = ["CERN",        "Facebook",   "NFL",          "Obesity",              "Twitter",  "Cigarettes",   "FIFA",       "Nintendo",     "StanfordUniversity",   "WarnerBros",  "Disney",       "NBA",        "NobelPrize",   "TikTok", "WorldHealthOrganization"]
    
    timesNews = mt.mergeTime() 
    timesNews.load("Times/TimesOfNews")
    
    #AC
    timeAC_CNN = []
    timeAC_euro = []
    timeAC_Al = []
    for n1 in newsL:
        for n2 in newsL: 
            if n2 != n1:
                for t1 in topics:
                    file1 = t1+"-"+n1     
                    file2 = t1+"-"+n2
                    if n1 == "Al-Jazeera":
                        timeAC_Al.append(timesNews.timeAC[(file1,file2)])
                    elif n1 == "CNN":
                        timeAC_CNN.append(timesNews.timeAC[(file1,file2)])
                    elif n1 == "euronews":
                        timeAC_euro.append(timesNews.timeAC[(file1,file2)])
    
    bar_plotAC = pd.DataFrame({'Al-Jazeera':  timeAC_Al,'Euro':  timeAC_euro,
      'CNN':  timeAC_CNN})
    # plot a bar chart
    ax = sns.barplot( data=bar_plotAC, estimator=np.mean, capsize=.2,errorbar = "sd", color='lightblue')
    plt.xlabel ('Broadcaster')
    plt.xticks(rotation = 45, ha='right')
    plt.ylabel ('Average merge time in s')
    plt.savefig("evaluation/newsMergeAC.pdf",dpi=300, bbox_inches = "tight")  
    plt.clf()
    
    #CC
    timeCC_CNN = []
    timeCC_euro = []
    timeCC_Al = []
    for n1 in newsL:
        for n2 in newsL: 
            if n2 != n1:
                for t1 in topics:
                    file1 = t1+"-"+n1     
                    file2 = t1+"-"+n2
                    if n1 == "Al-Jazeera":
                        timeCC_Al.append(timesNews.timeCC[(file1,file2)])
                    elif n1 == "CNN":
                        timeCC_CNN.append(timesNews.timeCC[(file1,file2)])
                    elif n1 == "euronews":
                        timeCC_euro.append(timesNews.timeCC[(file1,file2)])
    
    bar_plotCC = pd.DataFrame({'Al-Jazeera':  timeCC_Al,'Euro':  timeCC_euro,
      'CNN':  timeCC_CNN})
    # plot a bar chart
    ax = sns.barplot( data=bar_plotCC, estimator=np.mean, capsize=.2,errorbar = "sd", color='lightblue')
    plt.xlabel ('Broadcaster')
    plt.xticks(rotation = 45, ha='right')
    plt.ylabel ('Average merge time in s')
    plt.savefig("evaluation/newsMergeCC.pdf",dpi=300, bbox_inches = "tight")   
    plt.clf()
    
    #ACC
    timeACC_CNN = []
    timeACC_euro = []
    timeACC_Al = []
    for n1 in newsL:
        for n2 in newsL: 
            if n2 != n1:
                for t1 in topics:
                    file1 = t1+"-"+n1     
                    file2 = t1+"-"+n2
                    if n1 == "Al-Jazeera":
                        timeACC_Al.append(timesNews.timeACC[(file1,file2)])
                    elif n1 == "CNN":
                        timeACC_CNN.append(timesNews.timeACC[(file1,file2)])
                    elif n1 == "euronews":
                        timeACC_euro.append(timesNews.timeACC[(file1,file2)])
    
    bar_plotACC = pd.DataFrame({'Al-Jazeera':  timeACC_Al,'Euro':  timeACC_euro,
      'CNN':  timeACC_CNN})
    # plot a bar chart
    ax = sns.barplot( data=bar_plotACC, estimator=np.mean, capsize=.2,errorbar = "sd", color='lightblue')
    plt.xlabel ('Broadcaster')
    plt.xticks(rotation = 45, ha='right')
    plt.ylabel ('Average merge time in s')
    plt.savefig("evaluation/newsMergeACC.pdf",dpi=300, bbox_inches = "tight")  

def BTC2019():
    plt.clf()
    timesBTC = mt.mergeTime() 
    timesBTC.load("Times/TimesOfBTC2019")
    f1 = open("Files/files.txt","r")
    lineR = f1.read()
    linesNQ = lineR.replace(".nq","").split("\n")
    lines = lineR.replace(".nq","").replace("_00001","").split("\n")
    linesN = len(lines)
    f1.close()   
    f, ax = plt.subplots(figsize=(30, 5))
    
    edgesACs = []
    edgesCCs = []
    edgesACCs = []

    
    l = 0
    #loading phase:
    files = lineR.replace(".nq",".nq.gz")
    files = files.split("\n")
    for file in files:
        name = file.replace(".nq.gz","")
        if name != "btc2019-wikidata.org":

            summaryAC = gsg.summarySet()
            summaryAC.load("../data/BTC2019/"+file.replace(".nq.gz","")+"AC_Set")

            summaryCC = gsg.summarySet()
            summaryCC.load("../data/BTC2019/"+file.replace(".nq.gz","")+"CC_Set")

            summaryACC = gsg.summarySet()
            summaryACC.load("../data/BTC2019/"+file.replace(".nq.gz","")+"ACC_Set")
            
            edgesACs.append(len(summaryAC.edgesV)+len(summaryAC.edgesB)+len(summaryAC.edgesVB))
            edgesCCs.append(len(summaryCC.edgesV)+len(summaryCC.edgesB)+len(summaryCC.edgesVB))
            edgesACCs.append(len(summaryACC.edgesV)+len(summaryACC.edgesB)+len(summaryACC.edgesVB))
            
        else:
            summaryAC = gsg.summarySet()
            summaryAC.load("../data/wikidata/"+file.replace(".nq.gz","")+"AC_Set")

            summaryCC = gsg.summarySet()
            summaryCC.load("../data/wikidata/"+file.replace(".nq.gz","")+"CC_Set")

            summaryACC = gsg.summarySet()
            summaryACC.load("../data/wikidata/"+file.replace(".nq.gz","")+"ACC_Set")
            edgesACs.append(len(summaryAC.edgesV)+len(summaryAC.edgesB)+len(summaryAC.edgesVB))
            edgesCCs.append(len(summaryCC.edgesV)+len(summaryCC.edgesB)+len(summaryCC.edgesVB))
            edgesACCs.append(len(summaryACC.edgesV)+len(summaryACC.edgesB)+len(summaryACC.edgesVB))
        l +=1
    
    
    
    #AC
    times_AC = {}
    filesOrder = []
    for i in range(0,linesN):
        fileNQ1 = linesNQ[i]
        file1 = lines[i]
        filesOrder.append(lines[i])
        times_AC[file1] = []

        for j in range(0,linesN):
            fileNQ2 = linesNQ[j]
            if fileNQ1 != fileNQ2:
                times_AC[file1].append(timesBTC.timeAC[(fileNQ1,fileNQ2)])
    
    bar_plotAC = pd.DataFrame(times_AC)
    # plot a bar chart"Times/
    ax = sns.barplot( data=bar_plotAC, estimator=np.mean, capsize=.2,errorbar = "sd", color='lightblue')
    plt.xlabel ('PLD')
    plt.xticks(rotation = 45, ha='right')
    plt.ylabel ('Average merge time in s')
    
    ax2 = ax.twinx()
    dataAC = pd.DataFrame({"|E|":edgesACs},index =filesOrder)
    sns.lineplot( data=dataAC, ax=ax2, color='coral', marker='o')
    ax2.set_ylabel('Number of Edges')
    
    plt.savefig("evaluation/BTC2019MergeAC.pdf",dpi=300, bbox_inches = "tight")   
    plt.clf()
    
    #CC
    times_CC = {}
    filesOrder = []
    for i in range(0,linesN):
        fileNQ1 = linesNQ[i]
        file1 = lines[i]
        filesOrder.append(lines[i])
        #print(lines[i])
        times_CC[file1] = []
        for j in range(0,linesN):
            fileNQ2 = linesNQ[j]
            if fileNQ1 != fileNQ2:
                times_CC[file1].append(timesBTC.timeCC[(fileNQ1,fileNQ2)])
    
    bar_plotCC = pd.DataFrame(times_CC)
    # plot a bar chart
    ax = sns.barplot( data=bar_plotCC, estimator=np.mean, capsize=.2,errorbar = "sd", color='lightblue')
    plt.xlabel ('PLD')
    plt.xticks(rotation = 45, ha='right')
    plt.ylabel ('Average merge time in s')
    
    ax2 = ax.twinx()
    dataCC = pd.DataFrame({"|E|":edgesCCs},index =filesOrder)
    sns.lineplot( data=dataCC, ax=ax2, color='coral', marker='o')
    ax2.set_ylabel('Number of Edges')
    
    plt.savefig("evaluation/BTC2019MergeCC.pdf",dpi=300, bbox_inches = "tight")  
    plt.clf()
    
    #ACC
    times_ACC = {}
    filesOrder = []
    for i in range(0,linesN):
        fileNQ1 = linesNQ[i]
        file1 = lines[i]
        filesOrder.append(lines[i])
        #print(lines[i])
        times_ACC[file1] = []
        for j in range(0,linesN):
            fileNQ2 = linesNQ[j]
            if fileNQ1 != fileNQ2:
                times_ACC[file1].append(timesBTC.timeACC[(fileNQ1,fileNQ2)])
    
    bar_plotACC = pd.DataFrame(times_ACC)
    # plot a bar chart
    ax = sns.barplot( data=bar_plotACC, estimator=np.mean, capsize=.2,errorbar = "sd", color='lightblue')
    plt.xlabel ('PLD')
    plt.xticks(rotation = 45, ha='right')
    plt.ylabel ('Average merge time in s')
    ax2 = ax.twinx()
    dataACC = pd.DataFrame({"|E|":edgesACCs},index =filesOrder)
    sns.lineplot( data=dataACC, ax=ax2, color='coral', marker='o')
    ax2.set_ylabel('Number of Edges')
    plt.savefig("evaluation/BTC2019MergeACC.pdf",dpi=300, bbox_inches = "tight")  

def btcCor():
    print("BTC 2019 Correlation:")
    fr = open("Files/files.txt")
    files = fr.read()
    files = files.replace(".nq",".nq.gz")
    files = files.split("\n")

    times = mt.mergeTime() 
    times.name = "BTC"


    summaryACs = {}
    summaryCCs = {}
    summaryACCs = {}


    l = 0
    #loading phase:
    for file in files:
        name = file.replace(".nq.gz","")
        if name != "btc2019-wikidata.org":

            summaryACs[name] = gsg.summarySet()
            summaryACs[name].load("../data/BTC2019/"+file.replace(".nq.gz","")+"AC_Set")

            summaryCCs[name] = gsg.summarySet()
            summaryCCs[name].load("../data/BTC2019/"+file.replace(".nq.gz","")+"CC_Set")

            summaryACCs[name] = gsg.summarySet()
            summaryACCs[name].load("../data/BTC2019/"+file.replace(".nq.gz","")+"ACC_Set")

        else:
            summaryACs[name] = gsg.summarySet()
            summaryACs[name].load("../data/wikidata/"+file.replace(".nq.gz","")+"AC_Set")

            summaryCCs[name] = gsg.summarySet()
            summaryCCs[name].load("../data/wikidata/"+file.replace(".nq.gz","")+"CC_Set")

            summaryACCs[name] = gsg.summarySet()
            summaryACCs[name].load("../data/wikidata/"+file.replace(".nq.gz","")+"ACC_Set")

        l +=1

    
    timesNews = mt.mergeTime() 
    timesNews.load("Times/TimesOfBTC2019")
    
    n = ove.overlaps()
    n.load("analysis/BTCTest")
    
    xAC =[]
    xCC = []
    xACC = []
    
    xLAC =[]
    xLCC = []
    xLACC = []
    
    xAC2 =[]
    xCC2 = []
    xACC2 = []
    
    xPAC =[]
    xPCC = []
    xPACC = []
    
    xMAC =[]
    xMCC = []
    xMACC = []
    
    xC3AC = []
    xC3CC = []
    xC3ACC = []
    
    yAC =[]
    yCC = []
    yACC = []
    
    for file in files:
            name1 = file.replace(".nq.gz","")
            
            summary1AC_Set = summaryACs[name1]

            summary1CC_Set = summaryCCs[name1]

            summary1ACC_Set = summaryACCs[name1]

            for file2 in files:
                name2 = file2.replace(".nq.gz","")
                
                summary2AC_Set = summaryACs[name2]

                summary2CC_Set = summaryCCs[name2]

                summary2ACC_Set = summaryACCs[name2]

                if file != file2: 
                
                    edgesAC = len(summary1AC_Set.edgesV)+len(summary1AC_Set.edgesB)+len(summary1AC_Set.edgesVB)+len(summary2AC_Set.edgesV)+len(summary2AC_Set.edgesB)+len(summary2AC_Set.edgesVB)

                    edgesCC = len(summary1CC_Set.edgesV)+len(summary1CC_Set.edgesB)+len(summary1CC_Set.edgesVB)+len(summary2CC_Set.edgesV)+len(summary2CC_Set.edgesB)+len(summary2CC_Set.edgesVB)
                    edgesACC = len(summary1ACC_Set.edgesV)+len(summary1ACC_Set.edgesB)+len(summary1ACC_Set.edgesVB)+len(summary2ACC_Set.edgesV)+len(summary2ACC_Set.edgesB)+len(summary2ACC_Set.edgesVB)

                    if edgesAC > 0:

                        xAC.append(edgesAC)
                        xCC.append(edgesCC)
                        xACC.append(edgesACC)
                        
                        xAC2.append(edgesAC*edgesAC)
                        xCC2.append(edgesCC*edgesCC)
                        xACC2.append(edgesACC*edgesACC)

                        xLAC.append(numpy.log(edgesAC)*edgesAC)
                        xLCC.append(numpy.log(edgesCC)*edgesCC)
                        xLACC.append(numpy.log(edgesACC)*edgesACC)

                        xPAC.append(len(set.union(summary1AC_Set.payload,summary2AC_Set.payload)))
                        xPCC.append(len(set.union(summary1CC_Set.payload,summary2CC_Set.payload)))
                        xPACC.append(len(set.union(summary1ACC_Set.payload,summary2ACC_Set.payload)))

                        xMAC.append(len(set.union(summary1AC_Set.edgesB,summary2AC_Set.edgesB)))
                        xMCC.append(len(set.union(summary1CC_Set.edgesB,summary2CC_Set.edgesB)))
                        xMACC.append(len(set.union(summary1ACC_Set.edgesB,summary2ACC_Set.edgesB)))

                        xC3AC.append(n.Case3AC[(name1,name2)])
                        xC3CC.append(n.Case3CC[(name1,name2)])
                        xC3ACC.append(n.Case3ACC[(name1,name2)])


                        yAC.append(timesNews.timeAC[(name1,name2)])
                        yCC.append(timesNews.timeCC[(name1,name2)])
                        yACC.append(timesNews.timeACC[(name1,name2)])
    print("Samples :")
    print("AC: ",len(yAC))
    print("CC: ",len(yCC))
    print("ACC: ",len(yACC),"\n")

    print("Edges:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xAC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xAC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xAC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xCC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xCC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xCC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xACC, yACC) ) # Kendall's tau   
    
    
    
    print("\n\nEdges Log:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xLAC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xLAC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xLAC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xLCC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xLCC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xLCC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xLACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xLACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xLACC, yACC) ) # Kendall's tau  
    
    print("\n\nEdges Qua:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xAC2, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xAC2, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xAC2, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xCC2, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xCC2, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xCC2, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xACC2, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xACC2, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xACC2, yACC) ) # Kendall's tau  
    
    
    
    print("\n\nPayload:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xPAC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xPAC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xPAC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xPCC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xPCC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xPCC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xPACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xPACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xPACC, yACC) ) # Kendall's tau   
    
    
    print("\n\nMembers:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xMAC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xMAC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xMAC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xMCC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xMCC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xMCC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xMACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xMACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xMACC, yACC) ) # Kendall's tau   
    
    #Case3
    print("\n\nCase3:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xC3AC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xC3AC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xC3AC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xC3CC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xC3CC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xC3CC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xC3ACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xC3ACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xC3ACC, yACC) ) # Kendall's tau   

def newsCor():
    print("News Correlation:")
    newsL = ["Al-Jazeera","CNN","euronews"]
    topics = ["CERN",        "Facebook",   "NFL",          "Obesity",              "Twitter",  "Cigarettes",   "FIFA",       "Nintendo",     "StanfordUniversity",   "WarnerBros",  "Disney",       "NBA",        "NobelPrize",   "TikTok", "WorldHealthOrganization"]

    
    timesNews = mt.mergeTime() 
    timesNews.load("Times/Times/TimesOfNews")
    
    n = ove.overlaps()
    n.load("analysis/newsTest")
    
    xAC =[]
    xCC = []
    xACC = []
    
    xLAC =[]
    xLCC = []
    xLACC = []
    
    xAC2 =[]
    xCC2 = []
    xACC2 = []
    
    xPAC =[]
    xPCC = []
    xPACC = []
    
    xMAC =[]
    xMCC = []
    xMACC = []
    
    xC3AC = []
    xC3CC = []
    xC3ACC = []
    
    yAC =[]
    yCC = []
    yACC = []
    
    for topic in topics:
        for news in newsL:
            name1 = topic+"-"+news
          
            summary1AC_Set = gsg.summarySet()
            summary1AC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"AC_Set")

            summary1CC_Set = gsg.summarySet()
            summary1CC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"CC_Set")
            

            summary1ACC_Set = gsg.summarySet()
            summary1ACC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"ACC_Set")
            
            for news2 in newsL:
                if news != news2:
                    #print(news," ",news2)
                    name2 = topic+"-"+news2
                    summary2AC_Set = gsg.summarySet()
                    summary2AC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news2+"AC_Set")

                    summary2CC_Set = gsg.summarySet()
                    summary2CC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news2+"CC_Set")


                    summary2ACC_Set = gsg.summarySet()
                    summary2ACC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news2+"ACC_Set")
                
                    edgesAC = len(summary1AC_Set.edgesV)+len(summary1AC_Set.edgesB)+len(summary1AC_Set.edgesVB)+len(summary2AC_Set.edgesV)+len(summary2AC_Set.edgesB)+len(summary2AC_Set.edgesVB)
                    edgesCC = len(summary1CC_Set.edgesV)+len(summary1CC_Set.edgesB)+len(summary1CC_Set.edgesVB)+len(summary2CC_Set.edgesV)+len(summary2CC_Set.edgesB)+len(summary2CC_Set.edgesVB)
                    edgesACC = len(summary1ACC_Set.edgesV)+len(summary1ACC_Set.edgesB)+len(summary1ACC_Set.edgesVB)+len(summary2ACC_Set.edgesV)+len(summary2ACC_Set.edgesB)+len(summary2ACC_Set.edgesVB)
                    
                    if edgesAC > 0:
                        xAC.append(edgesAC)
                        xCC.append(edgesCC)
                        xACC.append(edgesACC)
                        
                        xAC2.append(edgesAC*edgesAC)
                        xCC2.append(edgesCC*edgesCC)
                        xACC2.append(edgesACC*edgesACC)

                        xLAC.append(numpy.log(edgesAC)*edgesAC)
                        xLCC.append(numpy.log(edgesCC)*edgesCC)
                        xLACC.append(numpy.log(edgesACC)*edgesACC)

                        xPAC.append(len(set.union(summary1AC_Set.payload,summary2AC_Set.payload)))
                        xPCC.append(len(set.union(summary1CC_Set.payload,summary2CC_Set.payload)))
                        xPACC.append(len(set.union(summary1ACC_Set.payload,summary2ACC_Set.payload)))

                        xMAC.append(len(set.union(summary1AC_Set.edgesB,summary2AC_Set.edgesB)))
                        xMCC.append(len(set.union(summary1CC_Set.edgesB,summary2CC_Set.edgesB)))
                        xMACC.append(len(set.union(summary1ACC_Set.edgesB,summary2ACC_Set.edgesB)))

                        xC3AC.append(n.Case3AC[(name1,name2)])
                        xC3CC.append(n.Case3CC[(name1,name2)])
                        xC3ACC.append(n.Case3ACC[(name1,name2)])


                        yAC.append(timesNews.timeAC[(name1,name2)])
                        yCC.append(timesNews.timeCC[(name1,name2)])
                        yACC.append(timesNews.timeACC[(name1,name2)])
    
    
    print("Samples :")
    print("AC: ",len(yAC))
    print("CC: ",len(yCC))
    print("ACC: ",len(yACC),"\n")

    print("Edges:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xAC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xAC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xAC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xCC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xCC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xCC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xACC, yACC) ) # Kendall's tau   
    
    print("\n\nEdges Log:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xLAC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xLAC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xLAC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xLCC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xLCC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xLCC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xLACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xLACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xLACC, yACC) ) # Kendall's tau  
    
    print("\n\nEdges Qua:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xAC2, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xAC2, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xAC2, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xCC2, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xCC2, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xCC2, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xACC2, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xACC2, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xACC2, yACC) ) # Kendall's tau 
    
    print("\n\nPayload:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xPAC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xPAC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xPAC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xPCC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xPCC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xPCC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xPACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xPACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xPACC, yACC) ) # Kendall's tau   
    
    
    print("\n\nMembers:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xMAC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xMAC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xMAC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xMCC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xMCC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xMCC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xMACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xMACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xMACC, yACC) ) # Kendall's tau   
    
    #Case3
    print("\n\nCase3:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xC3AC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xC3AC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xC3AC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xC3CC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xC3CC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xC3CC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xC3ACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xC3ACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xC3ACC, yACC) ) # Kendall's tau   

           

def codeCor():
    print("Code Correlation:")
    fr = open("Files/rfiles.txt")
    print("rfiles.txt")
    files = fr.read()
    files = files.replace(".R\n","\n")
    files = files.split("\n")
    fr.close()
    iC = 0
    files = files[:-1]

    
    timesNews = mt.mergeTime() 
    timesNews.load("Times/TimesOfCode")
    
    n = ove.overlaps()
    n.load("analysis/CodeTest")
    
    xAC =[]
    xCC = []
    xACC = []
    
    xLAC =[]
    xLCC = []
    xLACC = []
    
    xAC2 =[]
    xCC2 = []
    xACC2 = []
    
    xPAC =[]
    xPCC = []
    xPACC = []
    
    xMAC =[]
    xMCC = []
    xMACC = []
    
    xC3AC = []
    xC3CC = []
    xC3ACC = []
    
    yAC =[]
    yCC = []
    yACC = []
    
    allI = len(files)
    for file in files:
        iC += 1

        for part in [".dfg",".cfg",".normalize"]:
            name1 = file+"-"+part
            summary1AC_Set = gsg.summarySet()
            summary1AC_Set.load("../data/"+file+part+"AC_Set")

            summary1CC_Set = gsg.summarySet()
            summary1CC_Set.load("../data/"+file+part+"CC_Set")
            

            summary1ACC_Set = gsg.summarySet()
            summary1ACC_Set.load("../data/"+file+part+"ACC_Set")

            for part2 in [".dfg",".cfg",".normalize"]:
                if part != part2:
                    name2 = file+"-"+part2
                    summary2AC_Set = gsg.summarySet()
                    summary2AC_Set.load("../data/"+file+part2+"AC_Set")

                    summary2CC_Set = gsg.summarySet()
                    summary2CC_Set.load("../data/"+file+part2+"CC_Set")


                    summary2ACC_Set = gsg.summarySet()
                    summary2ACC_Set.load("../data/"+file+part2+"ACC_Set")

                    edgesAC = len(summary1AC_Set.edgesV)+len(summary1AC_Set.edgesB)+len(summary1AC_Set.edgesVB)+len(summary2AC_Set.edgesV)+len(summary2AC_Set.edgesB)+len(summary2AC_Set.edgesVB)

                    edgesCC = len(summary1CC_Set.edgesV)+len(summary1CC_Set.edgesB)+len(summary1CC_Set.edgesVB)+len(summary2CC_Set.edgesV)+len(summary2CC_Set.edgesB)+len(summary2CC_Set.edgesVB)
                    edgesACC = len(summary1ACC_Set.edgesV)+len(summary1ACC_Set.edgesB)+len(summary1ACC_Set.edgesVB)+len(summary2ACC_Set.edgesV)+len(summary2ACC_Set.edgesB)+len(summary2ACC_Set.edgesVB)

                    if edgesAC > 0:

                        xAC.append(edgesAC)
                        xCC.append(edgesCC)
                        xACC.append(edgesACC)
                        
                        xAC2.append(edgesAC*edgesAC)
                        xCC2.append(edgesCC*edgesCC)
                        xACC2.append(edgesACC*edgesACC)

                        xLAC.append(numpy.log(edgesAC)*edgesAC)
                        xLCC.append(numpy.log(edgesCC)*edgesCC)
                        xLACC.append(numpy.log(edgesACC)*edgesACC)

                        xPAC.append(len(set.union(summary1AC_Set.payload,summary2AC_Set.payload)))
                        xPCC.append(len(set.union(summary1CC_Set.payload,summary2CC_Set.payload)))
                        xPACC.append(len(set.union(summary1ACC_Set.payload,summary2ACC_Set.payload)))

                        xMAC.append(len(set.union(summary1AC_Set.edgesB,summary2AC_Set.edgesB)))
                        xMCC.append(len(set.union(summary1CC_Set.edgesB,summary2CC_Set.edgesB)))
                        xMACC.append(len(set.union(summary1ACC_Set.edgesB,summary2ACC_Set.edgesB)))

                        xC3AC.append(n.Case3AC[(name1,name2)])
                        xC3CC.append(n.Case3CC[(name1,name2)])
                        xC3ACC.append(n.Case3ACC[(name1,name2)])


                        yAC.append(timesNews.timeAC[(name1,name2)])
                        yCC.append(timesNews.timeCC[(name1,name2)])
                        yACC.append(timesNews.timeACC[(name1,name2)])
    
    print("Samples :")
    print("AC: ",len(yAC))
    print("CC: ",len(yCC))
    print("ACC: ",len(yACC),"\n")

    print("Edges:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xAC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xAC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xAC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xCC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xCC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xCC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xACC, yACC) ) # Kendall's tau   
    
    print("\n\nEdges Log:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xLAC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xLAC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xLAC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xLCC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xLCC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xLCC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xLACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xLACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xLACC, yACC) ) # Kendall's tau  
    
    print("\n\nEdges Qua:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xAC2, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xAC2, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xAC2, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xCC2, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xCC2, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xCC2, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xACC2, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xACC2, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xACC2, yACC) ) # Kendall's tau 
    
    print("\n\nPayload:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xPAC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xPAC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xPAC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xPCC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xPCC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xPCC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xPACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xPACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xPACC, yACC) ) # Kendall's tau   
    
    
    print("\n\nMembers:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xMAC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xMAC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xMAC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xMCC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xMCC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xMCC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xMACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xMACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xMACC, yACC) ) # Kendall's tau   
    
    #Case3
    print("\n\nCase3:")
    print("\nAC")
    print("Pearson: ",scipy.stats.pearsonr(xC3AC, yAC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xC3AC, yAC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xC3AC, yAC) ) # Kendall's tau     
    
    print("\nCC")
    print("Pearson: ",scipy.stats.pearsonr(xC3CC, yCC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xC3CC, yCC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xC3CC, yCC) ) # Kendall's tau     
    
    print("\nACC")
    print("Pearson: ",scipy.stats.pearsonr(xC3ACC, yACC) )   # Pearson's r
    print("Spearman: ",scipy.stats.spearmanr(xC3ACC, yACC) )  # Spearman's rho
    print("Kendall: ",scipy.stats.kendalltau(xC3ACC, yACC) ) # Kendall's tau   

    

    
def codeReg():
    fr = open("Files/rfiles.txt")
    print("rfiles.txt")
    files = fr.read()
    files = files.replace(".R\n","\n")
    files = files.split("\n")
    fr.close()
    iC = 0
    files = files[:-1]

    timesNews = mt.mergeTime() 
    timesNews.load("Times/TimesOfCode")
    
    xAC =[]
    xCC = []
    xACC = []

    yAC =[]
    yCC = []
    yACC = []
    
    allI = len(files)
    for file in files:
        iC += 1
        if iC % 1000 == 0:
            print(str((iC/allI)*100),"%")
        for part in [".dfg",".cfg",".normalize"]:
            name1 = file+"-"+part
            summary1AC_Set = gsg.summarySet()
            summary1AC_Set.load("../data/"+file+part+"AC_Set")

            summary1CC_Set = gsg.summarySet()
            summary1CC_Set.load("../data/"+file+part+"CC_Set")
            

            summary1ACC_Set = gsg.summarySet()
            summary1ACC_Set.load("../data/"+file+part+"ACC_Set")
            
            for part2 in [".dfg",".cfg",".normalize"]:
                if part != part2:
                    name2 = file+"-"+part2
                    summary2AC_Set = gsg.summarySet()
                    summary2AC_Set.load("../data/"+file+part2+"AC_Set")

                    summary2CC_Set = gsg.summarySet()
                    summary2CC_Set.load("../data/"+file+part2+"CC_Set")


                    summary2ACC_Set = gsg.summarySet()
                    summary2ACC_Set.load("../data/"+file+part2+"ACC_Set")
            
                    edgesAC = len(summary1AC_Set.edgesV)+len(summary1AC_Set.edgesB)+len(summary1AC_Set.edgesVB)+len(summary2AC_Set.edgesV)+len(summary2AC_Set.edgesB)+len(summary2AC_Set.edgesVB)
                    edgesCC = len(summary1CC_Set.edgesV)+len(summary1CC_Set.edgesB)+len(summary1CC_Set.edgesVB)+len(summary2CC_Set.edgesV)+len(summary2CC_Set.edgesB)+len(summary2CC_Set.edgesVB)
                    edgesACC = len(summary1ACC_Set.edgesV)+len(summary1ACC_Set.edgesB)+len(summary1ACC_Set.edgesVB)+len(summary2ACC_Set.edgesV)+len(summary2ACC_Set.edgesB)+len(summary2ACC_Set.edgesVB)
                    
                    if edgesAC > 0:
                        xAC.append(edgesAC)
                        xCC.append(edgesCC)
                        xACC.append(edgesACC)

                        yAC.append(timesNews.timeAC[(name1,name2)])
                        yCC.append(timesNews.timeCC[(name1,name2)])
                        yACC.append(timesNews.timeACC[(name1,name2)])
    
    #AC 
    f = open("regression/CodeACRegression.txt","w+")
    plt.clf()
    dAC = pd.DataFrame({'|E|': xAC,
                   'Time in s': yAC})
    ax = sns.scatterplot(data=dAC, x='|E|', y='Time in s')
    
    fit = stats.linregress(xAC, yAC)
    grid = np.linspace(min(xAC), max(xAC))
    ax.plot(grid, fit.intercept + fit.slope * grid, color="b", lw=1,label="|E|")
    f.write("Linear: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    fit = stats.linregress(np.log(xAC)*xAC, yAC)
    grid = np.linspace(min(xAC), max(xAC))
    ax.plot(grid, fit.intercept + fit.slope * np.log(grid)*grid, color="black", lw=1,label='|E|log(|E|)')
    f.write("Logarithm: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|log(|E|)+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    fit = stats.linregress(np.square(xAC), yAC)
    grid = np.linspace(min(xAC), max(xAC))
    ax.plot(grid, fit.intercept + fit.slope * np.square(grid), color="r", lw=1,label='|E|²')
    f.write("Quadratic: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E^2|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    ax.legend(loc="best")
    plt.savefig("regression/CodeACRegression.png",dpi=300, bbox_inches = "tight")    
    
    #CC 
    f = open("regression/CodeCCRegression.txt","w+")
    plt.clf()
    dCC = pd.DataFrame({'|E|': xCC,
                   'Time in s': yCC})
    ax = sns.scatterplot(data=dCC, x='|E|', y='Time in s')
    
    fit = stats.linregress(xCC, yCC)
    grid = np.linspace(min(xCC), max(xCC))
    ax.plot(grid, fit.intercept + fit.slope * grid, color="b", lw=1,label="|E|")
    f.write("Linear: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    
    fit = stats.linregress(np.log(xCC)*xCC, yCC)
    grid = np.linspace(min(xCC), max(xCC))
    ax.plot(grid, fit.intercept + fit.slope * np.log(grid)*grid, color="black", lw=1,label='|E|log(|E|)')
    f.write("Logarithm: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|log(|E|)+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    fit = stats.linregress(np.square(xCC), yCC)
    grid = np.linspace(min(xCC), max(xCC))
    ax.plot(grid, fit.intercept + fit.slope * np.square(grid), color="r", lw=1,label='|E|²')
    f.write("Quadratic: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E^2|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    ax.legend(loc="best")
    plt.savefig("regression/CodeCCRegression.png",dpi=300, bbox_inches = "tight")    
    
    #ACC 
    f = open("regression/CodeACCRegression.txt","w+")
    plt.clf()
    dACC = pd.DataFrame({'|E|': xACC,
                   'Time in s': yACC})
    ax = sns.scatterplot(data=dACC, x='|E|', y='Time in s')
    
    fit = stats.linregress(xACC, yACC)
    grid = np.linspace(min(xACC), max(xACC))
    ax.plot(grid, fit.intercept + fit.slope * grid, color="b", lw=1,label="|E|")
    f.write("Linear: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
  
    
    fit = stats.linregress(np.log(xACC)*xACC, yACC)
    grid = np.linspace(min(xACC), max(xACC))
    ax.plot(grid, fit.intercept + fit.slope * np.log(grid)*grid, color="black", lw=1,label='|E|log(|E|)')
    f.write("Logarithm: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|log(|E|)+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    
    fit = stats.linregress(np.square(xACC), yACC)
    grid = np.linspace(min(xACC), max(xACC))
    ax.plot(grid, fit.intercept + fit.slope * np.square(grid), color="r", lw=1,label='|E|²')
    f.write("Quadratic: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E^2|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    ax.legend(loc="best")
    plt.savefig("regression/CodeACCRegression.png",dpi=300, bbox_inches = "tight")    
    plt.clf()
    
def newsReg():
    newsL = ["Al-Jazeera","CNN","euronews"]
    topics = ["CERN",        "Facebook",   "NFL",          "Obesity",              "Twitter",  "Cigarettes",   "FIFA",       "Nintendo",     "StanfordUniversity",   "WarnerBros",  "Disney",       "NBA",        "NobelPrize",   "TikTok", "WorldHealthOrganization"]

    
    timesNews = mt.mergeTime() 
    timesNews.load("Times/TimesOfNews")
    

    
    xAC =[]
    xCC = []
    xACC = []
    
    yAC =[]
    yCC = []
    yACC = []
    
    for topic in topics:
        for news in newsL:
            name1 = topic+"-"+news
          
            summary1AC_Set = gsg.summarySet()
            summary1AC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"AC_Set")

            summary1CC_Set = gsg.summarySet()
            summary1CC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"CC_Set")
            

            summary1ACC_Set = gsg.summarySet()
            summary1ACC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"ACC_Set")
            
            for news2 in newsL:
                if news != news2:
                    name2 = topic+"-"+news2
                    summary2AC_Set = gsg.summarySet()
                    summary2AC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news2+"AC_Set")

                    summary2CC_Set = gsg.summarySet()
                    summary2CC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news2+"CC_Set")


                    summary2ACC_Set = gsg.summarySet()
                    summary2ACC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news2+"ACC_Set")
            
                    edgesAC = len(summary1AC_Set.edgesV)+len(summary1AC_Set.edgesB)+len(summary1AC_Set.edgesVB)+len(summary2AC_Set.edgesV)+len(summary2AC_Set.edgesB)+len(summary2AC_Set.edgesVB)
                    edgesCC = len(summary1CC_Set.edgesV)+len(summary1CC_Set.edgesB)+len(summary1CC_Set.edgesVB)+len(summary2CC_Set.edgesV)+len(summary2CC_Set.edgesB)+len(summary2CC_Set.edgesVB)
                    edgesACC = len(summary1ACC_Set.edgesV)+len(summary1ACC_Set.edgesB)+len(summary1ACC_Set.edgesVB)+len(summary2ACC_Set.edgesV)+len(summary2ACC_Set.edgesB)+len(summary2ACC_Set.edgesVB)
                    xAC.append(edgesAC)
                    xCC.append(edgesCC)
                    xACC.append(edgesACC)

                    yAC.append(timesNews.timeAC[(name1,name2)])
                    yCC.append(timesNews.timeCC[(name1,name2)])
                    yACC.append(timesNews.timeACC[(name1,name2)])


    #AC 
    f = open("regression/NewsACRegression.txt","w+")
    plt.clf()
    dAC = pd.DataFrame({'|E|': xAC,
                   'Time in s': yAC})
    ax = sns.scatterplot(data=dAC, x='|E|', y='Time in s')
    
    fit = stats.linregress(xAC, yAC)
    grid = np.linspace(min(xAC), max(xAC))
    ax.plot(grid, fit.intercept + fit.slope * grid, color="b", lw=1,label="|E|")
    f.write("Linear: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    
    fit = stats.linregress(np.log(xAC)*xAC, yAC)
    grid = np.linspace(min(xAC), max(xAC))
    ax.plot(grid, fit.intercept + fit.slope * np.log(grid)*grid, color="black", lw=1,label='|E|log(|E|)')
    f.write("Logarithm: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|log(|E|)+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    fit = stats.linregress(np.square(xAC), yAC)
    grid = np.linspace(min(xAC), max(xAC))
    ax.plot(grid, fit.intercept + fit.slope * np.square(grid), color="r", lw=1,label='|E|²')
    f.write("Quadratic: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E^2|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    ax.legend(loc="best")
    plt.savefig("regression/NewsACRegression.png",dpi=300, bbox_inches = "tight")    
    
    #CC 
    f = open("regression/NewsCCRegression.txt","w+")
    plt.clf()
    dCC = pd.DataFrame({'|E|': xCC,
                   'Time in s': yCC})
    ax = sns.scatterplot(data=dCC, x='|E|', y='Time in s')
    
    fit = stats.linregress(xCC, yCC)
    grid = np.linspace(min(xCC), max(xCC))
    ax.plot(grid, fit.intercept + fit.slope * grid, color="b", lw=1,label="|E|")
    f.write("Linear: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    
    fit = stats.linregress(np.log(xCC)*xCC, yCC)
    grid = np.linspace(min(xCC), max(xCC))
    ax.plot(grid, fit.intercept + fit.slope * np.log(grid)*grid, color="black", lw=1,label='|E|log(|E|)')
    f.write("Logarithm: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|log(|E|)+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    fit = stats.linregress(np.square(xCC), yCC)
    grid = np.linspace(min(xCC), max(xCC))
    ax.plot(grid, fit.intercept + fit.slope * np.square(grid), color="r", lw=1,label='|E|²')
    f.write("Quadratic: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E^2|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    ax.legend(loc="best")
    plt.savefig("regression/NewsCCRegression.png",dpi=300, bbox_inches = "tight")    
    
    #ACC 
    f = open("regression/NewsACCRegression.txt","w+")
    plt.clf()
    dACC = pd.DataFrame({'|E|': xACC,
                   'Time in s': yACC})
    ax = sns.scatterplot(data=dACC, x='|E|', y='Time in s')
    
    fit = stats.linregress(xACC, yACC)
    grid = np.linspace(min(xACC), max(xACC))
    ax.plot(grid, fit.intercept + fit.slope * grid, color="b", lw=1,label="|E|")
    f.write("Linear: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
  
    
    fit = stats.linregress(np.log(xACC)*xACC, yACC)
    grid = np.linspace(min(xACC), max(xACC))
    ax.plot(grid, fit.intercept + fit.slope * np.log(grid)*grid, color="black", lw=1,label='|E|log(|E|)')
    f.write("Logarithm: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|log(|E|)+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    
    fit = stats.linregress(np.square(xACC), yACC)
    grid = np.linspace(min(xACC), max(xACC))
    ax.plot(grid, fit.intercept + fit.slope * np.square(grid), color="r", lw=1,label='|E|²')
    f.write("Quadratic: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E^2|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    ax.legend(loc="best")
    plt.savefig("regression/NewsACCRegression.png",dpi=300, bbox_inches = "tight")    
    plt.clf()
    

def btcReg():
    fr = open("Files/files.txt")
    files = fr.read()
    files = files.replace(".nq",".nq.gz")
    files = files.split("\n")

    times = mt.mergeTime() 
    times.name = "BTC"

    summaryACs = {}
    summaryCCs = {}
    summaryACCs = {}


    l = 0
    #loading phase:

    for file in files:
        name = file.replace(".nq.gz","")
        if name != "btc2019-wikidata.org":

            summaryACs[name] = gsg.summarySet()
            summaryACs[name].load("../data/BTC2019/"+file.replace(".nq.gz","")+"AC_Set")

            summaryCCs[name] = gsg.summarySet()
            summaryCCs[name].load("../data/BTC2019/"+file.replace(".nq.gz","")+"CC_Set")

            summaryACCs[name] = gsg.summarySet()
            summaryACCs[name].load("../data/BTC2019/"+file.replace(".nq.gz","")+"ACC_Set")
        else:
            summaryACs[name] = gsg.summarySet()
            summaryACs[name].load("../data/wikidata/"+file.replace(".nq.gz","")+"AC_Set")

            summaryCCs[name] = gsg.summarySet()
            summaryCCs[name].load("../data/wikidata/"+file.replace(".nq.gz","")+"CC_Set")

            summaryACCs[name] = gsg.summarySet()
            summaryACCs[name].load("../data/wikidata/"+file.replace(".nq.gz","")+"ACC_Set")

        l +=1
        print(l," of ",len(files)," loaded.")

    
    timesNews = mt.mergeTime() 
    timesNews.load("Times/TimesOfBTC2019")
    

    
    

    
    xAC =[]
    xCC = []
    xACC = []
    
    yAC =[]
    yCC = []
    yACC = []
    
    for file in files:
            name1 = file.replace(".nq.gz","")
            print("First: ",name1)

            summary1AC_Set = summaryACs[name1]

            summary1CC_Set = summaryCCs[name1]

            summary1ACC_Set = summaryACCs[name1]

            for file2 in files:
                name2 = file2.replace(".nq.gz","")
                print("Second: ",name2)
                summary2AC_Set = summaryACs[name2]

                summary2CC_Set = summaryCCs[name2]

                summary2ACC_Set = summaryACCs[name2]
                if file != file2: 

                    edgesAC = len(summary1AC_Set.edgesV)+len(summary1AC_Set.edgesB)+len(summary1AC_Set.edgesVB)+len(summary2AC_Set.edgesV)+len(summary2AC_Set.edgesB)+len(summary2AC_Set.edgesVB)
                    edgesCC = len(summary1CC_Set.edgesV)+len(summary1CC_Set.edgesB)+len(summary1CC_Set.edgesVB)+len(summary2CC_Set.edgesV)+len(summary2CC_Set.edgesB)+len(summary2CC_Set.edgesVB)
                    edgesACC = len(summary1ACC_Set.edgesV)+len(summary1ACC_Set.edgesB)+len(summary1ACC_Set.edgesVB)+len(summary2ACC_Set.edgesV)+len(summary2ACC_Set.edgesB)+len(summary2ACC_Set.edgesVB)
                    xAC.append(edgesAC)
                    xCC.append(edgesCC)
                    xACC.append(edgesACC)

                    yAC.append(timesNews.timeAC[(name1,name2)])
                    yCC.append(timesNews.timeCC[(name1,name2)])
                    yACC.append(timesNews.timeACC[(name1,name2)])
    
    #AC 
    f = open("regression/BTCACRegression.txt","w+")
    plt.clf()
    dAC = pd.DataFrame({'|E|': xAC,
                   'Time in s': yAC})
    ax = sns.scatterplot(data=dAC, x='|E|', y='Time in s')
    
    fit = stats.linregress(xAC, yAC)
    grid = np.linspace(min(xAC), max(xAC))
    ax.plot(grid, fit.intercept + fit.slope * grid, color="b", lw=1,label="|E|")
    f.write("Linear: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    
    fit = stats.linregress(np.log(xAC)*xAC, yAC)
    grid = np.linspace(min(xAC), max(xAC))
    ax.plot(grid, fit.intercept + fit.slope * np.log(grid)*grid, color="black", lw=1,label='|E|log(|E|)')
    f.write("Logarithm: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|log(|E|)+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    fit = stats.linregress(np.square(xAC), yAC)
    grid = np.linspace(min(xAC), max(xAC))
    ax.plot(grid, fit.intercept + fit.slope * np.square(grid), color="r", lw=1,label='|E|²')
    f.write("Quadratic: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E^2|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    ax.legend(loc="best")
    plt.savefig("regression/BTCACRegression.png",dpi=300, bbox_inches = "tight")    
    
    #CC 
    f = open("regression/BTCCCRegression.txt","w+")
    plt.clf()
    dCC = pd.DataFrame({'|E|': xCC,
                   'Time in s': yCC})
    ax = sns.scatterplot(data=dCC, x='|E|', y='Time in s')
    
    fit = stats.linregress(xCC, yCC)
    grid = np.linspace(min(xCC), max(xCC))
    ax.plot(grid, fit.intercept + fit.slope * grid, color="b", lw=1,label="|E|")
    f.write("Linear: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    
    fit = stats.linregress(np.log(xCC)*xCC, yCC)
    grid = np.linspace(min(xCC), max(xCC))
    ax.plot(grid, fit.intercept + fit.slope * np.log(grid)*grid, color="black", lw=1,label='|E|log(|E|)')
    f.write("Logarithm: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|log(|E|)+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    fit = stats.linregress(np.square(xCC), yCC)
    grid = np.linspace(min(xCC), max(xCC))
    ax.plot(grid, fit.intercept + fit.slope * np.square(grid), color="r", lw=1,label='|E|²')
    f.write("Quadratic: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E^2|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    ax.legend(loc="best")
    plt.savefig("regression/BTCCCRegression.png",dpi=300, bbox_inches = "tight")    
    
    #ACC 
    f = open("regression/BTCACCRegression.txt","w+")
    plt.clf()
    dACC = pd.DataFrame({'|E|': xACC,
                   'Time in s': yACC})
    ax = sns.scatterplot(data=dACC, x='|E|', y='Time in s')
    
    fit = stats.linregress(xACC, yACC)
    grid = np.linspace(min(xACC), max(xACC))
    ax.plot(grid, fit.intercept + fit.slope * grid, color="b", lw=1,label="|E|")
    f.write("Linear: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
  
    
    fit = stats.linregress(np.log(xACC)*xACC, yACC)
    grid = np.linspace(min(xACC), max(xACC))
    ax.plot(grid, fit.intercept + fit.slope * np.log(grid)*grid, color="black", lw=1,label='|E|log(|E|)')
    f.write("Logarithm: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E|log(|E|)+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    
    fit = stats.linregress(np.square(xACC), yACC)
    grid = np.linspace(min(xACC), max(xACC))
    ax.plot(grid, fit.intercept + fit.slope * np.square(grid), color="r", lw=1,label='|E|²')
    f.write("Quadratic: \n")
    f.write('{:0.3e}'.format(fit.slope)+"|E^2|+"+'{:0.3e}'.format(fit.intercept)+"\n")
    f.write("r^2: "+str(fit.rvalue)+"\n")
    f.write("p-value: "+str(fit.pvalue)+"\n")
    f.write("intercept_stderr: "+str(fit.intercept_stderr)+"\n")
    f.write("std_err: "+str(fit.stderr)+"\n\n")
    
    ax.legend(loc="best")
    plt.savefig("regression/BTCACCRegression.png",dpi=300, bbox_inches = "tight")    
    plt.clf()
    
    
def main():
    #Times for the BTC 2019 Merge
    timesBTC_2019()
    
    #Average Time for pairwise merging
    news()
    code()
    BTC2019()
    
    #Correlation
    newsCor()
    btcCor()
    codeCor()
    
    #Linear regression
    newsReg()
    btcReg()
    codeReg()

    
if __name__ == "__main__":
    main()

