import pickle
import os.path as osp

import site
import sys
import gzip
site.addsitedir('../../lib')  # Always appends to end
import validators

import timeit
import re
import pathlib
#disable randomization of hash
#former group used randomized hash
import os
import sys
hashseed = os.getenv('PYTHONHASHSEED')
if not hashseed:
  os.environ['PYTHONHASHSEED'] = '0'
  os.execv(sys.executable, [sys.executable] + sys.argv)

import rdflib
import rdflib.parser as rdflib_parser
import rdflib.plugins.parsers.ntriples as triples
import rdflib.plugins.parsers.nquads as quads

#disable randomization of hash
import os
import sys
hashseed = os.getenv('PYTHONHASHSEED')
if not hashseed:
  os.environ['PYTHONHASHSEED'] = '0'
  os.execv(sys.executable, [sys.executable] + sys.argv)

#For BTC19
def manageBNode_(line):    
    """
    This function replaces all blanknodes in the line with a handmade IRI (prepend 'https://blanknode/', delete the '_:' and append '>')

    
    Args:
        line (str): Line to manage
    """
    line = re.sub('( |^)_:', '\g<1><https://blanknode/', line)
    line = re.sub("(( |^)[^@ ]*[^^,>\" ]) ", "\g<1>> ", line)
    
    return line


class summaries():
        
    def __init__(self):
        self.summary = ""
        self.eqcs = {} # key: vertex name, value: hash of its EQCs
        self.eqcsI = {}  # key: hash value: eqcs object
        
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

class eqcs():
    """
    first all vertices then the eqcs are created for statisitics
    """

    def __init__(self, s, ps,ts):
        self.members = set()
        self.members.add(s)
        self.edgesP = ps
        self.edgesT = ts


class graph_for_summary():
    """
    A class used to calculate graph summaries
    """

    def __init__(self):
        name = ""

        # vertex
        self.verticesI = {} #edges of a vertex
        self.vertices = set()
        self.seen_vertices = set()
        self.edgesL = set()


    
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


    def create_graph_information(self,name, lines):

        self.name = name
        lines = lines.split('\n')
        number_lines =  len(lines)
        
        print("Files has", number_lines,"lines.")
        
        count_line = 0
        count_invalid = 0
        ignoreNo = 0
        parseq = quads.NQuadsParser()
        sink = rdflib.ConjunctiveGraph()

        for line in lines:
            if not line:
                break
            quotationSplitLine = re.split(r'(?<!\\)\"', line) #(negative lookbehind regex in order to respect escaped " in literals)
            if '_:' in line:
                if(len(quotationSplitLine) == 1): #no literal as object in line
                    line = manageBNode_(line)
                elif (len(quotationSplitLine) == 3): #literal as object in line
                    line = ''
                    for j in range(0, len(quotationSplitLine)):
                        if(j%2 == 1): #literals
                            line = line + '"' + quotationSplitLine[j] + '"'
                        else: #non-literals
                            line = line + manageBNode_(quotationSplitLine[j])
                #else:
                   # ignoreNo += 1
                    #print('Ignored Line Number ' + str(f'{ignoreNo:,}') + ': ' + line)
                    #line = ''
            #print(line)
            #print()
            if not line:
                break
            count_line += 1
            if count_line % 10000 == 0:
                print("Read line", count_line, "of", number_lines, "(", count_line / number_lines * 100.0, "%)")

            sink = rdflib.ConjunctiveGraph()
            # parseq
            strSource = rdflib_parser.StringInputSource(line.encode('utf-8'))

            try:
                # try parsing the line to a valid N-Quad
                parseq.parse(strSource, sink)
                # write the validated N-Quad into the filtered File

                # print( list(sink.subjects()),list(sink.predicates()),list(sink.objects() ) )
                s = str(list(sink.subjects())[0])
                p = str(list(sink.predicates())[0])
                o = str(list(sink.objects())[0])  
                
                self.edgesL.add(p)
                
                
                if validators.url(o): 
                    self.seen_vertices.add(o)
                    #print(o)
                self.vertices.add(s)
                if s in self.verticesI:
                    self.verticesI[s].append((p,o))
                else:
                    self.verticesI[s] = [(p,o)]
                



            except triples.ParseError:
                # catch ParseErrors 
                count_invalid += 1

                # print the number of Errors and current trashed line to console
                print('Wrong Line Number ' + str(f'{count_invalid:,}') + ': ' + line)


        print("lines read:", count_line)
        print("invalid lines read:", count_invalid)

        

    def calculate_graph_summary(self,gs):
        """
        Calculate the by the index defined graph summary on the prepared data
        """
        # 2. create graph summary over whole graph
        # go through graph information and calculate labels and features
        if (gs == 1):
            return self.attribute_based_collection_impl()
        elif (gs == 2):
            return self.class_based_collection_impl()
        elif (gs == 3):
            return self.property_type_collection_impl()


    def attribute_based_collection_impl(self):
        """
        Implementation to calculate the attribute based collection

        """
        return self.based_collection_impl(True, False)

    def class_based_collection_impl(self):
        """
        Implementation to calculate the class based collection

        """
        return self.based_collection_impl(False, True)

    def property_type_collection_impl(self):
        """
        Implementation to calculate the property type collection


        """
        return self.based_collection_impl(True, True)


    def is_rdf_type(self, s):
        """
        Check if the given string contains rdf and therefore is an rdf-type


        Args:
            s (str): Feature used by the graph summary model

        Returns:
            bool: If it is a rdf-type
        """
        return "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" in s or "https://uni-ulm.de/r-ast/type" in s
        

    def based_collection_impl(self, prop, typ):
        """
        Base implementation for the graph summary calculation


        Args:
            prop (bool): If we want to use the property sets
            typ (bool): If we want to use the type sets
        """
        summary = summaries()
        if prop == True and typ == False:
            summary.summary = "AC"
        if prop == False  and typ == True:
            summary.summary = "CC"
        if prop == True and typ == True:
            summary.summary = "ACC"
        
        # iterate through all subjects
        for v in self.vertices:
            # calculate hash
            tmp_feature_list = []
            tmp_property_list = []
            tmp_type_list = []
            # go through edges of gi
            for h in self.verticesI[v]:
                
                # check if we want to use the feature in this config
                if (prop == True and self.is_rdf_type(h[0]) == False and h[0] not in tmp_property_list):
                    tmp_feature_list.append(h[0])
                    tmp_property_list.append(h[0])
                    	

                if (typ == True and self.is_rdf_type(h[0]) == True and h[1] not in tmp_type_list):
                    tmp_feature_list.append(h[1])
                    tmp_type_list.append(h[1])



            tmp_feature_list.sort()
            tmp_feature_list_string = "".join(tmp_feature_list)
            tmp_hash = hash(tmp_feature_list_string)


            summary.eqcs[v] = tmp_hash
            if tmp_hash in summary.eqcsI:
                summary.eqcsI[tmp_hash].members.add(v)
            else:
                summary.eqcsI[tmp_hash] = eqcs(v,tmp_property_list,tmp_type_list)
        
        tmp_hash = hash("")    
        for v in self.seen_vertices - self.vertices:
            summary.eqcs[v] = tmp_hash
            if tmp_hash in summary.eqcsI:
                summary.eqcsI[tmp_hash].members.add(v)
            else:
                summary.eqcsI[tmp_hash] = eqcs(v,[],[])
        
        return summary
    
class summarySet():
        
    def __init__(self):
        self.vertices = set()
        self.payload = set()
        self.edgesV = set()
        self.edgesB = set()
        self.edgesVB = set()
        
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
      
    def get_summary(self, summary):

        for k in summary.eqcsI.keys():
            self.vertices.add("hash:"+str(k))
            #print("hash:"+str(k))
            self.payload.add("payload:"+str(k))
            #print("payload:"+str(k))
            self.edgesVB.add(("hash:"+str(k),"https://uni-ulm.de/payload","payload:"+str(k)))
            
            for ps in summary.eqcsI[k].edgesP:
                #print(ps)
                self.edgesV.add(("hash:"+str(k),ps,"\"\""))
            #print("type")    
            
            for ts in summary.eqcsI[k].edgesT:
                self.edgesV.add(("hash:"+str(k),"http://www.w3.org/1999/02/22-rdf-syntax-ns#type",ts))
                self.vertices.add(ts)
                #print(ts)
                
            for m in summary.eqcsI[k].members:
                self.payload.add(m)
                self.edgesB.add(("payload:"+str(k),"https://uni-ulm.de/member",m))
                #print(m)
                
    def to_triples(self,summary):
        nt = ""
        for (s,p,o) in self.edgesV:
            if o != "\"\"":
                nt += "<"+s+"> "+"<"+p+"> "+"<"+o+"> .\n"
            else:
                nt += "<"+s+"> "+"<"+p+"> "+o+" .\n"
                
        for (s,p,o) in self.edgesVB:
            nt += "<"+s+"> "+"<"+p+"> "+"<"+o+"> .\n"
        for (s,p,o) in self.edgesB:
            nt += "<"+s+"> "+"<"+p+"> "+"<"+o+"> .\n"
        f = gzip.open(summary+".nt.gz","w+")
        f.write(nt.encode('utf-8'))
        f.close()
            
            
            
