import http.client
from os import RTLD_NOW, write, chdir
import pandas as pd 
import json 
import re 

def download(conn,headers,strext):
    payload = ''
    conn.request("GET", "/"+strext, payload, headers)    
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def test_download():
  ##strtmp = 'htt ps://dsat.apigateway.data.gov.mo/car_park_detail'
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


chdir('scraper')
dfmeta=pd.read_csv('dataframe_translation.csv',header = 0)

for i,row in dfmeta.iterrows():

    #row = dfmeta.iloc[1]
    if row['API url']!=row['API url']: #nan in API address
        #TBD : use the link on down arrow button ...  
        pass 
    else:
      fname= './data/' + re.sub("/","_",row['dataset_name_en'])+"."+row['Data Format']
      ##strext = re.sub('data.gov.mo/\w+','\1',row['API url'])
      ##url = re.sub('https://\w+/'+strext,'\1',row['API url'])
      strtmp = row['API url'].split('data.gov.mo/')
      strext=strtmp[-1]
      url = row['API url'].split('/')[2] ##re.sub("/"+ strext,"",row['API url']
      conn = http.client.HTTPSConnection(url)
      payload = ''
      headers = { row['api_key']:row['api_val']    }

      data = download(conn,headers,strext)

      with open(fname, 'w+') as obj:
          obj.write(data)
          obj.close

