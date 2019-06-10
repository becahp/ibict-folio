#!/usr/bin/python

# Function definition is here
def folio2solr(folioReg):
    #folioReg is the dictonary

    ##Checar campos problematicos
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

    #Mapping
    solrReg = {
    'id': folioReg['hrid'],
    'title': folioReg['title'],
    'title_alt': auxAltTitles,
    'edition': folioReg['editions'],
    'series': folioReg['series'],
    'author': auxContributors, #folioReg['contributors'][0]['name'],
    'topic': folioReg['subjects'],
    'publisher': auxContributors,
    'publishDate': auxDateOfPublication,
    'language': folioReg['languages']
    }

    return solrReg;
