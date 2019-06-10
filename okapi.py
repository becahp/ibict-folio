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
for i in listaErros:
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
        print(i)
        #listaErros.append(i)

#listaErros
#[22, 28, 33, 53, 55, 61, 239, 343, 347, 366, 401, 409, 564, 605, 647]



>>> r = requests.post(url, headers=headers, params=params, data=data)
>>> r.text
'{\n  "responseHeader":{\n    "status":0,\n    "QTime":24}}\n'
>>> exit()

if len(folioReg['contributors'])
    folioReg['contributors'][0]['name'] = ''
folioReg['contributors'][0]['name']
folioReg['publication'][0]['publisher']
folioReg['publication'][0]['dateOfPublication']

if len(folioReg['publication']): #diferente de zero

else:
   auxPublisher = []
   auxDateOfPublication = []


    if 'publisher' in folioReg['publication'][0]:
        auxPublisher = folioReg['publication'][0]['publisher']
    else:
        auxPublisher = []
if 'dateOfPublication' in folioReg['publication'][0]:
    auxDateOfPublication = folioReg['publication'][0]['dateOfPublication']
else:
    auxDateOfPublication = []

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
url = 'http://localhost:8080/solr/biblio/update'
params ={'commit': 'true', 'json.command': 'false'}
headers = {'Content-type': 'application/json'}
data=solrJson
r = requests.post(url, headers=headers, params=params, data=data)
r.text
response = r.json()

data = '[{
    "id": "in00002182",
    "title": "O Contrapoder popular /",
    "title_alt": [],
    "edition": [],
    "series": [],
    "author": "Pereira, Cristóvão",
    "topic": [
        "Ética",
        "Ciência política",
        "Cristianismo"
    ],
    "publisher": "Perffil Editora, ",
    "publishDate": "2005.",
    "language": [
        "por "
    ],
    "recordtype": "MARC-JSON"
}]'

data=open('example.file', 'rb')
curl -X POST -H 'Content-Type: application/json' 'http://localhost:8080/solr/biblio/update?commit=true' --data-binary '[{
    "id": "in00002182",
    "title": "O Contrapoder popular /",
    "title_alt": [],
    "edition": [],
    "series": [],
    "author": "Pereira, Cristóvão",
    "topic": [
        "Ética",
        "Ciência política",
        "Cristianismo"
    ],
    "publisher": "Perffil Editora, ",
    "publishDate": "2005.",
    "language": [
        "por "
    ],
    "recordtype": "MARC-JSON"
}]'

solrJson = json.dumps(solrReg, ensure_ascii=False, indent=4)
data=solrJson.encode('utf8')
