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
from timeit import default_timer as timer
import time
#disable randomization of hash
import os
import sys


def news_summary():
    newsL = ["Al-Jazeera","CNN","euronews"]
    topics = ["CERN",        "Facebook",   "NFL",          "Obesity",              "Twitter",  "Cigarettes",   "FIFA",       "Nintendo",     "StanfordUniversity",   "WarnerBros",  "Disney",       "NBA",        "NobelPrize",   "TikTok", "WorldHealthOrganization"]

    for topic in topics:
        for news in newsL:
            print(topic+"-"+news+".nq")

            summary1AC = gsg.summaries()
            summary1AC.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"AC")            
            summary1AC_Set = gsg.summarySet()
            summary1AC_Set.get_summary(summary1AC)
            summary1AC_Set.save("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"AC_Set")
            summary1AC_Set.to_triples("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"AC")
   
            summary1CC = gsg.summaries()
            summary1CC.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"CC")
            summary1CC_Set = gsg.summarySet()
            summary1CC_Set.get_summary(summary1CC)
            summary1CC_Set.save("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"CC_Set")
            summary1CC_Set.to_triples("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"CC")
            
            summary1ACC = gsg.summaries()
            summary1ACC.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"ACC")
            summary1ACC_Set = gsg.summarySet()
            summary1ACC_Set.get_summary(summary1ACC)
            summary1ACC_Set.save("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"ACC_Set")
            summary1ACC_Set.to_triples("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"ACC")
            
def code_summary():        
        fr = open("Files/rfiles.txt")
        print("rfiles.txt")
        files = fr.read()
        files = files.replace(".R\n","\n")
        files = files.split("\n")
        fr.close()
        iC = 0
        files = files[:-1]
        allI = len(files)
        
        for file in files:
            iC += 1
            if iC% 10000 == 0:
                print(str((iC/allI)*100),"%")
            for part in [".dfg",".cfg",".normalize"]:
                summary1AC = gsg.summaries()
                summary1AC.load("../data/"+file+part+"AC")
                summary1AC_Set = gsg.summarySet()
                summary1AC_Set.get_summary(summary1AC)
                summary1AC_Set.save("../data/"+file+part+"AC_Set")
                summary1AC_Set.to_triples("../data/"+file+part+"AC")

                summary1CC = gsg.summaries()
                summary1CC.load("../data/"+file+part+"CC")
                summary1CC_Set = gsg.summarySet()
                summary1CC_Set.get_summary(summary1CC)
                summary1CC_Set.save("../data/"+file+part+"CC_Set")
                summary1CC_Set.to_triples("../data/"+file+part+"CC")

                summary1ACC = gsg.summaries()
                summary1ACC.load("../data/"+file+part+"ACC")
                summary1ACC_Set = gsg.summarySet()
                summary1ACC_Set.get_summary(summary1ACC)
                summary1ACC_Set.save("../data/"+file+part+"ACC_Set")
                summary1ACC_Set.to_triples("../data/"+file+part+"ACC")

def BTC_summary():
        
        fr = open("Files/files.txt")
        files = fr.read()
        files = files.replace(".nq",".nq.gz")
        files = files.split("\n")
       
        summaryAll_AC_Set = gsg.summarySet()
        summaryAll_CC_Set = gsg.summarySet()
        summaryAll_ACC_Set = gsg.summarySet()
        
        summary_AC_Sets= {}
        summary_CC_Sets = {}
        summary_ACC_Sets = {}

        for i in range(67):
            print("btc2019-wikidata.org"+str(i))            
            acW = gsg.summaries()
            acW.load("../data/wikidata/btc2019-wikidata.org"+str(i)+"AC")
            summary_AC_Sets[i] = gsg.summarySet()
            summary_AC_Sets[i].get_summary(acW)
            
            ccW = gsg.summaries()
            ccW.load("../data/wikidata/btc2019-wikidata.org"+str(i)+"CC")
            summary_CC_Sets[i] = gsg.summarySet()
            summary_CC_Sets[i].get_summary(ccW)
            
            
            accW = gsg.summaries()
            accW.load("../data/wikidata/btc2019-wikidata.org"+str(i)+"ACC")
            summary_ACC_Sets[i] = gsg.summarySet()
            summary_ACC_Sets[i].get_summary(accW)
        
        
        verticesAC_L = []
        payloadAC_L = []
        edgesVAC_L = []
        edgesBAC_L = []
        edgesVBAC_L = []
        
        verticesCC_L = []
        payloadCC_L = []
        edgesVCC_L = []
        edgesBCC_L = []
        edgesVBCC_L = []
        
        verticesACC_L = []
        payloadACC_L = []
        edgesVACC_L = []
        edgesBACC_L = []
        edgesVBACC_L = []
        
        for i in range(67):
            verticesAC_L.append(summary_AC_Sets[i].vertices)
            payloadAC_L.append(summary_AC_Sets[i].payload)
            edgesVAC_L.append(summary_AC_Sets[i].edgesV)
            edgesBAC_L.append(summary_AC_Sets[i].edgesB)
            edgesVBAC_L.append(summary_AC_Sets[i].edgesVB)
            
            verticesCC_L.append(summary_CC_Sets[i].vertices)
            payloadCC_L.append(summary_CC_Sets[i].payload)
            edgesVCC_L.append(summary_CC_Sets[i].edgesV)
            edgesBCC_L.append(summary_CC_Sets[i].edgesB)
            edgesVBCC_L.append(summary_CC_Sets[i].edgesVB)
            
            verticesACC_L.append(summary_ACC_Sets[i].vertices)
            payloadACC_L.append(summary_ACC_Sets[i].payload)
            edgesVACC_L.append(summary_ACC_Sets[i].edgesV)
            edgesBACC_L.append(summary_ACC_Sets[i].edgesB)
            edgesVBACC_L.append(summary_ACC_Sets[i].edgesVB)
            
        print("AC:")    
        summaryAll_AC_Set.vertices = set().union(*verticesAC_L)
        print(len(summaryAll_AC_Set.vertices))
        summaryAll_AC_Set.payload = set().union(*payloadAC_L)
        summaryAll_AC_Set.edgesV = set().union(*edgesVAC_L)
        summaryAll_AC_Set.edgesB = set().union(*edgesBAC_L)
        summaryAll_AC_Set.edgesVB = set().union(*edgesVBAC_L)
        print("CC:")
        summaryAll_CC_Set.vertices = set().union(*verticesCC_L)
        print(len(summaryAll_CC_Set.vertices))
        summaryAll_CC_Set.payload = set().union(*payloadCC_L)
        summaryAll_CC_Set.edgesV = set().union(*edgesVCC_L)
        summaryAll_CC_Set.edgesB = set().union(*edgesBCC_L)
        summaryAll_CC_Set.edgesVB = set().union(*edgesVBCC_L)
        print("ACC:")
        summaryAll_ACC_Set.vertices = set().union(*verticesACC_L)
        print(len(summaryAll_ACC_Set.vertices))
        summaryAll_ACC_Set.payload = set().union(*payloadACC_L)
        summaryAll_ACC_Set.edgesV = set().union(*edgesVACC_L)
        summaryAll_ACC_Set.edgesB = set().union(*edgesBACC_L)
        summaryAll_ACC_Set.edgesVB = set().union(*edgesVBACC_L)
        
        print("AC:") 
        summaryAll_AC_Set.save("../data/wikidata/btc2019-wikidata.orgAC_Set")
        summaryAll_AC_Set.to_triples("../data/wikidata/btc2019-wikidata.orgAC")
        
        print("CC:") 
        summaryAll_CC_Set.save("../data/wikidata/btc2019-wikidata.orgCC_Set")
        summaryAll_CC_Set.to_triples("../data/wikidata/btc2019-wikidata.orgCC")
        
        print("ACC:") 
        summaryAll_ACC_Set.save("../data/wikidata/btc2019-wikidata.orgACC_Set")
        summaryAll_ACC_Set.to_triples("../data/wikidata/btc2019-wikidata.orgACC")
        
            
        
        for file in files:
            name = file.replace(".nq.gz","")
            print(name)
            if name != "btc2019-wikidata.org":
                print("AC") 
                summary1AC = gsg.summaries()
                summary1AC.load("../data/BTC2019/"+file.replace(".nq.gz","")+"AC")
                summary1AC_Set = gsg.summarySet()
                summary1AC_Set.get_summary(summary1AC)
                summary1AC_Set.save("../data/BTC2019/"+file.replace(".nq.gz","")+"AC_Set")
                summary1AC_Set.to_triples("../data/BTC2019/"+file.replace(".nq.gz","")+"AC")
   
                print("CC")
                summary1CC = gsg.summaries()
                summary1CC.load("../data/BTC2019/"+file.replace(".nq.gz","")+"CC")
                summary1CC_Set = gsg.summarySet()
                summary1CC_Set.get_summary(summary1CC)
                summary1CC_Set.save("../data/BTC2019/"+file.replace(".nq.gz","")+"CC_Set")
                summary1CC_Set.to_triples("../data/BTC2019/"+file.replace(".nq.gz","")+"CC")
                
                print("ACC")
                summary1ACC = gsg.summaries()
                summary1ACC.load("../data/BTC2019/"+file.replace(".nq.gz","")+"ACC") 
                summary1ACC_Set = gsg.summarySet()
                summary1ACC_Set.get_summary(summary1ACC)
                summary1ACC_Set.save("../data/BTC2019/"+file.replace(".nq.gz","")+"ACC_Set")
                summary1ACC_Set.to_triples("../data/BTC2019/"+file.replace(".nq.gz","")+"ACC")


    
def main():
    #Creating the summary structures used in the experiments. The structure is S=(V, B, E[V], E[V,B],E[B]).
    news_summary()
    code_summary()
    BTC_summary()


if __name__ == "__main__":
    main()
