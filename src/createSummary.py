import argparse
import configparser
import site
import sys
import re 
site.addsitedir('../lib')  # Always appends to end


from graph_summary_generator import summary as gsg

import pathlib
import gzip

#Creates summary structure for a view of the Source Code Graphs    
def code(part,typeS, number):
    fr = open("Files/rfiles"+str(number)+".txt")
    print("rfiles"+str(number)+".txt")
    files = fr.read()
    files = files.replace(".R\n","."+part+".nq.gz\n")
    files = files.split("\n")
    fr.close()
    i = 0
    allI = len(files)
    files[-1] = files[-1][:-2]+"."+part+".nq.gz"
    for file in files:
        i += 1

        print(str((i/allI)*100),"%")
        gs = gsg.graph_for_summary( )
 
        gs.load("../data/"+file.replace(".nq.gz",""))
        
        summary = gs.calculate_graph_summary(typeS)
        typeN = "X"
        if (typeS == 1):
            typeN = "AC"
        elif (typeS == 2):
            typeN = "CC"
        elif (typeS == 3):
            typeN = "ACC"
            
        summary.save("../data/"+file.replace(".nq.gz",typeN))
    
    
class DevNull:
    def write(self, msg):
        pass
        
#Creates summary structure for News-Knowledge-Graphs  
def news(typeS):
    sys.stderr = DevNull()# No error print for xml formats
    newsL = ["Al-Jazeera","CNN","euronews"]
    topics = ["CERN",        "Facebook",   "NFL",          "Obesity",              "Twitter",  "Cigarettes",   "FIFA",       "Nintendo",     "StanfordUniversity",   "WarnerBros",  "Disney",       "NBA",        "NobelPrize",   "TikTok", "WorldHealthOrganization"]
    for topic in topics:
        for news in newsL:
            print(topic+"-"+news+".nq")
            gs = gsg.graph_for_summary( )

            gs.load("../data/NewsQuads/"+topic+"/"+topic+"-"+news)
            summary = gs.calculate_graph_summary(typeS)
            typeN = "X"
            if (typeS == 1):
                typeN = "AC"
            elif (typeS == 2):
                typeN = "CC"
            elif (typeS == 3):
                typeN = "ACC"

            summary.save("../data/NewsQuads/"+topic+"/"+topic+"-"+news+typeN)

#Creates summary structure for Wikidata
def wikidata(typeS):
    sys.stderr = DevNull()# No error print for xml formats
    for i in range(67):
        print("btc2019-wikidata.org"+str(i))
        #print(lines)
        gs = gsg.graph_for_summary( )
        gs.load("../data/wikidata/btc2019-wikidata.org"+str(i))
        summary = gs.calculate_graph_summary(typeS)
        typeN = "X"
        if (typeS == 1):
            typeN = "AC"
        elif (typeS == 2):
            typeN = "CC"
        elif (typeS == 3):
            typeN = "ACC"

        summary.save("../data/wikidata/btc2019-wikidata.org"+str(i)+typeN)
    
          
#Creates summary structure for BTC 2019 without Wikidata
def btc2019(typeS):
    fr = open("Files/files.txt")
    files = fr.read()
    files = files.replace(".nq",".nq.gz")
    files = files.split("\n")[1:]

    for file in files:
        print(file)
        gs = gsg.graph_for_summary( )

        gs.load("../data/BTC2019/"+file.replace(".nq.gz",""))
        summary = gs.calculate_graph_summary(typeS)
        typeN = "X"
        if (typeS == 1):
            typeN = "AC"
        elif (typeS == 2):
            typeN = "CC"
        elif (typeS == 3):
            typeN = "ACC"

        summary.save("../data/BTC2019/"+file.replace(".nq.gz",typeN))




def main():
    args = sys.argv
    #Which dataset should be used?
    dataset = int(args[1])
    typS = int(args[2]) #1:AC 2:CC 3:ACC
    part = 0
    if dataset == 2 or dataset == 3 or dataset == 4   :
        part = int(args[3])
    
    if dataset == 1:
        news(typS)
    if dataset == 2:
        code("dfg",typS,part)
    if dataset == 3:
        code("cfg",typS,part)
    if dataset == 4:
        code("normalize",typS, part)
    if dataset == 5:
        wikidata(typS)
    if dataset == 6:
        btc2019(typS)
    
    
    
if __name__ == "__main__":
    main()
