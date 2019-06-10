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
r = requests.post(url, headers=headers, data=json.dumps(payload))
token = r.headers['x-okapi-token']
print(token)

#----------------------------------------------------------------
#Pegar uma instancia para saber quantas tem ao todo
url = 'http://localhost:9130/instance-storage/instances'
params = {'limit':'1'}
payload = {"username":"diku_admin","password":"admin"}
headers = {'Content-type': 'application/json', "Accept": "application/json", "X-Okapi-Tenant": "diku", "X-Okapi-Token": token}
r = requests.get(url, headers=headers, params=params, data=json.dumps(payload), )
response = r.json()
#total = response['totalRecords']
total = 1

#----------------------------------------------------------------
#Converter para solr

folioReg = data['instances'][0] #apenas para 1
solrReg = {
    'id': folioReg['hrid'],
    'title': folioReg['title'],
    'title_alt': folioReg['alternativeTitles'],
    'edition': folioReg['editions'],
    'series': folioReg['series'],
    'author': folioReg['contributors'][0]['name'],
    'topic': folioReg['subjects'],
    'publisher': folioReg['publication'][0]['publisher'],
    'publishDate': folioReg['publication'][0]['dateOfPublication'],
    'language': folioReg['languages']
    }

solrJson = json.dumps(solrReg, ensure_ascii=False, indent=4, sort_keys=True)

#----------------------------------------------------------------
#Enviar para solr

#Pegar uma instancia para saber quantas tem ao todo
#Necessário 'json.command': 'false'
url = 'http://localhost:8080/solr/biblio/update'
params ={'commit': 'true', 'json.command': 'false'}
headers = {'Content-type': 'application/json'}
data=solrJson
r = requests.post(url, headers=headers, params=params, data=data)
r.text
