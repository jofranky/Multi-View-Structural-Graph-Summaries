import argparse
import configparser
import site
import sys
import re 
import pickle
site.addsitedir('../lib')  # Always appends to end


from graph_summary_generator import summary as gsg
from graph_summary_generator import overlaps  as ove
from graph_summary_generator import mergeTime  as mt
import pathlib
import gzip
from timeit import default_timer as timer
import time
#disable randomization of hash
import os
import sys
hashseed = os.getenv('PYTHONHASHSEED')
if not hashseed:
  os.environ['PYTHONHASHSEED'] = '0'
  os.execv(sys.executable, [sys.executable] + sys.argv)
import random   
    

"""
Algorithm for merging two summaries with auxiliary functions.
Including improvements that improve the running time.
Comment Speedup indicates such an improvement.
"""

def merge(s1,s2,psi):
    #Phase1
    s = gsg.summarySet()
    s.vertices = s1.vertices.union(s2.vertices)
    s.payload = s1.payload.union(s2.payload)
    s.edgesV = s1.edgesV.union(s2.edgesV)
    s.edgesB = s1.edgesB.union(s2.edgesB)
    s.edgesVB = s1.edgesVB.union(s2.edgesVB)
    
    #Phase2
    getEQC1 = getEQC(s1)
    getEQC2 = getEQC(s2)
    members1 = getMembers(s1)
    members2 = getMembers(s2)
    i = 0

    #Speedup
    schema = {}
    for v in s.edgesV:
        if v[0] in schema:
            schema[v[0]].append((v[1],v[2]))
        else:
            schema[v[0]] = [(v[1],v[2])]
    schema["hash:0"] = []

    for m in members1:
        if m in members2:
            eqc1 = getEQC1[m]
            eqc2 = getEQC2[m]
            if eqc1 != eqc2:
                combineEQCs(s,eqc1,eqc2,m,psi,schema)
                
                
    #Phase3
    eqcM = {}
    for edge in s.edgesVB:
        eqcM[edge[0]] = 0
    for me in  s.edgesB:
         if me[1] == "https://uni-ulm.de/member":
            eqcM[me[0].replace("payload:","hash:")] += 1
    for k in eqcM:
        if eqcM[k] == 0:
            s.vertices.remove(k)
            s.payload.remove(k.replace("hash:","payload:"))
            s.edgesVB.remove((k,"https://uni-ulm.de/payload",k.replace("hash:","payload:"))) 
            #speedup
            for se in schema[k]:
                s.edgesV.remove((k,se[0],se[1]))

            
    return s
            

def getMembers(s):
    members = set()
    for m in s.edgesB:
        if m[1] == "https://uni-ulm.de/member":
            members.add(m[2])
    return members

def getEQC(s):
    eqcs = {}
    for m in s.edgesB:
        if m[1] == "https://uni-ulm.de/member":
            eqcs[m[2]] = m[0]
    return eqcs 

def combineEQCs(s,eqc1,eqc2,m,psi,schema):
    s.edgesB.remove((eqc1.replace("hash:","payload:"),"https://uni-ulm.de/member",m))
    s.edgesB.remove((eqc2.replace("hash:","payload:"),"https://uni-ulm.de/member",m))

    e = set()
    vertices = set()
    vertices.add(m)

    #speedup
    for edge in schema[eqc1.replace("payload:","hash:")]:
         e.add((m,edge[0],edge[1]))
         vertices.add(edge[1])
    for edge in schema[eqc2.replace("payload:","hash:")]:
         e.add((m,edge[0],edge[1]))
         vertices.add(edge[1])

    eqc = createEQC(vertices,e,m,psi)
        
    s.vertices.add(eqc)
    s.payload.add(eqc.replace("hash:","payload:"))
    for edge in e:
        s.edgesV.add((eqc,edge[1],edge[2]))
    s.edgesVB.add((eqc,"https://uni-ulm.de/payload",eqc.replace("hash:","payload:")))
    s.edgesB.add((eqc.replace("hash:","payload:"),"https://uni-ulm.de/member",m))


#v only for summaries with more than 1-hop important
#m not important for 1-hop
def createEQC(v,e,m,psi):
    tmp_feature_list = []
    tmp_property_list = []
    tmp_type_list = []
    if psi == "AC":
        for h in e:
            if h[1] != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and h[1] not in tmp_property_list:
                tmp_feature_list.append(h[1])
                tmp_property_list.append(h[1])
    elif psi == "CC":
         for h in e:
            if h[1] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and h[2]  not in tmp_type_list:
                tmp_feature_list.append(h[2])
                tmp_type_list.append(h[2])
        
    elif psi == "ACC":
         for h in e:
            if h[1] != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and h[1] not in tmp_property_list:
                tmp_feature_list.append(h[1])
                tmp_property_list.append(h[1])
            if h[1] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and h[2]  not in tmp_type_list:
                tmp_feature_list.append(h[2])
                tmp_type_list.append(h[2])
        
    
    tmp_feature_list.sort()
    tmp_feature_list_string = "".join(tmp_feature_list)
    tmp_hash = hash(tmp_feature_list_string)
    return "hash:"+str(tmp_hash)


"""
Experiments:
"""
    
def news_merge():
    newsL = ["Al-Jazeera","CNN","euronews"]
    topics = ["CERN",        "Facebook",   "NFL",          "Obesity",              "Twitter",  "Cigarettes",   "FIFA",       "Nintendo",     "StanfordUniversity",   "WarnerBros",  "Disney",       "NBA",        "NobelPrize",   "TikTok", "WorldHealthOrganization"]
    times =  mt.mergeTime() 
    times.name = "News"
    for topic in topics:
        for news in newsL:
            name1 = topic+"-"+news
            print("First: ",topic+"-"+news+".nq")
          
            summary1AC_Set = gsg.summarySet()
            summary1AC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"AC_Set")

            summary1CC_Set = gsg.summarySet()
            summary1CC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"CC_Set")
            

            summary1ACC_Set = gsg.summarySet()
            summary1ACC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"ACC_Set")
            for news2 in newsL:
                name2 = topic+"-"+news2
                print("Second: ",topic+"-"+news+".nq")
                summary2AC_Set = gsg.summarySet()
                summary2AC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news2+"AC_Set")

                summary2CC_Set = gsg.summarySet()
                summary2CC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news2+"CC_Set")


                summary2ACC_Set = gsg.summarySet()
                summary2ACC_Set.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news2+"ACC_Set")
                
                #AC
                st = time.process_time()
                s = merge(summary1AC_Set,summary2AC_Set,"AC")
                et = time.process_time()
                # get execution time
                res = et - st
                times.timeAC[name1,name2] = res
                
                #CC
                st = time.process_time()
                s = merge(summary1CC_Set,summary2CC_Set,"CC")
                et = time.process_time()
                # get execution time
                res = et - st
                times.timeCC[name1,name2] = res
                
                #ACC
                st = time.process_time()
                s = merge(summary1ACC_Set,summary2ACC_Set,"ACC")
                et = time.process_time()
                # get execution time
                res = et - st
                times.timeACC[name1,name2] = res
    times.save("Times/TimesOfNews")
    
def BTC_merge():
        
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
                    
                    #AC
                    st = time.process_time()
                    s = merge(summary1AC_Set,summary2AC_Set,"AC")
                    et = time.process_time()
                    # get execution time
                    res = et - st
                    times.timeAC[name1,name2] = res

                    #CC
                    st = time.process_time()
                    s = merge(summary1CC_Set,summary2CC_Set,"CC")
                    et = time.process_time()
                    # get execution time
                    res = et - st
                    times.timeCC[name1,name2] = res

                    #ACC
                    st = time.process_time()
                    s = merge(summary1ACC_Set,summary2ACC_Set,"ACC")
                    et = time.process_time()
                    # get execution time
                    res = et - st
                    times.timeACC[name1,name2] = res
        times.save("Times/TimesOfBTC2019")
        
        
def code_merge():
    fr = open("Files/rfiles.txt")
    print("rfiles.txt")
    files = fr.read()
    files = files.replace(".R\n","\n")
    files = files.split("\n")
    fr.close()
    iC = 0
    files = files[:-1]
    allI = len(files)
    times = mt.mergeTime() 
    times.name = "Code"
    for file in files:
        iC += 1
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
                name2 = file+"-"+part2
                summary2AC_Set = gsg.summarySet()
                summary2AC_Set.load("../data/"+file+part2+"AC_Set")

                summary2CC_Set = gsg.summarySet()
                summary2CC_Set.load("../data/"+file+part2+"CC_Set")


                summary2ACC_Set = gsg.summarySet()
                summary2ACC_Set.load("../data/"+file+part2+"ACC_Set")
                
                #AC
                st = time.process_time()
                s = merge(summary1AC_Set,summary2AC_Set,"AC")
                et = time.process_time()
                # get execution time
                res = et - st
                times.timeAC[name1,name2] = res
                
                #CC
                st = time.process_time()
                s = merge(summary1CC_Set,summary2CC_Set,"CC")
                et = time.process_time()
                # get execution time
                res = et - st
                times.timeCC[name1,name2] = res
                
                #ACC
                st = time.process_time()
                s = merge(summary1ACC_Set,summary2ACC_Set,"ACC")
                et = time.process_time()
                # get execution time
                res = et - st
                times.timeACC[name1,name2] = res
    times.save("Times/TimesOfCode")
    

       

def main():
#Experiment: Pairwise merging
    BTC_merge()
    news_merge()
    code_merge()

if __name__ == "__main__":
    main()

