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
    ##checar campos problemáticos
    #contributors
    if len(folioReg['contributors']): #diferente de zero
        auxContributors = folioReg['contributors'][0]['name']
    else:
        auxContributors = []
    #alternativeTitles
    if len(folioReg['alternativeTitles']): #diferente de zero
        auxAltTitles = folioReg['alternativeTitles'][0]['alternativeTitle']
    else:
        auxAltTitles = []
    ##publication
    if len(folioReg['publication']): #diferente de zero
        #publisher
        if 'publisher' in folioReg['publication'][0]:
            auxPublisher = folioReg['publication'][0]['publisher']
        else:
            auxPublisher = []
        #dateOfPublication
        if 'dateOfPublication' in folioReg['publication'][0]:
            auxDateOfPublication = folioReg['publication'][0]['dateOfPublication']
        else:
            auxDateOfPublication = []
    else:
        auxPublisher = []
        auxDateOfPublication = []
    #Dicionario
    solrReg = {
    'id': folioReg['hrid'],
    'title': folioReg['title'],
    'title_alt': auxAltTitles,
    'edition': folioReg['editions'],
    'series': folioReg['series'],
    'author': auxContributors, #folioReg['contributors'][0]['name'],
    'topic': folioReg['subjects'],
    'publisher': auxPublisher,
    'publishDate': auxDateOfPublication,
    'language': folioReg['languages']
    }
    solrJson = json.dumps(solrReg, ensure_ascii=False, indent=4, sort_keys=True)
    data=solrJson.encode()
    print("Enviando o item " + str(i))
    r = requests.post(url, headers=headers, params=params, data=data)
    #print("Resposta " + str(r.status_code)) #str(solr['responseHeader']['status']) #solr=r.json()
    if r.status_code != 200:
        listaErros.append(i)

print(listaErros)
