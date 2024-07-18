import argparse
import configparser
import site
import sys
import re 
import pickle
site.addsitedir('../lib')  # Always appends to end


from graph_summary_generator import summary as gsg
from graph_summary_generator import overlaps  as ove
import pathlib
import gzip
    
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl

import seaborn as sns
sns.set_theme()
from matplotlib.colors import LogNorm, Normalize
from matplotlib.ticker import MaxNLocator

def show(name,times):
    n = ove.overlaps()
    n.load(name)
    print(name,":")
    print("Edges: ",n.noEdges)
    print("Vertices: ",n.noVertices)
    print("AC: ",n.noAC)
    print("CC: ",n.noCC)
    print("ACC: ",n.noACC)   
    
    
    ovAC = 0
    allAC = 0
    for i,j in n.ovAC.keys():
        if i != j:
            ovAC+= n.ovAC[(i,j)]
        else:
            allAC  += n.ovAC[(i,j)]
    allAC = times*allAC
    print("ov_AC: ",ovAC/allAC)
    
    ovCC = 0
    allCC = 0
    for i,j in n.ovCC.keys():
        if i != j:
            ovCC+= n.ovCC[(i,j)]
        else:
            allCC  += n.ovCC[(i,j)]
    allCC = times*allCC
    print("ov_CC: ",ovCC/allCC)
    
    ovACC = 0
    allACC = 0
    for i,j in n.ovACC.keys():
        if i != j:
            ovACC+= n.ovACC[(i,j)]
        else:
            allACC  += n.ovACC[(i,j)]
    allACC = times*allACC
    print("ov_ACC: ",ovACC/allACC)
    
    Case1 = 0
    Case2 = 0
    Case3 = 0
    All = 0
    for i,j in n.Case1AC.keys():
        if i != j:
            Case1 += n.Case1AC[(i,j)]
        else:
            All += n.Case1AC[(i,j)]
            
    for i,j in n.Case2AC.keys():
        if i != j:
            Case2 += n.Case2AC[(i,j)]
            
    for i,j in n.Case3AC.keys():
        if i != j:
            Case3 += n.Case3AC[(i,j)]
    All = All*times
    print("AC_Case1:", Case1/All)
    print("AC_Case2:", Case2/All)
    print("AC_Case3:", Case3/All)
    print((Case1+Case2+Case3)/All)
    
    Case1 = 0
    Case2 = 0
    Case3 = 0
    All = 0
    for i,j in n.Case1CC.keys():
        if i != j:
            Case1 += n.Case1CC[(i,j)]
        else:
            All += n.Case1CC[(i,j)]
            
    for i,j in n.Case2CC.keys():
        if i != j:
            Case2 += n.Case2CC[(i,j)]
            
    for i,j in n.Case3CC.keys():
        if i != j:
            Case3 += n.Case3CC[(i,j)]
    All = All*times
    print("CC_Case1:", Case1/All)
    print("CC_Case2:", Case2/All)
    print("CC_Case3:", Case3/All)
    print((Case1+Case2+Case3)/All)
    
    Case1 = 0
    Case2 = 0
    Case3 = 0
    All = 0
    for i,j in n.Case1ACC.keys():
        if i != j:
            Case1 += n.Case1ACC[(i,j)]
        else:
            All += n.Case1ACC[(i,j)]
            
    for i,j in n.Case2ACC.keys():
        if i != j:
            Case2 += n.Case2ACC[(i,j)]
            
    for i,j in n.Case3ACC.keys():
        if i != j:
            Case3 += n.Case3ACC[(i,j)]
    All = All*times
    print("ACC_Case1:", Case1/All)
    print("ACC_Case2:", Case2/All)
    print("ACC_Case3:", Case3/All)
    print((Case1+Case2+Case3)/All)
    
    ovV = 0
    allV = 0
    for i,j in n.ovVertices.keys():
        if i != j:
            ovV += n.ovVertices[(i,j)]
        else:
            allV  += n.ovVertices[(i,j)]
    allV = times*allV
    print("ov_Vertices: ",ovV/allV )
    
    ovP = 0
    allP = 0
    for i,j in n.ovPredicates.keys():
        if i != j:
            ovP += n.ovPredicates[(i,j)]
        else:
            allP  += n.ovPredicates [(i,j)]
    allP= times*allP
    print("ov_Predicates: ",ovP/allP )
    print()
    

    
def codeAll():
    n = ove.overlaps()
    allAC = set()
    allCC = set()
    allACC = set()
    
    allVertices = set()
    
    for i in range(14):
        print(i+1," of 14")
        nc = ove.overlapsCode()
        nc.load("analysis/CodeTest"+str(i))
        
        allAC = allAC.union(nc.noAC)
        allCC = allCC.union(nc.noCC)
        allACC = allACC.union(nc.noACC)
        
        allVertices = allVertices.union(nc.noVertices)
        
        n.ovAC.update(nc.ovAC) 
        n.ovCC.update(nc.ovCC) 
        n.ovACC.update(nc.ovACC) 
        
        n.Case1AC.update(nc.Case1AC)
        n.Case2AC.update(nc.Case2AC)
        n.Case3AC.update(nc.Case3AC)
        
        n.Case1CC.update(nc.Case1CC)
        n.Case2CC.update(nc.Case2CC)
        n.Case3CC.update(nc.Case3CC)
        
        n.Case1ACC.update(nc.Case1ACC)
        n.Case2ACC.update(nc.Case2ACC)
        n.Case3ACC.update(nc.Case3ACC)
        
        n.ovVertices.update(nc.ovVertices)
        n.ovPredicates.update(nc.ovPredicates)
        
        n.noEdges += nc.noEdges
        
        
    n.noAC = len(allAC)
    n.noCC = len(allCC)
    n.noACC = len(allACC)
    n.noVertices =len(allVertices)  
    n.save("analysis/CodeTest")
       
def drawBTC():
    n = ove.overlaps()
    n.load("analysis/BTCTest")
    
    f1 = open("files.txt","r")
    lineR = f1.read()
    linesNQ = lineR.replace(".nq","").split("\n")
    lines = lineR.replace(".nq","").replace("_00001","").split("\n")
    linesN = len(lines)
    f1.close()
    
    ovAC1 ={}
    ovACC1 ={}
    ovCC1 ={}
    
    ovAC2 ={}
    ovACC2 ={}
    ovCC2 ={}
    
    ovAC3 ={}
    ovACC3 ={}
    ovCC3 ={}
    
    for i in range(0,linesN):
        ovAC1[i] = 0
        ovACC1[i] = 0
        ovCC1[i] = 0
        
        ovAC2[i] = 0
        ovACC2[i] = 0
        ovCC2[i] = 0
        
        ovAC3[i] = 0
        ovACC3[i] = 0
        ovCC3[i] = 0
    fileV = {}    
    filesOrder = []
    for i in range(0,linesN):
        filesOrder.append(lines[i])
        file1 = linesNQ[i]
        fileV[i] = n.ovVertices[(file1,file1)]
        for j in range(0,linesN):
            file2 = linesNQ[j]
            if i != j:
                ovAC1[i] += n.Case1AC[(file1,file2)]
                ovACC1[i] += n.Case1ACC[(file1,file2)]
                ovCC1[i] += n.Case1CC[(file1,file2)]

                ovAC2[i] += n.Case2AC[(file1,file2)]
                ovACC2[i] += n.Case2ACC[(file1,file2)]
                ovCC2[i] += n.Case2CC[(file1,file2)]
                
                ovAC3[i] += n.Case3AC[(file1,file2)]
                ovACC3[i] += n.Case3ACC[(file1,file2)]
                ovCC3[i] += n.Case3CC[(file1,file2)]
    
            
    
    AC_C1 = []
    AC_C2 = []
    AC_C3 = []
    
    CC_C1 = []
    CC_C2 = []
    CC_C3 = []
    
    ACC_C1 = []
    ACC_C2 = []
    ACC_C3 = []
        
    for i in range(0,linesN):
        AC_C1.append(ovAC1[i]/fileV[i])
        AC_C2.append(ovAC2[i]/fileV[i])
        AC_C3.append(ovAC3[i]/fileV[i])
        
        CC_C1.append(ovCC1[i]/fileV[i])
        CC_C2.append(ovCC2[i]/fileV[i])
        CC_C3.append(ovCC3[i]/fileV[i])
        
        ACC_C1.append(ovACC1[i]/fileV[i])
        ACC_C2.append(ovACC2[i]/fileV[i])
        ACC_C3.append(ovACC3[i]/fileV[i])
    plt.rcParams.update({'axes.facecolor':'white'})
    bar_plotAC = pd.DataFrame({'Case 1':  AC_C1,
      'Case 2':  AC_C2,
      'Case 3':  AC_C3},
      index =filesOrder)
    bar_plotAC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],figsize=(30,10),legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('PLD')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/BTC_overlapAC_Cases.pdf",dpi=300, bbox_inches = "tight")    
    
    
    bar_plotCC = pd.DataFrame({'Case 1':  CC_C1,
      'Case 2':  CC_C2,
      'Case 3':  CC_C3},
      index =filesOrder)
    bar_plotCC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],figsize=(30,10),legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('PLD')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/BTC_overlapCC_Cases.pdf",dpi=300, bbox_inches = "tight")       
    
    bar_plotACC = pd.DataFrame({'Case 1':  ACC_C1,
      'Case 2':  ACC_C2,
      'Case 3':  ACC_C3},
      index =filesOrder)
    bar_plotACC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],figsize=(30,10),legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('PLD')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/BTC_overlapACC_Cases.pdf",dpi=300, bbox_inches = "tight")      
    
    labels = ["Case 1","Case 2","Case 3"]
    ac_case1 = 0
    ac_case2 = 0
    ac_case3 = 0
    for i in AC_C1:
         ac_case1 += i
    for i in AC_C2:
         ac_case2 += i
    for i in AC_C3:
         ac_case3 += i
    
    cc_case1 = 0
    cc_case2 = 0
    cc_case3 = 0
    for i in CC_C1:
         cc_case1 += i
    for i in CC_C2:
         cc_case2 += i
    for i in CC_C3:
         cc_case3 += i
            
    acc_case1 = 0
    acc_case2 = 0
    acc_case3 = 0
    for i in ACC_C1:
         acc_case1 += i
    for i in ACC_C2:
         acc_case2 += i
    for i in ACC_C3:
         acc_case3 += i
            
    ac_cases = [ac_case1,ac_case2,ac_case3]
    cc_cases = [cc_case1,cc_case2,cc_case3]
    acc_cases = [acc_case1,acc_case2,acc_case3]
    plt.clf()
    fig, ax = plt.subplots()
    ax.pie(ac_cases, labels=labels,  colors = ['Blue', 'grey', 'red'],autopct='%.2f%%',
       pctdistance=1.25, labeldistance=.6)
    plt.savefig("analysis/BTC_overlapAC_AllCases.pdf")          
    plt.clf()
    fig, ax = plt.subplots()
    ax.pie(cc_cases, labels=labels,  colors = ['Blue', 'grey', 'red'],autopct='%.2f%%',
       pctdistance=1.25, labeldistance=.6)
    plt.savefig("analysis/BTC_overlapCC_AllCases.pdf")    
    plt.clf()
    fig, ax = plt.subplots()
    ax.pie(acc_cases, labels=labels, colors = ['Blue', 'grey', 'red'], autopct='%.2f%%',
       pctdistance=1.25, labeldistance=.6)
    plt.savefig("analysis/BTC_overlapACC_AllCases.pdf")   
 
def drawBTC2():
    n = ove.overlaps()
    n.load("analysis/BTCTest2")
    
    f1 = open("files.txt","r")
    lineR = f1.read()
    linesNQ = lineR.replace(".nq","").split("\n")
    lines = lineR.replace(".nq","").replace("_00001","").split("\n")
    linesN = len(lines)
    f1.close()
    
    fileL1 = []
    fileL2 = []
    vL = []
    eL = []
    acL = []
    accL = []
    ccL = []
    pL = []
    

    filesOrder = []
    for i in range(0,linesN):
        fileNQ1 = linesNQ[i]
        file1 = lines[i]
        filesOrder.append(lines[i])
        for j in range(0,linesN):
            fileNQ2 = linesNQ[j]
            file2 = lines[j]
            fileL1.append(file1)
            fileL2.append(file2)


            vL.append(n.ovVertices[(fileNQ1,fileNQ2)]/n.ovVertices[(fileNQ1,fileNQ1)] )
            acL.append(n.ovAC[(fileNQ1,fileNQ2)]/n.ovAC[(fileNQ1,fileNQ1)]  )
            accL.append(n.ovACC[(fileNQ1,fileNQ2)]/n.ovACC[(fileNQ1,fileNQ1)] )
            ccL.append(n.ovCC[(fileNQ1,fileNQ2)]/n.ovCC[(fileNQ1,fileNQ1)] )
            pL.append(n.ovPredicates[(fileNQ1,fileNQ2)]/n.ovPredicates[(fileNQ1,fileNQ1)] )

                

    
    dv = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the vertices': vL})
    dvs = dv.pivot(index="File1", columns="File2", values="Overlap of the vertices")
    dvs = dvs.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(90, 60))
    cmap = mpl.colormaps.get_cmap("Blues")
    cmap.set_bad("white")
    sns.heatmap(dvs , annot=False, fmt="d", linewidths=.5, ax=ax,norm=LogNorm(), cmap=cmap)
    plt.xlabel("PLD")
    plt.ylabel("PLD")
    plt.savefig("analysis/BTC_overlapV.pdf")
    
    
    dac = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the ACs': acL})
    dacs = dac.pivot(index="File1", columns="File2", values="Overlap of the ACs")
    dacs = dacs.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(90, 60))
    sns.heatmap(dacs , annot=False, fmt="d", linewidths=.5, ax=ax,norm=LogNorm(), cmap=cmap,lw=0)
    plt.xlabel("PLD")
    plt.ylabel("PLD")
    plt.savefig("analysis/BTC_overlapAC.pdf")
   
    dacc = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the ACCs': accL})
    daccs = dacc.pivot(index="File1", columns="File2", values="Overlap of the ACCs")
    daccs = daccs.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(90, 60))
    #sns.heatmap(daccs , annot=True, fmt="d", linewidths=.5, ax=ax,mask=(daccs==0))
    sns.heatmap(daccs , annot=False, fmt="d", linewidths=.5, ax=ax,norm=LogNorm(), cmap=cmap,lw=0)
    plt.xlabel("PLD")
    plt.ylabel("PLD")
    plt.savefig("analysis/BTC_overlapACC.pdf")
    dcc = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the CCs': ccL})
    dccs = dcc.pivot(index="File1", columns="File2", values="Overlap of the CCs")
    dccs = dccs.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(90, 60))
    sns.heatmap(dccs , annot=False, fmt="d", linewidths=.5, ax=ax,norm=LogNorm(), cmap=cmap,lw=0)
    plt.xlabel("PLD")
    plt.ylabel("PLD")
    plt.savefig("analysis/BTC_overlapCC.pdf")
    
    
    dp = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the Predicates': pL})
    dps = dp.pivot(index="File1", columns="File2", values="Overlap of the Predicates")
    dps = dps.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(90, 60))
    sns.heatmap(dps , annot=False, fmt="d", linewidths=.5, ax=ax,norm=LogNorm(), cmap=cmap,lw=0)
    plt.xlabel("PLD")
    plt.ylabel("PLD")
    plt.savefig("analysis/BTC_overlapPredicates.pdf")
    
    
    
def drawNews():
    newsL = ["Al-Jazeera","CNN","euronews"]
    topics = ["CERN",        "Facebook",   "NFL",          "Obesity",              "Twitter",  "Cigarettes",   "FIFA",       "Nintendo",     "StanfordUniversity",   "WarnerBros",  "Disney",       "NBA",        "NobelPrize",   "TikTok", "WorldHealthOrganization"]
    n = ove.overlaps()
    n.load("analysis/newsTest")
    
    ovAC1 ={}
    ovACC1 ={}
    ovCC1 ={}
    
    ovAC2 ={}
    ovACC2 ={}
    ovCC2 ={}
    
    ovAC3 ={}
    ovACC3 ={}
    ovCC3 ={}  
    fileV = {}
    for i in range(0,3):
        ovAC1[i] = 0
        ovACC1[i] = 0
        ovCC1[i] = 0
        
        ovAC2[i] = 0
        ovACC2[i] = 0
        ovCC2[i] = 0
        
        ovAC3[i] = 0
        ovACC3[i] = 0
        ovCC3[i] = 0
        
        fileV[i] = 0
    filesOrder = []

    i = 0
    for n1 in newsL:
        filesOrder.append(n1)
        for t1 in topics:
            file1 = t1+"-"+n1     
            for n2 in newsL:               
                file2 = t1+"-"+n2
                if n2 != n1:
                    fileV[i] += n.ovVertices[(file1,file1)]
                    ovAC1[i] += n.Case1AC[(file1,file2)]
                    ovACC1[i] += n.Case1ACC[(file1,file2)]
                    ovCC1[i] += n.Case1CC[(file1,file2)]

                    ovAC2[i] += n.Case2AC[(file1,file2)]
                    ovACC2[i] += n.Case2ACC[(file1,file2)]
                    ovCC2[i] += n.Case2CC[(file1,file2)]

                    ovAC3[i] += n.Case3AC[(file1,file2)]
                    ovACC3[i] += n.Case3ACC[(file1,file2)]
                    ovCC3[i] += n.Case3CC[(file1,file2)]
        i += 1

            
    
    AC_C1 = []
    AC_C2 = []
    AC_C3 = []
    
    CC_C1 = []
    CC_C2 = []
    CC_C3 = []
    
    ACC_C1 = []
    ACC_C2 = []
    ACC_C3 = []
        
    for i in range(0,3):
        AC_C1.append(ovAC1[i]/fileV[i]*100)
        AC_C2.append(ovAC2[i]/fileV[i]*100)
        AC_C3.append(ovAC3[i]/fileV[i]*100)
        
        CC_C1.append(ovCC1[i]/fileV[i]*100)
        CC_C2.append(ovCC2[i]/fileV[i]*100)
        CC_C3.append(ovCC3[i]/fileV[i]*100)
        
        ACC_C1.append(ovACC1[i]/fileV[i]*100)
        ACC_C2.append(ovACC2[i]/fileV[i]*100)
        ACC_C3.append(ovACC3[i]/fileV[i]*100)

    plt.rcParams.update({'axes.facecolor':'white'})
    bar_plotAC = pd.DataFrame({'Case 1':  AC_C1,
      'Case 2':  AC_C2,
      'Case 3':  AC_C3},
      index =filesOrder)
    bar_plotAC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('Broadcaster')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/News_overlapAC_Cases.pdf",dpi=300, bbox_inches = "tight")       
    
    bar_plotCC = pd.DataFrame({'Case 1':  CC_C1,
      'Case 2':  CC_C2,
      'Case 3':  CC_C3},
      index =filesOrder)
    bar_plotCC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('Broadcaster')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/News_overlapCC_Cases.pdf",dpi=300, bbox_inches = "tight")       
    
    bar_plotACC = pd.DataFrame({'Case 1':  ACC_C1,
      'Case 2':  ACC_C2,
      'Case 3':  ACC_C3},
      index =filesOrder)
    bar_plotACC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('Broadcaster')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/News_overlapACC_Cases.pdf",dpi=300, bbox_inches = "tight")       
    
    labels = ["Case 1","Case 2","Case 3"]
    ac_case1 = 0
    ac_case2 = 0
    ac_case3 = 0
    for i in AC_C1:
         ac_case1 += i
    for i in AC_C2:
         ac_case2 += i
    for i in AC_C3:
         ac_case3 += i
    
    cc_case1 = 0
    cc_case2 = 0
    cc_case3 = 0
    for i in CC_C1:
         cc_case1 += i
    for i in CC_C2:
         cc_case2 += i
    for i in CC_C3:
         cc_case3 += i
            
    acc_case1 = 0
    acc_case2 = 0
    acc_case3 = 0
    for i in ACC_C1:
         acc_case1 += i
    for i in ACC_C2:
         acc_case2 += i
    for i in ACC_C3:
         acc_case3 += i
            
    ac_cases = [ac_case1,ac_case2,ac_case3]
    cc_cases = [cc_case1,cc_case2,cc_case3]
    acc_cases = [acc_case1,acc_case2,acc_case3]
    plt.clf()
    fig, ax = plt.subplots()
    ax.pie(ac_cases, labels=labels,  colors = ['Blue', 'grey', 'red'],autopct='%.2f%%',
       pctdistance=1.25, labeldistance=.6)
    plt.savefig("analysis/News_overlapAC_AllCases.pdf")          
    plt.clf()
    fig, ax = plt.subplots()
    ax.pie(cc_cases, labels=labels,  colors = ['Blue', 'grey', 'red'],autopct='%.2f%%',
       pctdistance=1.25, labeldistance=.6)
    plt.savefig("analysis/News_overlapCC_AllCases.pdf")    
    plt.clf()
    fig, ax = plt.subplots()
    ax.pie(acc_cases, labels=labels, colors = ['Blue', 'grey', 'red'], autopct='%.2f%%',
       pctdistance=1.25, labeldistance=.6)
    plt.savefig("analysis/News_overlapACC_AllCases.pdf")   

def drawNews2():
    newsL = ["Al-Jazeera","CNN","euronews"]
    topics = ["CERN",        "Facebook",   "NFL",          "Obesity",              "Twitter",  "Cigarettes",   "FIFA",       "Nintendo",     "StanfordUniversity",   "WarnerBros",  "Disney",       "NBA",        "NobelPrize",   "TikTok", "WorldHealthOrganization"]
    n = ove.overlaps()
    n.load("analysis/newsTest")
    
    fileL1 = []
    fileL2 = []
    vL = []
    eL = []
    acL = []
    accL = []
    ccL = []
    pL = []
    
    ovV ={}
    ovAC ={}
    ovACC ={}
    ovCC ={}
    ovP ={}
    filesOrder = []
    
    for n1 in newsL:
        for n2 in newsL:
            ovV[(n1,n2)] = 0
            ovAC[(n1,n2)] = 0
            ovACC[(n1,n2)] = 0
            ovCC[(n1,n2)] = 0
            ovP[(n1,n2)] = 0
    
    for n1 in newsL:
        filesOrder.append(n1)
        for t1 in topics:
            file1 = t1+"-"+n1     
            for n2 in newsL:               
                file2 = t1+"-"+n2
                ovV[(n1,n2)] += n.ovVertices[(file1,file2)]
                ovAC[(n1,n2)] += n.ovAC[(file1,file2)]
                ovACC[(n1,n2)] += n.ovACC[(file1,file2)]
                ovCC[(n1,n2)] += n.ovCC[(file1,file2)]
                ovP[(n1,n2)] += n.ovPredicates[(file1,file2)]
    for n1 in newsL:   
        for n2 in newsL:               
            fileL1.append(n1)
            fileL2.append(n2)


            vL.append(ovV[(n1,n2)]/ovV[(n1,n1)])
            acL.append(ovAC[(n1,n2)]/ovAC[(n1,n1)] )
            accL.append(ovACC[(n1,n2)]/ovACC[(n1,n1)] )
            ccL.append(ovCC[(n1,n2)]/ovCC[(n1,n1)])
            pL.append(ovP[(n1,n2)] /ovP[(n1,n1)])
    
    
    
                

    
    dv = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the vertices': vL})
    dvs = dv.pivot(index="File1", columns="File2", values="Overlap of the vertices")
    dvs = dvs.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 6))
    cmap = mpl.colormaps.get_cmap("Blues")
    cmap.set_bad("white")
    sns.heatmap(dvs , annot=False, fmt="d", linewidths=.5, ax=ax, cmap=cmap)
    plt.xlabel("Broadcaster")
    plt.ylabel("Broadcaster")
    plt.savefig("analysis/News_overlapV.pdf")
    
    
    dac = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the ACs': acL})
    dacs = dac.pivot(index="File1", columns="File2", values="Overlap of the ACs")
    dacs = dacs.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(dacs , annot=False, fmt="d", linewidths=.5, ax=ax, cmap=cmap,lw=0)
    plt.xlabel("Broadcaster")
    plt.ylabel("Broadcaster")
    plt.savefig("analysis/News_overlapAC.pdf")
   
    dacc = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the ACCs': accL})
    daccs = dacc.pivot(index="File1", columns="File2", values="Overlap of the ACCs")
    daccs = daccs.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 6))
    #sns.heatmap(daccs , annot=True, fmt="d", linewidths=.5, ax=ax,mask=(daccs==0))
    sns.heatmap(daccs , annot=False, fmt="d", linewidths=.5, ax=ax, cmap=cmap,lw=0)
    plt.xlabel("Broadcaster")
    plt.ylabel("Broadcaster")
    plt.savefig("analysis/News_overlapACC.pdf")
    dcc = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the CCs': ccL})
    dccs = dcc.pivot(index="File1", columns="File2", values="Overlap of the CCs")
    dccs = dccs.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(dccs , annot=False, fmt="d", linewidths=.5, ax=ax, cmap=cmap,lw=0)
    plt.xlabel("Broadcaster")
    plt.ylabel("Broadcaster")
    plt.savefig("analysis/News_overlapCC.pdf")
    
    
    dp = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the Predicates': pL})
    dps = dp.pivot(index="File1", columns="File2", values="Overlap of the Predicates")
    dps = dps.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(dps , annot=False, fmt="d", linewidths=.5, ax=ax, cmap=cmap,lw=0)
    plt.xlabel("Broadcaster")
    plt.ylabel("Broadcaster")
    plt.savefig("analysis/News_overlapPredicates.pdf")
    
def drawNews3():
    newsL = ["Al-Jazeera","CNN","euronews"]
    topics = ["CERN",        "Facebook",   "NFL",          "Obesity",              "Twitter",  "Cigarettes",   "FIFA",       "Nintendo",     "StanfordUniversity",   "WarnerBros",  "Disney",       "NBA",        "NobelPrize",   "TikTok", "WorldHealthOrganization"]
    n = ove.overlaps()
    n.load("analysis/newsTest")
    
    ovAC1 ={}
    ovACC1 ={}
    ovCC1 ={}
    
    ovAC2 ={}
    ovACC2 ={}
    ovCC2 ={}
    
    ovAC3 ={}
    ovACC3 ={}
    ovCC3 ={}  
    fileV = {}
    for i in range(0,6):
        ovAC1[i] = 0
        ovACC1[i] = 0
        ovCC1[i] = 0
        
        ovAC2[i] = 0
        ovACC2[i] = 0
        ovCC2[i] = 0
        
        ovAC3[i] = 0
        ovACC3[i] = 0
        ovCC3[i] = 0
        
        fileV[i] = 0
    filesOrder = []

    i = -1
    for n1 in newsL:
        
        for n2 in newsL: 
            if n2 != n1:
                i += 1
                filesOrder.append(n1+" and "+n2)
                for t1 in topics:
                    file1 = t1+"-"+n1     

                    file2 = t1+"-"+n2

                    fileV[i] += n.ovVertices[(file1,file1)]
                    ovAC1[i] += n.Case1AC[(file1,file2)]
                    ovACC1[i] += n.Case1ACC[(file1,file2)]
                    ovCC1[i] += n.Case1CC[(file1,file2)]

                    ovAC2[i] += n.Case2AC[(file1,file2)]
                    ovACC2[i] += n.Case2ACC[(file1,file2)]
                    ovCC2[i] += n.Case2CC[(file1,file2)]

                    ovAC3[i] += n.Case3AC[(file1,file2)]
                    ovACC3[i] += n.Case3ACC[(file1,file2)]
                    ovCC3[i] += n.Case3CC[(file1,file2)]
        

            
    
    AC_C1 = []
    AC_C2 = []
    AC_C3 = []
    
    CC_C1 = []
    CC_C2 = []
    CC_C3 = []
    
    ACC_C1 = []
    ACC_C2 = []
    ACC_C3 = []
        
    for i in range(0,6):
        AC_C1.append(ovAC1[i]/fileV[i]*100)
        AC_C2.append(ovAC2[i]/fileV[i]*100)
        AC_C3.append(ovAC3[i]/fileV[i]*100)
        
        CC_C1.append(ovCC1[i]/fileV[i]*100)
        CC_C2.append(ovCC2[i]/fileV[i]*100)
        CC_C3.append(ovCC3[i]/fileV[i]*100)
        
        ACC_C1.append(ovACC1[i]/fileV[i]*100)
        ACC_C2.append(ovACC2[i]/fileV[i]*100)
        ACC_C3.append(ovACC3[i]/fileV[i]*100)

    plt.rcParams.update({'axes.facecolor':'white'})
    bar_plotAC = pd.DataFrame({'Case 1':  AC_C1,
      'Case 2':  AC_C2,
      'Case 3':  AC_C3},
      index =filesOrder)
    bar_plotAC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('Pair')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/News_Pair_overlapAC_Cases.pdf",dpi=300, bbox_inches = "tight")     
    
    bar_plotCC = pd.DataFrame({'Case 1':  CC_C1,
      'Case 2':  CC_C2,
      'Case 3':  CC_C3},
      index =filesOrder)
    bar_plotCC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('Pair')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/News_Pair_overlapCC_Cases.pdf",dpi=300, bbox_inches = "tight")    
    
    bar_plotACC = pd.DataFrame({'Case 1':  ACC_C1,
      'Case 2':  ACC_C2,
      'Case 3':  ACC_C3},
      index =filesOrder)
    bar_plotACC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('Pair')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/News_Pair_overlapACC_Cases.pdf",dpi=300, bbox_inches = "tight") 
    
def drawCode():
    viewL = ["NormalizedAST","CFG","DFG"]
    n = ove.overlaps()
    n.load("analysis/CodeTest")
    fr = open("rfiles.txt")
    files = fr.read()
    files = files.replace(".R\n","\n")
    files = files.split("\n")
    files = files[:-1]
    fr.close()
    ovAC1 ={}
    ovACC1 ={}
    ovCC1 ={}
    
    ovAC2 ={}
    ovACC2 ={}
    ovCC2 ={}
    
    ovAC3 ={}
    ovACC3 ={}
    ovCC3 ={}  
    fileV = {}
    for i in range(0,3):
        ovAC1[i] = 0
        ovACC1[i] = 0
        ovCC1[i] = 0
        
        ovAC2[i] = 0
        ovACC2[i] = 0
        ovCC2[i] = 0
        
        ovAC3[i] = 0
        ovACC3[i] = 0
        ovCC3[i] = 0
        
        fileV[i] = 0
    filesOrder = []

    i = 0
    for n1 in viewL:
        filesOrder.append(n1)
        for t1 in files:
            if n1 == "NormalizedAST":
                file1 = t1+"-.normalize"
            elif n1 == "CFG":
                file1 = t1+"-.cfg"
            elif n1 == "DFG":
                file1 = t1+"-.dfg"

            for n2 in viewL: 
                file2 = ""
                if n2 == "NormalizedAST":
                    file2 = t1+"-.normalize"
                elif n2 == "CFG":
                    file2 = t1+"-.cfg"
                elif n2 == "DFG":
                    file2 = t1+"-.dfg"
                    

                if n2 != n1:
                    fileV[i] += n.ovVertices[(file1,file1)]
                    ovAC1[i] += n.Case1AC[(file1,file2)]
                    ovACC1[i] += n.Case1ACC[(file1,file2)]
                    ovCC1[i] += n.Case1CC[(file1,file2)]

                    ovAC2[i] += n.Case2AC[(file1,file2)]
                    ovACC2[i] += n.Case2ACC[(file1,file2)]
                    ovCC2[i] += n.Case2CC[(file1,file2)]

                    ovAC3[i] += n.Case3AC[(file1,file2)]
                    ovACC3[i] += n.Case3ACC[(file1,file2)]
                    ovCC3[i] += n.Case3CC[(file1,file2)]
        i += 1

            
    
    AC_C1 = []
    AC_C2 = []
    AC_C3 = []
    
    CC_C1 = []
    CC_C2 = []
    CC_C3 = []
    
    ACC_C1 = []
    ACC_C2 = []
    ACC_C3 = []
        
    for i in range(0,3):
        AC_C1.append(ovAC1[i]/fileV[i]*100)
        AC_C2.append(ovAC2[i]/fileV[i]*100)
        AC_C3.append(ovAC3[i]/fileV[i]*100)
        
        CC_C1.append(ovCC1[i]/fileV[i]*100)
        CC_C2.append(ovCC2[i]/fileV[i]*100)
        CC_C3.append(ovCC3[i]/fileV[i]*100)
        
        ACC_C1.append(ovACC1[i]/fileV[i]*100)
        ACC_C2.append(ovACC2[i]/fileV[i]*100)
        ACC_C3.append(ovACC3[i]/fileV[i]*100)

    plt.rcParams.update({'axes.facecolor':'white'})
    bar_plotAC = pd.DataFrame({'Case 1':  AC_C1,
      'Case 2':  AC_C2,
      'Case 3':  AC_C3},
      index =filesOrder)
    bar_plotAC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('View')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/Code_overlapAC_Cases.pdf",dpi=300, bbox_inches = "tight")   
    
    bar_plotCC = pd.DataFrame({'Case 1':  CC_C1,
      'Case 2':  CC_C2,
      'Case 3':  CC_C3},
      index =filesOrder)
    bar_plotCC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('View')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/Code_overlapCC_Cases.pdf",dpi=300, bbox_inches = "tight")    
    
    bar_plotACC = pd.DataFrame({'Case 1':  ACC_C1,
      'Case 2':  ACC_C2,
      'Case 3':  ACC_C3},
      index =filesOrder)
    bar_plotACC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('View')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/Code_overlapACC_Cases.pdf",dpi=300, bbox_inches = "tight")    
    
    labels = ["Case 1","Case 2","Case 3"]
    ac_case1 = 0
    ac_case2 = 0
    ac_case3 = 0
    for i in AC_C1:
         ac_case1 += i
    for i in AC_C2:
         ac_case2 += i
    for i in AC_C3:
         ac_case3 += i
    
    cc_case1 = 0
    cc_case2 = 0
    cc_case3 = 0
    for i in CC_C1:
         cc_case1 += i
    for i in CC_C2:
         cc_case2 += i
    for i in CC_C3:
         cc_case3 += i
            
    acc_case1 = 0
    acc_case2 = 0
    acc_case3 = 0
    for i in ACC_C1:
         acc_case1 += i
    for i in ACC_C2:
         acc_case2 += i
    for i in ACC_C3:
         acc_case3 += i
            
    ac_cases = [ac_case1,ac_case2,ac_case3]
    cc_cases = [cc_case1,cc_case2,cc_case3]
    acc_cases = [acc_case1,acc_case2,acc_case3]
    plt.clf()
    fig, ax = plt.subplots()
    ax.pie(ac_cases, labels=labels,  colors = ['Blue', 'grey', 'red'],autopct='%.2f%%',
       pctdistance=1.25, labeldistance=.6)
    plt.savefig("analysis/Code_overlapAC_AllCases.pdf")          
    plt.clf()
    fig, ax = plt.subplots()
    ax.pie(cc_cases, labels=labels,  colors = ['Blue', 'grey', 'red'],autopct='%.2f%%',
       pctdistance=1.25, labeldistance=.6)
    plt.savefig("analysis/Code_overlapCC_AllCases.pdf")    
    plt.clf()
    fig, ax = plt.subplots()
    ax.pie(acc_cases, labels=labels, colors = ['Blue', 'grey', 'red'], autopct='%.2f%%',
       pctdistance=1.25, labeldistance=.6)
    plt.savefig("analysis/Code_overlapACC_AllCases.pdf")   

def drawCode2():
    viewL = ["NormalizedAST","CFG","DFG"]
    n = ove.overlaps()
    n.load("analysis/CodeTest")
    fr = open("rfiles.txt")
    files = fr.read()
    files = files.replace(".R\n","\n")
    files = files.split("\n")
    files = files[:-1]
    fr.close()
    
    fileL1 = []
    fileL2 = []
    vL = []
    eL = []
    acL = []
    accL = []
    ccL = []
    pL = []
    
    ovV ={}
    ovAC ={}
    ovACC ={}
    ovCC ={}
    ovP ={}
    filesOrder = []
    
    for n1 in viewL :
        for n2 in viewL:
            ovV[(n1,n2)] = 0
            ovAC[(n1,n2)] = 0
            ovACC[(n1,n2)] = 0
            ovCC[(n1,n2)] = 0
            ovP[(n1,n2)] = 0
    for n1 in viewL:
        filesOrder.append(n1)
        for t1 in files:
            if n1 == "NormalizedAST":
                file1 = t1+"-.normalize"
            elif n1 == "CFG":
                file1 = t1+"-.cfg"
            elif n1 == "DFG":
                file1 = t1+"-.dfg"

            for n2 in viewL: 
                file2 = ""
                if n2 == "NormalizedAST":
                    file2 = t1+"-.normalize"
                elif n2 == "CFG":
                    file2 = t1+"-.cfg"
                elif n2 == "DFG":
                    file2 = t1+"-.dfg"

                ovV[(n1,n2)] += n.ovVertices[(file1,file2)]
                ovAC[(n1,n2)] += n.ovAC[(file1,file2)]
                ovACC[(n1,n2)] += n.ovACC[(file1,file2)]
                ovCC[(n1,n2)] += n.ovCC[(file1,file2)]
                ovP[(n1,n2)] += n.ovPredicates[(file1,file2)]

    for n1 in viewL :   
        for n2 in viewL :               
            fileL1.append(n1)
            fileL2.append(n2)


            vL.append(ovV[(n1,n2)]/ovV[(n1,n1)])
            acL.append(ovAC[(n1,n2)]/ovAC[(n1,n1)] )
            accL.append(ovACC[(n1,n2)]/ovACC[(n1,n1)] )
            ccL.append(ovCC[(n1,n2)]/ovCC[(n1,n1)])
            pL.append(ovP[(n1,n2)] /ovP[(n1,n1)])
    
    

                

    
    dv = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the vertices': vL})
    dvs = dv.pivot(index="File1", columns="File2", values="Overlap of the vertices")
    dvs = dvs.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 6))
    cmap = mpl.colormaps.get_cmap("Blues")
    cmap.set_bad("white")
    sns.heatmap(dvs , annot=False, fmt="d", linewidths=.5, ax=ax, cmap=cmap)
    plt.xlabel("View")
    plt.ylabel("View")
    plt.savefig("analysis/Code_overlapV.pdf")
    
    
    dac = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the ACs': acL})
    dacs = dac.pivot(index="File1", columns="File2", values="Overlap of the ACs")
    dacs = dacs.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(dacs , annot=False, fmt="d", linewidths=.5, ax=ax, cmap=cmap,lw=0)
    plt.xlabel("View")
    plt.ylabel("View")
    plt.savefig("analysis/Code_overlapAC.pdf")
   
    dacc = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the ACCs': accL})
    daccs = dacc.pivot(index="File1", columns="File2", values="Overlap of the ACCs")
    daccs = daccs.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 6))
    #sns.heatmap(daccs , annot=True, fmt="d", linewidths=.5, ax=ax,mask=(daccs==0))
    sns.heatmap(daccs , annot=False, fmt="d", linewidths=.5, ax=ax, cmap=cmap,lw=0)
    plt.xlabel("View")
    plt.ylabel("View")
    plt.savefig("analysis/Code_overlapACC.pdf")
    dcc = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the CCs': ccL})
    dccs = dcc.pivot(index="File1", columns="File2", values="Overlap of the CCs")
    dccs = dccs.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(dccs , annot=False, fmt="d", linewidths=.5, ax=ax, cmap=cmap,lw=0)
    plt.xlabel("View")
    plt.ylabel("View")
    plt.savefig("analysis/Code_overlapCC.pdf")
    
    dp = pd.DataFrame({'File1': fileL1,
                   'File2': fileL2,
                   'Overlap of the Predicates': pL})
    dps = dp.pivot(index="File1", columns="File2", values="Overlap of the Predicates")
    dps = dps.reindex(filesOrder, level=0).T.reindex(filesOrder).T
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(dps , annot=False, fmt="d", linewidths=.5, ax=ax, cmap=cmap,lw=0)
    plt.xlabel("View")
    plt.ylabel("View")
    plt.savefig("analysis/Code_overlapPredicates.pdf")
    
def drawCode3():
    viewL = ["NormalizedAST","CFG","DFG"]
    n = ove.overlaps()
    n.load("analysis/CodeTest")
    fr = open("rfiles.txt")
    files = fr.read()
    files = files.replace(".R\n","\n")
    files = files.split("\n")
    files = files[:-1]
    fr.close()
    ovAC1 ={}
    ovACC1 ={}
    ovCC1 ={}
    
    ovAC2 ={}
    ovACC2 ={}
    ovCC2 ={}
    
    ovAC3 ={}
    ovACC3 ={}
    ovCC3 ={}  
    fileV = {}
    for i in range(0,6):
        ovAC1[i] = 0
        ovACC1[i] = 0
        ovCC1[i] = 0
        
        ovAC2[i] = 0
        ovACC2[i] = 0
        ovCC2[i] = 0
        
        ovAC3[i] = 0
        ovACC3[i] = 0
        ovCC3[i] = 0
        
        fileV[i] = 0
    filesOrder = []

    i = -1
    for n1 in viewL:
        for n2 in viewL: 
            if n2 != n1:
                filesOrder.append(n1+" and "+n2)
                i += 1
                for t1 in files:
                    file1 = ""
                    file2 = ""

                    if n1 == "NormalizedAST":
                        file1 = t1+"-.normalize"
                    elif n1 == "CFG":
                        file1 = t1+"-.cfg"
                    elif n1 == "DFG":
                        file1 = t1+"-.dfg"

                    if n2 == "NormalizedAST":
                        file2 = t1+"-.normalize"
                    elif n2 == "CFG":
                        file2 = t1+"-.cfg"
                    elif n2 == "DFG":
                        file2 = t1+"-.dfg"
                
                    fileV[i] += n.ovVertices[(file1,file1)]
                    ovAC1[i] += n.Case1AC[(file1,file2)]
                    ovACC1[i] += n.Case1ACC[(file1,file2)]
                    ovCC1[i] += n.Case1CC[(file1,file2)]

                    ovAC2[i] += n.Case2AC[(file1,file2)]
                    ovACC2[i] += n.Case2ACC[(file1,file2)]
                    ovCC2[i] += n.Case2CC[(file1,file2)]

                    ovAC3[i] += n.Case3AC[(file1,file2)]
                    ovACC3[i] += n.Case3ACC[(file1,file2)]
                    ovCC3[i] += n.Case3CC[(file1,file2)]
      

            
    
    AC_C1 = []
    AC_C2 = []
    AC_C3 = []
    
    CC_C1 = []
    CC_C2 = []
    CC_C3 = []
    
    ACC_C1 = []
    ACC_C2 = []
    ACC_C3 = []
        
    for i in range(0,6):
        AC_C1.append(ovAC1[i]/fileV[i]*100)
        AC_C2.append(ovAC2[i]/fileV[i]*100)
        AC_C3.append(ovAC3[i]/fileV[i]*100)
        
        CC_C1.append(ovCC1[i]/fileV[i]*100)
        CC_C2.append(ovCC2[i]/fileV[i]*100)
        CC_C3.append(ovCC3[i]/fileV[i]*100)
        
        ACC_C1.append(ovACC1[i]/fileV[i]*100)
        ACC_C2.append(ovACC2[i]/fileV[i]*100)
        ACC_C3.append(ovACC3[i]/fileV[i]*100)

    plt.rcParams.update({'axes.facecolor':'white'})
    bar_plotAC = pd.DataFrame({'Case 1':  AC_C1,
      'Case 2':  AC_C2,
      'Case 3':  AC_C3},
      index =filesOrder)
    bar_plotAC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('Pair')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/Code_Pair_overlapAC_Cases.pdf",dpi=300, bbox_inches = "tight")   
    
    bar_plotCC = pd.DataFrame({'Case 1':  CC_C1,
      'Case 2':  CC_C2,
      'Case 3':  CC_C3},
      index =filesOrder)
    bar_plotCC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('Pair')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/Code_Pair_overlapCC_Cases.pdf",dpi=300, bbox_inches = "tight")    
    
    bar_plotACC = pd.DataFrame({'Case 1':  ACC_C1,
      'Case 2':  ACC_C2,
      'Case 3':  ACC_C3},
      index =filesOrder)
    bar_plotACC.plot (kind = 'bar', stacked = True, color = ['Blue', 'grey', 'red'],legend=None)
    plt.xticks(rotation = 45, ha='right')
    plt.xlabel ('Pair')
    plt.ylabel ('Occurrences in %')
    plt.ylim(0, 100)
    plt.savefig("analysis/Code_Pair_overlapACC_Cases.pdf",dpi=300, bbox_inches = "tight")     
    


    
def avgNews():
    newsL = ["Al-Jazeera","CNN","euronews"]
    topics = ["CERN",        "Facebook",   "NFL",          "Obesity",              "Twitter",  "Cigarettes",   "FIFA",       "Nintendo",     "StanfordUniversity",   "WarnerBros",  "Disney",       "NBA",        "NobelPrize",   "TikTok", "WorldHealthOrganization"]
    sourceAC = []
    sourceCC = []
    sourceACC = []

    for topic in topics:
        allACs = set()
        allCCs = set()
        allACCs = set()
        for news in newsL:
            summary1AC = gsg.summaries()
            summary1AC.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"AC")

            summary1CC = gsg.summaries()
            summary1CC.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"CC")

            summary1ACC = gsg.summaries()
            summary1ACC.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"ACC")
            allACs = allACs.union(set(summary1AC.eqcsI.keys()))
            allCCs = allCCs.union(set(summary1CC.eqcsI.keys()))
            allACCs = allACCs.union(set(summary1ACC.eqcsI.keys()))
        sourceAC.append(len(allACs))
        sourceCC.append(len(allCCs))
        sourceACC.append(len(allACCs))
    sumAC = 0
    sumCC = 0
    sumACC = 0
    for i in range(0,len(sourceAC)):
        sumAC += sourceAC[i]
        sumCC += sourceCC[i]
        sumACC += sourceACC[i]
    print("Avg. AC in News ",sumAC/len(sourceAC))
    print("Avg. CC in News ",sumCC/len(sourceCC))
    print("Avg. ACC in News ",sumACC/len(sourceACC))
    
    
def avgCode():
    fr = open("rfiles.txt")
    files = fr.read()
    files = files.replace(".R\n","\n")
    files = files.split("\n")
    files = files[:-1]
    fr.close()
    iC = 0
    allI = len(files)
    
    sourceAC = []
    sourceCC = []
    sourceACC = []

    for file in files:
        iC += 1
        print(str((iC/allI)*100),"%")
        allACs = set()
        allCCs = set()
        allACCs = set()
        for part in [".dfg",".cfg",".normalize"]:          
            summary1AC = gsg.summaries()
            summary1AC.load("../data/"+file+part+"AC")

            summary1CC = gsg.summaries()
            summary1CC.load("../data/"+file+part+"CC")

            summary1ACC = gsg.summaries()
            summary1ACC.load("../data/"+file+part+"ACC")
            allACs = allACs.union(set(summary1AC.eqcsI.keys()))
            allCCs = allCCs.union(set(summary1CC.eqcsI.keys()))
            allACCs = allACCs.union(set(summary1ACC.eqcsI.keys()))
        sourceAC.append(len(allACs))
        sourceCC.append(len(allCCs))
        sourceACC.append(len(allACCs))
    sumAC = 0
    sumCC = 0
    sumACC = 0
    for i in range(0,len(sourceAC)):
        sumAC += sourceAC[i]
        sumCC += sourceCC[i]
        sumACC += sourceACC[i]
    print(len(sourceAC))
    print("Avg. AC in Code ",sumAC/len(sourceAC))
    print("Avg. CC in Code ",sumCC/len(sourceCC))
    print("Avg. ACC in Code ",sumACC/len(sourceACC))
    
    
def drawNews4():
    newsL = ["Al-Jazeera","CNN","euronews"]
    topics = ["CERN",        "Facebook",   "NFL",          "Obesity",              "Twitter",  "Cigarettes",   "FIFA",       "Nintendo",     "StanfordUniversity",   "WarnerBros",  "Disney",       "NBA",        "NobelPrize",   "TikTok", "WorldHealthOrganization"]
    #name2 = topic+"-"+news2
    n = ove.overlaps()
    n.load("analysis/newsTest")
    


    ovAC1 = 0
    ovACC1 = 0
    ovCC1 = 0

    ovAC2 = 0
    ovACC2 = 0
    ovCC2 = 0

    ovAC3 = 0
    ovACC3 = 0
    ovCC3 = 0
        
    fileV = 0
    j = 0
    for n1 in newsL:
        
        for n2 in newsL: 
            if n2 != n1:
                for t1 in topics:
                    file1 = t1+"-"+n1     

                    file2 = t1+"-"+n2
                    
                    if file1 != file2:
                        j += 1
                        fileV = n.ovVertices[(file1,file1)]
                        ovAC1 += n.Case1AC[(file1,file2)]/fileV
                        ovACC1 += n.Case1ACC[(file1,file2)]/fileV
                        ovCC1 += n.Case1CC[(file1,file2)]/fileV

                        ovAC2 += n.Case2AC[(file1,file2)]/fileV
                        ovACC2 += n.Case2ACC[(file1,file2)]/fileV
                        ovCC2 += n.Case2CC[(file1,file2)]/fileV

                        ovAC3 += n.Case3AC[(file1,file2)]/fileV
                        ovACC3 += n.Case3ACC[(file1,file2)]/fileV
                        ovCC3 += n.Case3CC[(file1,file2)]/fileV
    
            
    C1 = []
    C2 = []
    C3 = []
    

    C1.append(ovAC1*100/j)
    C2.append(ovAC2*100/j)
    C3.append(ovAC3*100/j)

    C1.append(ovCC1*100/j)
    C2.append(ovCC2*100/j)
    C3.append(ovCC3*100/j)

    C1.append(ovACC1*100/j)
    C2.append(ovACC2*100/j)
    C3.append(ovACC3*100/j)
    
    print("News")
    print("AC,CC,ACC")
    print("Case 1: ",C1)
    print("Case 2: ",C2)
    print("Case 3: ",C3)
    
    plt.rcParams.update({'axes.facecolor':'white'})   
    plt.rcParams["figure.figsize"] = (6, 5)

    bar_plotAC = pd.DataFrame({'Case 1':  C1,
      'Case 2':  C2,
      'Case 3':  C3},
      index =["AC","CC","ACC"])
    ax = bar_plotAC.plot (kind = 'bar', width = 0.9, color = ['Blue', 'grey', 'red'],legend=None,fontsize = 15)
    plt.xticks(rotation = 0)
    plt.xlabel ('Summary',fontsize = 15)
    plt.ylabel ('Occurrences in %',fontsize = 15)
    plt.ylim(0, 70)
    plt.yticks([0,20,40,60])
    for rect in ax.patches:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2
        space = 1
        label = "{:.2f}".format(y_value)
        ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center', va='bottom')
    plt.savefig("analysis/News_Cases.pdf", bbox_inches = "tight")   

def drawCode4():
    viewL = ["NormalizedAST","CFG","DFG"]
    #.dfg .cfg .normalize
    #name2 = topic+"-"+news2
    n = ove.overlaps()
    n.load("analysis/CodeTest")
    fr = open("rfiles.txt")
    files = fr.read()
    files = files.replace(".R\n","\n")
    files = files.split("\n")
    files = files[:-1]
    fr.close()
    
    ovAC1 = 0
    ovACC1 = 0
    ovCC1 = 0

    ovAC2 = 0
    ovACC2 = 0
    ovCC2 = 0

    ovAC3 = 0
    ovACC3 = 0
    ovCC3 = 0
        
    fileV = 0
    j = 0
    l = 0
    for n1 in viewL:
        for n2 in viewL: 
            if n2 != n1:
                for t1 in files:
                    file1 = ""
                    file2 = ""
                        
                    
                    if n1 == "NormalizedAST":
                        file1 = t1+"-.normalize"
                    elif n1 == "CFG":
                        file1 = t1+"-.cfg"
                    elif n1 == "DFG":
                        file1 = t1+"-.dfg"

                    if n2 == "NormalizedAST":
                        file2 = t1+"-.normalize"
                    elif n2 == "CFG":
                        file2 = t1+"-.cfg"
                    elif n2 == "DFG":
                        file2 = t1+"-.dfg"
                    
                    if file1 != file2:
                        
                        fileV = n.ovVertices[(file1,file1)]
                        if fileV > 0:
                            j += 1
                            ovAC1 += n.Case1AC[(file1,file2)]/fileV
                            ovACC1 += n.Case1ACC[(file1,file2)]/fileV
                            ovCC1 += n.Case1CC[(file1,file2)]/fileV

                            ovAC2 += n.Case2AC[(file1,file2)]/fileV
                            ovACC2 += n.Case2ACC[(file1,file2)]/fileV
                            ovCC2 += n.Case2CC[(file1,file2)]/fileV

                            ovAC3 += n.Case3AC[(file1,file2)]/fileV
                            ovACC3 += n.Case3ACC[(file1,file2)]/fileV
                            ovCC3 += n.Case3CC[(file1,file2)]/fileV
                        else:
                            l += 1
            
    C1 = []
    C2 = []
    C3 = []
    

    C1.append(ovAC1*100/j)
    C2.append(ovAC2*100/j)
    C3.append(ovAC3*100/j)

    C1.append(ovCC1*100/j)
    C2.append(ovCC2*100/j)
    C3.append(ovCC3*100/j)

    C1.append(ovACC1*100/j)
    C2.append(ovACC2*100/j)
    C3.append(ovACC3*100/j)
    print("Code")
    print(j)
    print(l)
    print("AC,CC,ACC")
    print("Case 1: ",C1)
    print("Case 2: ",C2)
    print("Case 3: ",C3)
    
    plt.rcParams.update({'axes.facecolor':'white'})
    plt.rcParams["figure.figsize"] = (6, 5)
    bar_plotAC = pd.DataFrame({'Case 1':  C1,
      'Case 2':  C2,
      'Case 3':  C3},
      index =["AC","CC","ACC"])
    ax = bar_plotAC.plot (kind = 'bar', width = 0.9, color = ['Blue', 'grey', 'red'],legend=None,fontsize = 15)
    plt.xticks(rotation = 0)
    plt.xlabel ('Summary',fontsize = 15)
    plt.ylabel ('Occurrences in %',fontsize = 15)
    plt.ylim(0, 70)
    plt.yticks([0,20,40,60])
    for rect in ax.patches:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2
        space = 1
        label = "{:.2f}".format(y_value)
        ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center', va='bottom')
    plt.savefig("analysis/Code_Cases.pdf", bbox_inches = "tight")     
    
    
def drawBTC4():
    n = ove.overlaps()
    n.load("analysis/BTCTest")
    
    f1 = open("files.txt","r")
    lineR = f1.read()
    linesNQ = lineR.replace(".nq","").split("\n")#[-100:]
    lines = lineR.replace(".nq","").replace("_00001","").split("\n")#[-100:]
    linesN = len(lines)
    f1.close()
    
    ovAC1 = 0
    ovACC1 = 0
    ovCC1 = 0

    ovAC2 = 0
    ovACC2 = 0
    ovCC2 = 0

    ovAC3 = 0
    ovACC3 = 0
    ovCC3 = 0
        
    fileV = 0
    k = 0
    for i in range(0,linesN):
        file1 = linesNQ[i]
        fileV += n.ovVertices[(file1,file1)]
        for j in range(0,linesN):
            file2 = linesNQ[j]
            if file1 != file2:
                k += 1
                fileV = n.ovVertices[(file1,file1)]
                ovAC1 += n.Case1AC[(file1,file2)]/fileV
                ovACC1 += n.Case1ACC[(file1,file2)]/fileV
                ovCC1 += n.Case1CC[(file1,file2)]/fileV

                ovAC2 += n.Case2AC[(file1,file2)]/fileV
                ovACC2 += n.Case2ACC[(file1,file2)]/fileV
                ovCC2 += n.Case2CC[(file1,file2)]/fileV

                ovAC3 += n.Case3AC[(file1,file2)]/fileV
                ovACC3 += n.Case3ACC[(file1,file2)]/fileV
                ovCC3 += n.Case3CC[(file1,file2)]/fileV

            
    C1 = []
    C2 = []
    C3 = []
    

    C1.append(ovAC1*100/k)
    C2.append(ovAC2*100/k)
    C3.append(ovAC3*100/k)

    C1.append(ovCC1*100/k)
    C2.append(ovCC2*100/k)
    C3.append(ovCC3*100/k)

    C1.append(ovACC1*100/k)
    C2.append(ovACC2*100/k)
    C3.append(ovACC3*100/k)
    print("BTC2019")
    print("AC,CC,ACC")
    print("Case 1: ",C1)
    print("Case 2: ",C2)
    print("Case 3: ",C3)
    
    plt.rcParams.update({'axes.facecolor':'white'})
    plt.rcParams["figure.figsize"] = (6, 4)
    bar_plotAC = pd.DataFrame({'Case 1':  C1,
      'Case 2':  C2,
      'Case 3':  C3},
      index =["AC","CC","ACC"])
    ax = bar_plotAC.plot (kind = 'bar', width = 1, color = ['Blue', 'grey', 'red'],legend=None,fontsize = 15)
    plt.xticks(rotation = 0)
    plt.xlabel ('Summary',fontsize = 15)
    plt.ylabel ('Occurrences in %',fontsize = 15)
    plt.ylim(0, 70)
    plt.yticks([0,20,40,60])
    for rect in ax.patches:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2
        space = 1
        label = "{:.2f}".format(y_value)
        ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center', va='bottom')    
    plt.savefig("analysis/BTC_Cases.pdf", bbox_inches = "tight")     
    
    
def main():

    #News-Knowledge-Graphs
    n = ove.overlaps()
    n.analyzeNews()
    n.save("analysis/newsTest")
    drawNews()
    drawNews2() 
    drawNews3()
    drawNews4()
    avgNews()
    show("analysis/newsTest",2)
    
    #BTC2019
    n = ove.overlaps()
    n.analyzeBTC()
    n.save("analysis/BTCTest")
    drawBTC() 
    drawBTC2() 
    #no drawBTC3()
    drawBTC4()
    show("analysis/BTCTest",100)
    
    #Source Code Graphs
    for part in range(14):
        n = ove.overlapsCode()
        n.analyzeCode(part)
        n.save("analysis/CodeTest"+str(part))
    codeAll()
    drawCode()
    drawCode2()
    drawCode3()
    drawCode4( ) 
    avgCode()
    show("analysis/CodeTest",2)
    

    
if __name__ == "__main__":
    main()
