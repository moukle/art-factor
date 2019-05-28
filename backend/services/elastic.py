from elasticSearch.elasticSearch_api import search_persons

def search(fuzzy):
    eleasticResponse = search_persons(fuzzy)
    return buildJson(eleasticResponse)

def buildJson(eleasticResponse):
    responseJson = []
    for p in eleasticResponse['hits']['hits']:
        _class =  p['_type']

        _source =  p['_source']
        _label = _source['name']
        _uri = _source['uri']

        responseJson.append({'class': _class, 'label': _label, 'uri': _uri})
    return responseJson