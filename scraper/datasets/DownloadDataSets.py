import http.client
from os import RTLD_NOW, write, chdir
import pandas as pd 
import json 
import re 

def download(conn,headers,strext):
  """
  Builds GET request with specific header (containing for example API key and value) 
  """
    payload = ''
    conn.request("GET", "/"+strext, payload, headers)    
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def test_download():
    """
    unit test for download function
    """
    conn = http.client.HTTPSConnection("dst.apigateway.data.gov.mo")
    payload = ''
    headers = {
        'Authorization': 'APPCODE 09d43a591fba407fb862412970667de4'
    }
    conn.request("GET", "/dst_bars", payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))
    print(download(conn,headers,"dst_bars"))




"""
Script for download of all data sets attainable through API 
"""
chdir('scraper')
dfmeta=pd.read_csv('../resources/dataframe_t.csv',header = 0)

for i,row in dfmeta.iterrows():

    #row = dfmeta.iloc[1]
    if row['API url']!=row['API url']: #nan in API address
        #TBD : use the link on down arrow button ...  not the API 
        pass 
    else:
        fname= '../resources/data/' + re.sub("/","_",row['dataset_name_en'])+"."+row['Data Format']
        strtmp = row['API url'].split('data.gov.mo/')
        strext=strtmp[-1]
        url = row['API url'].split('/')[2]
        conn = http.client.HTTPSConnection(url)
        payload = ''
        headers = { row['api_key']:row['api_val']    }

        data = download(conn,headers,strext)

        with open(fname, 'w+') as obj:
            obj.write(data)
            obj.close

#write graph of nodes 
#TBD
