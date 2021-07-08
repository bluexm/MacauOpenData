import http.client
from os import RTLD_NOW, chdir
import pandas as pd 
import json 
import re 
from csv import QUOTE_NONNUMERIC

"""
Script to build a graph where nodes are datasets connected if they have one field name in common.
The fields of each dataset are read from the file dataframe_translation.csv
The results are saved in 2 files graphEdges.csv and graphNodes.csv to be used in Gephi 
"""

chdir('analysis')
dfmeta=pd.read_csv('../resources/dataframe_t.csv',header = 0)
fname_edges= '../analysis/graphEdges.csv'
fname_nodes= '../analysis/graphNodes.csv'
dfedges = pd.DataFrame(columns= ['Source','Target','Type','Id','Label',	'timeset','Weight'])
dfnodes = pd.DataFrame(columns= ['Id','Label'])
lnodes = []

lignore=["[]","['']","[' ,']"]
idxnode=0
for i,row in dfmeta.iterrows(): # store datasets columns in a list 
    tmpdesc = row['Field Description (English)']
    if tmpdesc==tmpdesc: #not nan
        #print("original",tmpdesc)
        tmpdesc= re.sub("'-*'(,\s'-*')*","",tmpdesc)
        if tmpdesc not in lignore:
            #print(tmpdesc)
            lnodes.append({'name':row['dataset_name_en'], 'id':i, 'cols':set(tmpdesc[2:-2].split("', '"))})
            dfnodes = dfnodes.append({'Id':idxnode,'Label':row['dataset_name_en']}, ignore_index=True)
            idxnode+=1
dfnodes.to_csv(fname_nodes,index=False, quotechar='"', quoting=QUOTE_NONNUMERIC, mode='a') 

for i in range(len(lnodes)-1): # look at common nodes (columns names)
    print('--------->>> checking <<<<<------------ ', lnodes[i]['cols'])
    for j in range(i+1,len(lnodes)): 
        #print(lnodes[j]['cols'])
        cfields =lnodes[i]['cols'].intersection(lnodes[j]['cols']) #common fields
        w = len(cfields)
        if w>0:
            #print("{} edges".format(w))
            #print(lnodes[j]['cols'])
            dfedges = dfedges.append({'Source':lnodes[i]['id'],'Target':lnodes[j]['id'],
                'Type':'Directed','Id':len(dfedges)+1,'Label':lnodes[i]['name']+lnodes[j]['name'],
                'timeset':'','Weight':1}, ignore_index=True)
dfedges.to_csv(fname_edges,index=False, quotechar='"', quoting=QUOTE_NONNUMERIC) 

print("finished, found {} nodes and {} edges".format(len(dfnodes),len(dfedges)))
