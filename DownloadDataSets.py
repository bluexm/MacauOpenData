
import http.client
conn = http.client.HTTPSConnection(“dst.apigateway.data.gov.mo”)
payload = ‘’
headers = {
  ‘Authorization’: ‘APPCODE 09d43a591fba407fb862412970667de4’
}
conn.request(“GET”, “/dst_bars”, payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode(“utf-8"))

