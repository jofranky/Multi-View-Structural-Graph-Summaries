import argparse
import configparser
import site
import sys
import re 
site.addsitedir('../lib')  # Always appends to end
from rdflib import Literal

from graph_summary_generator import summary as gsg

import pathlib
import gzip

#Creates graph structure for a view of the Source Code Graphs
def code(part, number):
    fr = open("Files/rfiles"+str(number)+".txt")
    print("rfiles"+str(number)+".txt")
    files = fr.read()
    files = files.replace(".R\n","."+part+".nq.gz\n")
    files = files.split("\n")
    done = open("Files/done-"+part+"-"+str(number)+".txt","w+")
    i = 0
    allI = len(files)
    files[-1] = files[-1][:-2]+"."+part+".nq.gz"
    for file in files:
        i += 1

        print(str((i/allI)*100),"%")
        f = gzip.open("../data/"+file)
        fname = file.split("/")[-1].replace("."+part+".nq.gz",".R")
        fname2 = file.split("/")[-1].replace("."+part+".nq.gz","")
        done.write(file+"\n")
        done.flush()
        print(fname)
        print(file)
        print(fname2)
        lines =  f.read().decode("utf-8")
                        
        gs = gsg.graph_for_summary( )
      
        gs.create_graph_information(file.replace(".nq.gz",""),lines)

        gs.save("../data/Better/"+file.replace(".nq.gz",""))
    
    done.close()
    
    
class DevNull:
    def write(self, msg):
        pass
        
#Creates graph structure for News-Knowledge-Graphs   
def news():
    sys.stderr = DevNull()# No error print for xml formats
    newsL = ["Al-Jazeera","CNN","euronews"]
    topics = ["CERN",        "Facebook",   "NFL",          "Obesity",              "Twitter",  "Cigarettes",   "FIFA",       "Nintendo",     "StanfordUniversity",   "WarnerBros",  "Disney",       "NBA",        "NobelPrize",   "TikTok", "WorldHealthOrganization"]
    for topic in topics:
        for news in newsL:
            print(topic+"-"+news+".nq")
            f = open("../data/NewsQuads/"+topic+"/"+topic+"-"+news+".nq","r")
            lines = f.read()
            for i in range(10):
                lines =  lines.replace("<"+topic+"-"+news+"-"+str(i)+">","")
            f.close()
            gs = gsg.graph_for_summary( )
            gs.create_graph_information(topic+"-"+news,lines)
            gs.save("../data/NewsQuads/"+topic+"/"+topic+"-"+news)

#Creates graph structure for a part of Wikidata      
def wikidata(i):
    sys.stderr = DevNull()# No error print for xml formats

    print("btc2019-wikidata.org"+str(i))
    f = open("../data/wikidata/btc2019-wikidata.org"+str(i)+".nq","r")
    lines = f.read()
    f.close()
    gs = gsg.graph_for_summary( )
    gs.create_graph_information("btc2019-wikidata.org"+str(i),lines)
    gs.save("../data/wikidata/btc2019-wikidata.org"+str(i))
 
#Creates graph structure for BTC 2019 without Wikidata        
def btc2019():
    fr = open("Files/files.txt")
    files = fr.read()
    files = files.replace(".nq",".nq.gz")
    files = files.split("\n")[1:]

    for file in files:
        print(file)
        f = gzip.open("../data/BTC2019/"+file)
        lines =  f.read().decode("utf-8")
        f.close()
        gs = gsg.graph_for_summary( )
        gs.create_graph_information(file.replace(".nq.gz",""),lines)
        gs.save("../data/BTC2019/"+file.replace(".nq.gz",""))



def main():
    args = sys.argv
    #Which dataset should be used?
    dataset = int(args[1])
    part = 0
    if dataset == 5 or dataset == 2 or dataset == 3 or dataset == 4   :
        part = int(args[2])
    
    if dataset == 1:
        news()
    if dataset == 2:
        code("dfg",part)
    if dataset == 3:
        code("cfg",part)
    if dataset == 4:
        code("normalize",part)
    if dataset == 5:
        wikidata(part)
    if dataset == 6:
        btc2019()
    
    
    
if __name__ == "__main__":
    main()
