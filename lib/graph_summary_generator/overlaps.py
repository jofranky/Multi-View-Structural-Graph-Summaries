import argparse
import configparser
import site
import sys
import re 
import pickle
site.addsitedir('../lib')  # Always appends to end


from graph_summary_generator import summary as gsg

import pathlib
import gzip
    


class overlaps():
        
    def __init__(self):
        self.ovAC = {}
        self.ovCC = {}
        self.ovACC = {}
        
        self.noAC = 0
        self.noCC = 0
        self.noACC = 0
        
        self.Case1AC = {}
        self.Case2AC = {}
        self.Case3AC ={}
        
        self.Case1CC = {}
        self.Case2CC = {}
        self.Case3CC ={}
        
        self.Case1ACC = {}
        self.Case2ACC = {}
        self.Case3ACC ={}
        
        
        self.noEdges = 0
        self.noVertices = 0
        self.ovVertices = {}
        self.ovPredicates = {}
         # utils
    def load(self, filename):
        """
        Load the given data file

        
        Args:
            filename (str): Filename
        """
        f = open(filename, 'rb')
        tmp_dict = pickle.load(f)
        f.close() 
        self.__dict__.update(tmp_dict) 

    def save(self, filename):
        """
        Save the class to a data file

        
        Args:
            filename (str): Filename
        """
        f = open(filename, 'wb')
        pickle.dump(self.__dict__, f, 2)
        f.close()  
        
    def analyzeNews(self):
        newsL = ["Al-Jazeera","CNN","euronews"]
        topics = ["CERN",        "Facebook",   "NFL",          "Obesity",              "Twitter",  "Cigarettes",   "FIFA",       "Nintendo",     "StanfordUniversity",   "WarnerBros",  "Disney",       "NBA",        "NobelPrize",   "TikTok", "WorldHealthOrganization"]
        allACs = set()
        allCCs = set()
        allACCs = set()
       
        allV = set()
        
        for topic in topics:
            for news in newsL:
                print("First: ",topic+"-"+news+".nq")
                
                gs1 = gsg.graph_for_summary( )
                gs1.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news)
                
                summary1AC = gsg.summaries()
                summary1AC.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"AC")
                
                summary1CC = gsg.summaries()
                summary1CC.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"CC")
                
                summary1ACC = gsg.summaries()
                summary1ACC.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news+"ACC")
                
                name1 = topic+"-"+news
                allACs = allACs.union(set(summary1AC.eqcsI.keys()))
                allCCs = allCCs.union(set(summary1CC.eqcsI.keys()))
                allACCs = allACCs.union(set(summary1ACC.eqcsI.keys()))
               
                allV = allV.union(set(summary1AC.eqcs.keys()))
                
                for edgeL in gs1.verticesI.values():
                    for i in edgeL:
                        self.noEdges += 1

                for news2 in newsL:

                    name2 = topic+"-"+news2

                    print("Second: ",topic+"-"+news2+".nq")

                    gs2 = gsg.graph_for_summary( )
                    gs2.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news2)

                    summary2AC = gsg.summaries()
                    summary2AC.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news2+"AC")

                    summary2CC = gsg.summaries()
                    summary2CC.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news2+"CC")

                    summary2ACC = gsg.summaries()
                    summary2ACC.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news2+"ACC")

                    #AC
                    if (name2,name1) in self.ovAC:
                        self.ovAC[(name1,name2)] = self.ovAC[(name2,name1)]
                    else:
                        self.ovAC[(name1,name2)] = len(set(summary1AC.eqcsI.keys()).intersection(set(summary2AC.eqcsI.keys())))
                    
                    #Cases
                    ovV = set(summary1AC.eqcs.keys()).intersection(set(summary2AC.eqcs.keys())) 
                    novV = set(summary1AC.eqcs.keys()) - set(summary2AC.eqcs.keys())
                    
                    case1 = 0
                    case2 = 0
                    case3 = 0
                    for v in ovV:
                        eqc1 = summary1AC.eqcs[v]
                        eqc2 = summary2AC.eqcs[v]
                        if eqc1 == eqc2:
                            case1 += 1
                        else:
                            case3 += 1
                    for v in novV:
                        eqc1 = summary1AC.eqcs[v]
                        if eqc1 in summary2AC.eqcsI:
                            case2 += 1
                        else: 
                            case1 += 1
                    self.Case1AC[(name1,name2)] = case1
                    self.Case2AC[(name1,name2)] = case2
                    self.Case3AC[(name1,name2)] = case3
                    
                    #CC
                    if (name2,name1) in self.ovCC:
                        self.ovCC[(name1,name2)] = self.ovCC[(name2,name1)]
                    else:
                        self.ovCC[(name1,name2)] = len(set(summary1CC.eqcsI.keys()).intersection(set(summary2CC.eqcsI.keys())))
                    
                    #Cases
                    ovV = set(summary1CC.eqcs.keys()).intersection(set(summary2CC.eqcs.keys()))
                    novV = set(summary1CC.eqcs.keys()) - set(summary2CC.eqcs.keys())
                    
                    case1 = 0
                    case2 = 0
                    case3 = 0
                    for v in ovV:
                        eqc1 = summary1CC.eqcs[v]
                        eqc2 = summary2CC.eqcs[v]
                        if eqc1 == eqc2:
                            case1 += 1
                        else:
                            case3 += 1
                    for v in novV:
                        eqc1 = summary1CC.eqcs[v]
                        if eqc1 in summary2CC.eqcsI:
                            case2 += 1
                        else: 
                            case1 += 1
                            
                    self.Case1CC[(name1,name2)] = case1
                    self.Case2CC[(name1,name2)] = case2
                    self.Case3CC[(name1,name2)] = case3
                    
                    #ACC
                    if (name2,name1) in self.ovACC:
                        self.ovACC[(name1,name2)] = self.ovACC[(name2,name1)]
                    else:
                        self.ovACC[(name1,name2)] = len(set(summary1ACC.eqcsI.keys()).intersection(set(summary2ACC.eqcsI.keys())))
                    
                    #Cases
                    ovV = set(summary1ACC.eqcs.keys()).intersection(set(summary2ACC.eqcs.keys()))
                    novV = set(summary1ACC.eqcs.keys()) - set(summary2ACC.eqcs.keys())
                    
                    case1 = 0
                    case2 = 0
                    case3 = 0
                    for v in ovV:
                        eqc1 = summary1ACC.eqcs[v]
                        eqc2 = summary2ACC.eqcs[v]
                        if eqc1 == eqc2:
                            case1 += 1
                        else:
                            case3 += 1
                    for v in novV:
                        eqc1 = summary1ACC.eqcs[v]
                        if eqc1 in summary2ACC.eqcsI:
                            case2 += 1
                        else: 
                            case1 += 1
                            
                    self.Case1ACC[(name1,name2)] = case1
                    self.Case2ACC[(name1,name2)] = case2
                    self.Case3ACC[(name1,name2)] = case3
                    
                    #vertices
                    self.ovVertices[(name1,name2)] = len(ovV)
                    #labels
                    self.ovPredicates[(name1,name2)] = len(gs1.edgesL.intersection(gs2.edgesL))
                        
        self.noAC = len(allACs)
        self.noCC = len(allCCs)
        self.noACC  = len(allACCs) 
        self.noVertices = len(allV) 
            
    def analyzeBTC(self):
        
        fr = open("files.txt")
        files = fr.read()
        files = files.replace(".nq",".nq.gz")
        files = files.split("\n")

        
        allACs = set()
        allCCs = set()
        allACCs = set()
       
        allV = set()
        p = 0
        
        graphs = {}
        summaryACs = {}
        summaryCCs = {}
        summaryACCs = {}
        
        
        l = 0
        #loading phase:
        graphs["btc2019-wikidata.org"] = gsg.graph_for_summary( )
  
        summaryACs["btc2019-wikidata.org"] = gsg.summaries()
        summaryACs["btc2019-wikidata.org"].summary = "AC"
            
        summaryCCs["btc2019-wikidata.org"] = gsg.summaries()
        summaryCCs["btc2019-wikidata.org"].summary = "CC"
            
        summaryACCs["btc2019-wikidata.org"] = gsg.summaries()
        summaryACCs["btc2019-wikidata.org"].summary = "ACC"

        
        for i in range(67):
            print("btc2019-wikidata.org"+str(i))
            gsW = gsg.graph_for_summary( )
            gsW.load("../data/wikidata/btc2019-wikidata.org"+str(i))
            acW = gsg.summaries()
            acW.load("../data/wikidata/btc2019-wikidata.org"+str(i)+"AC")
            ccW = gsg.summaries()
            ccW.load("../data/wikidata/btc2019-wikidata.org"+str(i)+"CC")
            accW = gsg.summaries()
            accW.load("../data/wikidata/btc2019-wikidata.org"+str(i)+"ACC")
            
            graphs["btc2019-wikidata.org"].verticesI.update(gsW.verticesI)
            graphs["btc2019-wikidata.org"].edgesL = graphs["btc2019-wikidata.org"].edgesL.union(gsW.edgesL)
            
            summaryACs["btc2019-wikidata.org"].eqcs.update(acW.eqcs)
            summaryACs["btc2019-wikidata.org"].eqcsI.update(acW.eqcsI)
            
            summaryCCs["btc2019-wikidata.org"].eqcs.update(ccW.eqcs)
            summaryCCs["btc2019-wikidata.org"].eqcsI.update(ccW.eqcsI)
            
            summaryACCs["btc2019-wikidata.org"].eqcs.update(accW.eqcs)
            summaryACCs["btc2019-wikidata.org"].eqcsI.update(accW.eqcsI)
        
        for file in files:
            name = file.replace(".nq.gz","")
            if name != "btc2019-wikidata.org":
            
                graphs[name] = gsg.graph_for_summary( )
                graphs[name].load("../data/BTC2019/"+file.replace(".nq.gz",""))

                summaryACs[name] = gsg.summaries()
                summaryACs[name].load("../data/BTC2019/"+file.replace(".nq.gz","")+"AC")

                summaryCCs[name] = gsg.summaries()
                summaryCCs[name].load("../data/BTC2019/"+file.replace(".nq.gz","")+"CC")

                summaryACCs[name] = gsg.summaries()
                summaryACCs[name].load("../data/BTC2019/"+file.replace(".nq.gz","")+"ACC")
            l +=1
            print(l," of ",len(files)," loaded.")
        
        for file in files:
                name1 = file.replace(".nq.gz","")
                p2 = 0
                gs1 = graphs[name1]

                summary1AC = summaryACs[name1]
                
                summary1CC = summaryCCs[name1]
                
                summary1ACC = summaryACCs[name1]
                
                
                allACs = allACs.union(set(summary1AC.eqcsI.keys()))
                allCCs = allCCs.union(set(summary1CC.eqcsI.keys()))
                allACCs = allACCs.union(set(summary1ACC.eqcsI.keys()))
               
                allV = allV.union(set(summary1AC.eqcs.keys()))
                
                for edgeL in gs1.verticesI.values():
                    for i in edgeL:
                        self.noEdges += 1

                for file2 in files:

                    name2 = file2.replace(".nq.gz","")

                    #print("Second: ",name2)

                    gs2 = graphs[name2]

                    summary2AC = summaryACs[name2]

                    summary2CC = summaryCCs[name2]

                    summary2ACC = summaryACCs[name2]

                    #AC
                    if (name2,name1) in self.ovAC:
                        self.ovAC[(name1,name2)] = self.ovAC[(name2,name1)]
                    else:
                        self.ovAC[(name1,name2)] = len(set(summary1AC.eqcsI.keys()).intersection(set(summary2AC.eqcsI.keys())))
                    
                    #Cases
                    ovV = set(summary1AC.eqcs.keys()).intersection(set(summary2AC.eqcs.keys())) 
                    novV = set(summary1AC.eqcs.keys()) - set(summary2AC.eqcs.keys())
                    
                    case1 = 0
                    case2 = 0
                    case3 = 0
                    for v in ovV:
                        eqc1 = summary1AC.eqcs[v]
                        eqc2 = summary2AC.eqcs[v]
                        if eqc1 == eqc2:
                            case1 += 1
                        else:
                            case3 += 1
                    for v in novV:
                        eqc1 = summary1AC.eqcs[v]
                        if eqc1 in summary2AC.eqcsI:
                            case2 += 1
                        else: 
                            case1 += 1
                    self.Case1AC[(name1,name2)] = case1
                    self.Case2AC[(name1,name2)] = case2
                    self.Case3AC[(name1,name2)] = case3
                    
                    #CC
                    if (name2,name1) in self.ovCC:
                        self.ovCC[(name1,name2)] = self.ovCC[(name2,name1)]
                    else:
                        self.ovCC[(name1,name2)] = len(set(summary1CC.eqcsI.keys()).intersection(set(summary2CC.eqcsI.keys())))
                    
                    #Cases
                    ovV = set(summary1CC.eqcs.keys()).intersection(set(summary2CC.eqcs.keys()))
                    novV = set(summary1CC.eqcs.keys()) - set(summary2CC.eqcs.keys())
                    
                    case1 = 0
                    case2 = 0
                    case3 = 0
                    for v in ovV:
                        eqc1 = summary1CC.eqcs[v]
                        eqc2 = summary2CC.eqcs[v]
                        if eqc1 == eqc2:
                            case1 += 1
                        else:
                            case3 += 1
                    for v in novV:
                        eqc1 = summary1CC.eqcs[v]
                        if eqc1 in summary2CC.eqcsI:
                            case2 += 1
                        else: 
                            case1 += 1
                            
                    self.Case1CC[(name1,name2)] = case1
                    self.Case2CC[(name1,name2)] = case2
                    self.Case3CC[(name1,name2)] = case3
                    
                    #ACC
                    if (name2,name1) in self.ovACC:
                        self.ovACC[(name1,name2)] = self.ovACC[(name2,name1)]
                    else:
                        self.ovACC[(name1,name2)] = len(set(summary1ACC.eqcsI.keys()).intersection(set(summary2ACC.eqcsI.keys())))
                    
                    #Cases
                    ovV = set(summary1ACC.eqcs.keys()).intersection(set(summary2ACC.eqcs.keys()))
                    novV = set(summary1ACC.eqcs.keys()) - set(summary2ACC.eqcs.keys())
                    
                    case1 = 0
                    case2 = 0
                    case3 = 0
                    for v in ovV:
                        eqc1 = summary1ACC.eqcs[v]
                        eqc2 = summary2ACC.eqcs[v]
                        if eqc1 == eqc2:
                            case1 += 1
                        else:
                            case3 += 1
                    for v in novV:
                        eqc1 = summary1ACC.eqcs[v]
                        if eqc1 in summary2ACC.eqcsI:
                            case2 += 1
                        else: 
                            case1 += 1
                            
                    self.Case1ACC[(name1,name2)] = case1
                    self.Case2ACC[(name1,name2)] = case2
                    self.Case3ACC[(name1,name2)] = case3
                    
                    #vertices
                    self.ovVertices[(name1,name2)] = len(ovV)
                    #labels
                    self.ovPredicates[(name1,name2)] = len(gs1.edgesL.intersection(gs2.edgesL))
                    p2 += 1
                    print("FinishedPart: ",(p2/len(files))*100,"%") 
                p += 1
                print("\nFinishedAll: ",(p/len(files))*100,"%")        
        self.noAC = len(allACs)
        self.noCC = len(allCCs)
        self.noACC  = len(allACCs) 
        self.noVertices = len(allV) 
        
      
                
                
class overlapsCode():
        
    def __init__(self):
        self.ovAC = {}
        self.ovCC = {}
        self.ovACC = {}
        
        self.noAC = set()
        self.noCC = set()
        self.noACC = set()
        
        self.Case1AC = {}
        self.Case2AC = {}
        self.Case3AC ={}
        
        self.Case1CC = {}
        self.Case2CC = {}
        self.Case3CC ={}
        
        self.Case1ACC = {}
        self.Case2ACC = {}
        self.Case3ACC ={}
        
        
        self.noEdges = 0
        self.noVertices = set()
        self.ovVertices = {}
        self.ovPredicates = {}
         # utils
    def load(self, filename):
        """
        Load the given data file

        
        Args:
            filename (str): Filename
        """
        f = open(filename, 'rb')
        tmp_dict = pickle.load(f)
        f.close() 
        self.__dict__.update(tmp_dict) 

    def save(self, filename):
        """
        Save the class to a data file

        
        Args:
            filename (str): Filename
        """
        f = open(filename, 'wb')
        pickle.dump(self.__dict__, f, 2)
        f.close()  
      
                             
        
    def analyzeCode(self,part):
        
       

        
        fr = open("rfiles"+str(part)+".txt")
        print("rfiles"+str(part)+".txt")
        files = fr.read()
        files = files.replace(".R\n","\n")
        files = files.split("\n")
        fr.close()
        iC = 0
        files = files[:-1]
        
        allI = len(files)
        
        allACs = {}
        allCCs = {}
        allACCs = {}    
        
        allVertices = {}
        
        for file in files:
        
            iC += 1
            print(str((iC/allI)*100),"%")
            for part in [".dfg",".cfg",".normalize"]:
                name1 = file+"-"+part
                #print("First: ",name1)
  
                gs1 = gsg.graph_for_summary( )
                gs1.load("../data/"+file+part)

                summary1AC = gsg.summaries()
                summary1AC.load("../data/"+file+part+"AC")

                summary1CC = gsg.summaries()
                summary1CC.load("../data/"+file+part+"CC")

                summary1ACC = gsg.summaries()
                summary1ACC.load("../data/"+file+part+"ACC")
                
                
                
                allACs[name1] = set(summary1AC.eqcsI.keys())
                allCCs[name1]= set(summary1CC.eqcsI.keys())
                allACCs[name1] = set(summary1ACC.eqcsI.keys())
               
                allVertices[name1] = set(summary1AC.eqcs.keys())
                
                
               
                
                for edgeL in gs1.verticesI.values():
                    for i in edgeL:
                        self.noEdges += 1

                for part2 in [".dfg",".cfg",".normalize"]:

                    name2 = file+"-"+part2

                    #print("Second: ",name2)

                    gs2 = gsg.graph_for_summary( )
                    gs2.load("../data/"+file+part2)

                    summary2AC = gsg.summaries()
                    summary2AC.load("../data/"+file+part2+"AC")

                    summary2CC = gsg.summaries()
                    summary2CC.load("../data/"+file+part2+"CC")

                    summary2ACC = gsg.summaries()
                    summary2ACC.load("../data/"+file+part2+"ACC")

                    #AC
                    if (name2,name1) in self.ovAC:
                        self.ovAC[(name1,name2)] = self.ovAC[(name2,name1)]
                    else:
                        self.ovAC[(name1,name2)] = len(set(summary1AC.eqcsI.keys()).intersection(set(summary2AC.eqcsI.keys())))
                    
                    #Cases
                    ovV = set(summary1AC.eqcs.keys()).intersection(set(summary2AC.eqcs.keys())) 
                    novV = set(summary1AC.eqcs.keys()) - set(summary2AC.eqcs.keys())
                    
                    case1 = 0
                    case2 = 0
                    case3 = 0
                    for v in ovV:
                        eqc1 = summary1AC.eqcs[v]
                        eqc2 = summary2AC.eqcs[v]
                        if eqc1 == eqc2:
                            case1 += 1
                        else:
                            case3 += 1
                    for v in novV:
                        eqc1 = summary1AC.eqcs[v]
                        if eqc1 in summary2AC.eqcsI:
                            case2 += 1
                        else: 
                            case1 += 1
                    self.Case1AC[(name1,name2)] = case1
                    self.Case2AC[(name1,name2)] = case2
                    self.Case3AC[(name1,name2)] = case3
                    
                    #CC
                    if (name2,name1) in self.ovCC:
                        self.ovCC[(name1,name2)] = self.ovCC[(name2,name1)]
                    else:
                        self.ovCC[(name1,name2)] = len(set(summary1CC.eqcsI.keys()).intersection(set(summary2CC.eqcsI.keys())))
                    
                    #Cases
                    ovV = set(summary1CC.eqcs.keys()).intersection(set(summary2CC.eqcs.keys()))
                    novV = set(summary1CC.eqcs.keys()) - set(summary2CC.eqcs.keys())
                    
                    case1 = 0
                    case2 = 0
                    case3 = 0
                    for v in ovV:
                        eqc1 = summary1CC.eqcs[v]
                        eqc2 = summary2CC.eqcs[v]
                        if eqc1 == eqc2:
                            case1 += 1
                        else:
                            case3 += 1
                    for v in novV:
                        eqc1 = summary1CC.eqcs[v]
                        if eqc1 in summary2CC.eqcsI:
                            case2 += 1
                        else: 
                            case1 += 1
                            
                    self.Case1CC[(name1,name2)] = case1
                    self.Case2CC[(name1,name2)] = case2
                    self.Case3CC[(name1,name2)] = case3
                    
                    #ACC
                    if (name2,name1) in self.ovACC:
                        self.ovACC[(name1,name2)] = self.ovACC[(name2,name1)]
                    else:
                        self.ovACC[(name1,name2)] = len(set(summary1ACC.eqcsI.keys()).intersection(set(summary2ACC.eqcsI.keys())))
                    
                    #Cases
                    ovV = set(summary1ACC.eqcs.keys()).intersection(set(summary2ACC.eqcs.keys()))
                    novV = set(summary1ACC.eqcs.keys()) - set(summary2ACC.eqcs.keys())
                    
                    case1 = 0
                    case2 = 0
                    case3 = 0
                    for v in ovV:
                        eqc1 = summary1ACC.eqcs[v]
                        eqc2 = summary2ACC.eqcs[v]
                        if eqc1 == eqc2:
                            case1 += 1
                        else:
                            case3 += 1
                    for v in novV:
                        eqc1 = summary1ACC.eqcs[v]
                        if eqc1 in summary2ACC.eqcsI:
                            case2 += 1
                        else: 
                            case1 += 1
                            
                    self.Case1ACC[(name1,name2)] = case1
                    self.Case2ACC[(name1,name2)] = case2
                    self.Case3ACC[(name1,name2)] = case3
                    
                    #vertices
                    self.ovVertices[(name1,name2)] = len(ovV)
                    #labels
                    self.ovPredicates[(name1,name2)] = len(gs1.edgesL.intersection(gs2.edgesL))
        
        print("set union")
        
        self.noAC = set().union(*list(allACs.values()))
        print(len(self.noAC))
        
        self.noCC= set().union(*list(allCCs.values()))
        print(len(self.noCC))
        
        self.noACC = set().union(*list(allACCs.values()))
        print(len(self.noACC))
    
        self.noVertices = set().union(*list(allVertices.values()))
        print(len(self.noVertices))

    