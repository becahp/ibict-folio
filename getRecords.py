import requests
import json

#example
#url = 'https://api.github.com/some/endpoint'
#payload = {'some': 'data'}
#headers = {'content-type': 'application/json'}
#r = requests.post(url, data=json.dumps(payload), headers=headers)

#----------------------------------------------------------------
#Pegar Okapi-token
url = 'http://localhost:9130/authn/login'
payload = {"username":"diku_admin","password":"admin"}
headers = {'Content-type': 'application/json', "Accept": "application/json", "X-Okapi-Tenant": "diku"} #-H "Content-type: application/json" -H "Accept: application/json" -H "X-Okapi-Tenant: diku"
r = requests.post(url, data=json.dumps(payload), headers=headers)
token = r.headers['x-okapi-token']
#print(token)

#----------------------------------------------------------------
#Pegar uma instancia para saber quantas tem ao todo
url = 'http://localhost:9130/instance-storage/instances?limit=1'
payload = {"username":"diku_admin","password":"admin"}
headers = {'Content-type': 'application/json', "Accept": "application/json", "X-Okapi-Tenant": "diku", "X-Okapi-Token": token}
r = requests.get(url, data=json.dumps(payload), headers=headers)
response = r.json()
total = response['totalRecords']

#----------------------------------------------------------------
#Pegar todas as instancias
url = 'http://localhost:9130/instance-storage/instances?limit='+str(total)
payload = {"username":"diku_admin","password":"admin"}
headers = {'Content-type': 'application/json', "Accept": "application/json", "X-Okapi-Tenant": "diku", "X-Okapi-Token": token}
r = requests.get(url, data=json.dumps(payload), headers=headers) #estou com jsonGrande
data = r.json() #tenho um dicionario com totalRecords e instances

##salvar??
with open('records.json', "w") as file_write:
    json.dump(data, file_write, ensure_ascii=False, indent=4)
