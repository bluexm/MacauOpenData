###############################################################################
# This scripts reads a pdf of most costly works in Macau, tries to guess the 
# address of the work location, and outputs a file .csv file for upload to 
# Google Maps.
# the pdf is read with camelot, and addresses are red using google maps API
#
# July 2021: Xavier Mathieu, initial version 
###############################################################################

import csv
import json
from os import chdir
import camelot 
import pandas as pd 

import googlemaps
from datetime import datetime

chdir('./scraper/pdfscraper')

# enter your API key for google maps in the file apikey_googlemaps.txt
with open('apikey_googlemaps.txt') as f:
    gmapkey=f.readline()[:-1]
    f.close()

fname = "obrasover100m.pdf" 

# reads document with camelot 
tables= camelot.read_pdf(fname, pages='1,2')    #, flavor='stream', strip_text='\r')
tables[0].df.to_csv("ob1001.csv")
tables[1].df.to_csv("ob1002.csv")

#merge into one single dataframe
completed_tbl= tables[0].df.append(tables[1].df.iloc[2:-5],ignore_index=True)
completed_tbl=completed_tbl.iloc[2:]
completed_tbl['google address']=''
completed_tbl['lon']=0
completed_tbl['lat']=0

# find the adresses with google API 
gmaps = googlemaps.Client(key=gmapkey)
for i in range(len(completed_tbl)):
    try:
        desc_pt =  ' '.join(completed_tbl.iloc[i][2].split('\n')[1:])
        desc_cn = completed_tbl.iloc[i][2].split('\n')[0]  # we use the chinese characters to find the address, nore likely to be correct for Macau 
        #print(desc_pt)
        geocode_result = gmaps.geocode(desc_cn)
        #print( "--> GOOGLE ADDRESS" , geocode_result[0]['formatted_address'],geocode_result[0]['geometry']['location']['lng'])
        #pprint.pprint(geocode_result)
        completed_tbl.at[i,'google address']=geocode_result[0]['formatted_address']
        completed_tbl.at[i,'lon']= geocode_result[0]['geometry']['location']['lng']  
        completed_tbl.at[i,'lat']= geocode_result[0]['geometry']['location']['lat'] 
    except: 
        print('failed for '+desc_pt)
        pass

googlecsv= pd.DataFrame(columns=['lon','lat','name','address'])
googlecsv['lon']=completed_tbl.iloc[1:]['lon']
googlecsv['lat']=completed_tbl.iloc[1:]['lat']
googlecsv['address']=completed_tbl.iloc[1:]['google address']
googlecsv['name']=completed_tbl.iloc[1:][2]
googlecsv['Amnount']=completed_tbl.iloc[1:][3]
googlecsv.to_csv('import_googlemaps.csv', index=False)