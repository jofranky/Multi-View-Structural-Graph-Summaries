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
    
def BTC_randomAll(part,i):
        r = random.Random(510*i) # seed number is 510 times i
        print(510*i)
        fr = open("Files/files.txt")
        filesR = fr.read()
        filesR = filesR.replace(".nq","")
        filesR = filesR.split("\n")
        times = mt.mergeTime()  
        times.load("Times/TimesOfBTC2019RandomS_"+part)
        times.name = "BTCRandom_"+part
        print(part)

        summarys = {}

        files = []

        l = 0
        #loading phase:
        for file in filesR:
            name = file.replace(".nq.gz","")
            if name != "btc2019-wikidata.org":

                summarys[name] = gsg.summarySet()
                summarys[name].load("../data/BTC2019/"+file+part+"_Set")
                files.append(name)

            else:
                summarys[name] = gsg.summarySet()
                summarys[name].load("../data/wikidata/"+file+part+"_Set")
                files.append(name)

            l +=1
            print(l," of ",len(filesR)," loaded.")

        merged = 0
        res = 0
        path = []

        while files:
                print(i,"-",merged)
                name1 = r.choice(files)
                files.remove(name1)

                summary1_Set = summarys[name1]

                if files:
                    name2 = r.choice(files)
                    path.append((name1,name2))
                    files.remove(name2)
                    summary2_Set = summarys[name2]

                    merged += 1

                    st = time.process_time()
                    s = merge(summary1_Set,summary2_Set,part)
                    et = time.process_time()
                    #get execution time
                    res += et - st
                    summarys[str(merged)] = s

                    files.append(str(merged))

        if part == "AC":
            times.timeAC[i] = res
            times.timeAC["path"+str(i)] = path
        elif part == "CC":
            times.timeCC[i] = res
            times.timeCC["path"+str(i)] = path
        elif part == "ACC":
            times.timeACC[i] = res
            times.timeACC["path"+str(i)] =path
        
        times.save("Times/TimesOfBTC2019RandomS_"+part)
        
        
def BTC_min(part,i):
        maxV = False
        fr = open("Files/files.txt")
        filesR = fr.read()
        filesR = filesR.replace(".nq","")
        filesR = filesR.split("\n")
        times = mt.mergeTime()  
        times.load("Times/TimesOfBTC2019MinS_"+part)
        times.name = "BTCMin_"+part       
        summarys = {}

        files = []

        l = 0
        #loading phase:
        for file in filesR:
            name = file.replace(".nq.gz","")
            if name != "btc2019-wikidata.org":

                summarys[name] = gsg.summarySet()
                summarys[name].load("../data/BTC2019/"+file+part+"_Set")
                files.append((len(summarys[name].vertices)+len(summarys[name].payload),name))

            else:
                summarys[name] = gsg.summarySet()
                summarys[name].load("../data/wikidata/"+file+part+"_Set")
                files.append((len(summarys[name].vertices)+len(summarys[name].payload),name))

            l +=1
            print(l," of ",len(filesR)," loaded.")

        merged = 0
        res = 0
        path = []
        print(part)
        files.sort(reverse = maxV)
        while files:
                print(len(files))
                name1 = files.pop(0)[1]

                summary1_Set = summarys[name1]

                if files:
                    name2 = files.pop(0)[1]
                    path.append((name1,name2))
                    summary2_Set = summarys[name2]

                    merged += 1
                    #AC
                    st = time.process_time()
                    s = merge(summary1_Set,summary2_Set,part)
                    et = time.process_time()
                    #get execution time
                    res += et - st
                    summarys[str(merged)] = s

                    #delete old summaries
                    summarys[name1] = ""
                    summarys[name2] = ""

                    files.append(((len(summarys[str(merged)].vertices)+len(summarys[str(merged)].payload),str(merged))))
                    files.sort(reverse = maxV)

        if part == "AC":
            times.timeAC[i] = res
            times.timeAC["path"+str(i)] = path
        elif part == "CC":
            times.timeCC[i] = res
            times.timeCC["path"+str(i)] = path
        elif part == "ACC":
            times.timeACC[i] = res
            times.timeACC["path"+str(i)] =path

        times.save("Times/TimesOfBTC2019MinS_"+part)
        
        
        
def BTC_parallelAll(part,i):
        fr = open("Files/files.txt")
        filesR = fr.read()
        filesR = filesR.replace(".nq","")
        filesR = filesR.split("\n")
        times = mt.mergeTime() 
        times.load("Times/TimesOfBTC2019ParallelS_"+part)
        times.name = "BTCParallel"
        

        summarys = {}


        files = []
        l = 0
        #loading phase:
        for file in filesR:
            name = file.replace(".nq.gz","")
            if name != "btc2019-wikidata.org":

                summarys[name] = gsg.summarySet()
                summarys[name].load("../data/BTC2019/"+file+part+"_Set")
                files.append((0,name))

            else:
                summarys[name] = gsg.summarySet()
                summarys[name].load("../data/wikidata/"+file+part+"_Set")
                files.append((0,name))

            l +=1
            print(l," of ",len(filesR)," loaded.")


        merged = 0
        path = []
        print(part)
        while len(files) > 1:
                print(len(files))
                name1 = files.pop(0)[1]

                summary1_Set = summarys[name1]

                if files:
                    time2,name2 = files.pop(0)
                    path.append((name1,name2))
                    summary2_Set = summarys[name2]

                    merged += 1

                    st = time.process_time()
                    s = merge(summary1_Set,summary2_Set,part)
                    et = time.process_time()
                    #get execution time
                    res = et - st
                    summarys[str(merged)] = s

                    files.append((time2+res,str(merged)))
                    if time2 != 0:
                        files.sort()

        if part == "AC":
            times.timeAC[i] = files.pop(0)[0]
            times.timeAC["path"+str(i)] = path
        elif part == "CC":
            times.timeCC[i] = files.pop(0)[0]
            times.timeCC["path"+str(i)] = path
        elif part == "ACC":
            times.timeACC[i] = files.pop(0)[0]
            times.timeACC["path"+str(i)] =path

        times.save("Times/TimesOfBTC2019ParallelS_"+part)

def BTC_max(part,i):
        maxV = True
        fr = open("Files/files.txt")
        filesR = fr.read()
        filesR = filesR.replace(".nq","")
        filesR = filesR.split("\n")
        times = mt.mergeTime()  
        times.load("Times/TimesOfBTC2019MaxS_"+part)
        times.name = "BTCMax_"+part
       
        summarys = {}

        files = []

        l = 0
        #loading phase:
        for file in filesR:
            name = file.replace(".nq.gz","")
            if name != "btc2019-wikidata.org":

                summarys[name] = gsg.summarySet()
                summarys[name].load("../data/BTC2019/"+file+part+"_Set")
                files.append((len(summarys[name].vertices)+len(summarys[name].payload),name))

            else:
                summarys[name] = gsg.summarySet()
                summarys[name].load("../data/wikidata/"+file+part+"_Set")
                files.append((len(summarys[name].vertices)+len(summarys[name].payload),name))

            l +=1
            print(l," of ",len(filesR)," loaded.")

        merged = 0
        res = 0
        path = []
        print(part)
        files.sort(reverse = maxV)
        while files:
                print(len(files))
                name1 = files.pop(0)[1]

                summary1_Set = summarys[name1]

                if files:
                    name2 = files.pop(0)[1]
                    path.append((name1,name2))
                    summary2_Set = summarys[name2]

                    merged += 1
                    #AC
                    st = time.process_time()
                    s = merge(summary1_Set,summary2_Set,part)
                    et = time.process_time()
                    #get execution time
                    res += et - st
                    summarys[str(merged)] = s

                    #delete old summaries
                    summarys[name1] = ""
                    summarys[name2] = ""

                    files.append(((len(summarys[str(merged)].vertices)+len(summarys[str(merged)].payload),str(merged))))
                    files.sort(reverse = maxV)

        if part == "AC":
            times.timeAC[i] = res
            times.timeAC["path"+str(i)] = path
        elif part == "CC":
            times.timeCC[i] = res
            times.timeCC["path"+str(i)] = path
        elif part == "ACC":
            times.timeACC[i] = res
            times.timeACC["path"+str(i)] =path

        times.save("Times/TimesOfBTC2019MaxS_"+part)
       

def main():
    #Experiment: Merging BTC 2019
    #Used by all.sh
    
    args = sys.argv
    #Which dataset should be used?
    stra = int(args[1])
    summary = int(args[2])
    number = int(args[3])
    
    if stra == 0:
        times = mt.mergeTime()
        for part in ["AC","CC","ACC"]:
            times.save("Times/TimesOfBTC2019MaxS_"+part)
            times.save("Times/TimesOfBTC2019ParallelS_"+part)
            times.save("Times/TimesOfBTC2019MinS_"+part)
            times.save("Times/TimesOfBTC2019RandomS_"+part)
        
    if stra == 1:
        if summary == 1:
            BTC_min("AC",number )
        elif summary == 2:
            BTC_min("CC",number )
        elif summary == 3:
            BTC_min("ACC",number )
        
    elif stra == 2:
        if summary == 1:
            BTC_max("AC",number )
        elif summary == 2:
            BTC_max("CC",number )
        elif summary == 3:
            BTC_max("ACC",number )
        
    elif stra == 3:
        if summary == 1:
            BTC_parallelAll("AC",number )
        elif summary == 2:
            BTC_parallelAll("CC",number )
        elif summary == 3:
            BTC_parallelAll("ACC",number )
            
    elif stra == 4:
        if summary == 1:
            BTC_randomAll("AC",number )
        elif summary == 2:
            BTC_randomAll("CC",number )
        elif summary == 3:
            BTC_randomAll("ACC",number )

if __name__ == "__main__":
    main()