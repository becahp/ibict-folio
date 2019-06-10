import requests
import json

#example
#url = 'https://api.github.com/some/endpoint'
#payload = {'some': 'data'}
#headers = {'content-type': 'application/json'}
#r = requests.post(url, data=json.dumps(payload), headers=headers)

okapi = https://folio-snapshot-core-okapi.aws.indexdata.com

#----------------------------------------------------------------
#Pegar Okapi-token
url = okapi + '/authn/login'
payload = {"username":"diku_admin","password":"admin"}
headers = {'Content-type': 'application/json', "Accept": "application/json", "X-Okapi-Tenant": "diku"} #-H "Content-type: application/json" -H "Accept: application/json" -H "X-Okapi-Tenant: diku"
r = requests.post(url, data=json.dumps(payload), headers=headers)
token = r.headers['x-okapi-token']
#print(token)

#----------------------------------------------------------------
#Pegar uma instancia para saber quantas tem ao todo
url = okapi + '/instance-storage/instances'
params = {'limit':'1'}
payload = {"username":"diku_admin","password":"admin"}
headers = {'Content-type': 'application/json', "Accept": "application/json", "X-Okapi-Tenant": "diku", "X-Okapi-Token": token}
r = requests.get(url, headers=headers, params=params, data=json.dumps(payload))
response = r.json()
total = response['totalRecords']

#----------------------------------------------------------------
#Pegar todas as instancias
url = okapi + '/instance-storage/instances'
params = {'limit':total}
payload = {"username":"diku_admin","password":"admin"}
headers = {'Content-type': 'application/json', "Accept": "application/json", "X-Okapi-Tenant": "diku", "X-Okapi-Token": token}
r = requests.get(url, headers=headers, params=params, data=json.dumps(payload)) #estou com jsonGrande
dados = r.json() #tenho um dicionario com totalRecords e instances

##verificar tamanho de dados
#len(dados['instances'])

##salvar??
with open('folio-snapshot.json', "w") as file_write:
    json.dump(dados, file_write, ensure_ascii=False, indent=4)
