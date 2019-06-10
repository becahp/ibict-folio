import requests
import json
from foliofunctions import folio2solr

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
r = requests.post(url, headers=headers, data=json.dumps(payload))
token = r.headers['x-okapi-token']
print(token)

#----------------------------------------------------------------
#Pegar uma instancia para saber quantas tem ao todo
url = 'http://localhost:9130/instance-storage/instances'
params = {'limit':'1'}
payload = {"username":"diku_admin","password":"admin"}
headers = {'Content-type': 'application/json', "Accept": "application/json", "X-Okapi-Tenant": "diku", "X-Okapi-Token": token}
r = requests.get(url, headers=headers, params=params, data=json.dumps(payload))
response = r.json()
total = response['totalRecords']

#----------------------------------------------------------------
#Pegar todas as instancias
url = 'http://localhost:9130/instance-storage/instances'
params = {'limit':total}
payload = {"username":"diku_admin","password":"admin"}
headers = {'Content-type': 'application/json', "Accept": "application/json", "X-Okapi-Tenant": "diku", "X-Okapi-Token": token}
r = requests.get(url, headers=headers, params=params, data=json.dumps(payload)) #estou com jsonGrande
dados = r.json() #tenho um dicionario com totalRecords e instances

##verificar tamanho de dados
#len(dados['instances'])

#----------------------------------------------------------------
#Converter para solr
url = 'http://localhost:8080/solr/biblio/update'
params ={'commit': 'true', 'json.command': 'false'}
headers = {'Content-type': 'application/json'}

listaErros = []
for i in range(len(dados['instances'])):
    folioReg = dados['instances'][i] #muda com o i
    #function folio2solr convert folioReg to solr schema
    try:
        solrReg = folio2solr(folioReg)
    except:
        print("Erro no mapeamento!")
    solrJson = json.dumps(solrReg, ensure_ascii=False, indent=4, sort_keys=True)
    data=solrJson.encode()
    print("Enviando o item " + str(i))
    r = requests.post(url, headers=headers, params=params, data=data)
    #print("Resposta " + str(r.status_code)) #str(solr['responseHeader']['status']) #solr=r.json()
    if r.status_code != 200:
        listaErros.append(i)

print(listaErros)
