from ontologyAPI.ontology_api import get_all_persons
from elasticsearch import Elasticsearch


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Connected to Elasticsearch')
    else:
        print('Awww it could not connect!')
    return _es


def create_person_index():
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "persons": {
                "dynamic": "strict",
                "properties": {
                    "uri": {
                        "type": "text"
                    },
                    "name": {
                        "type": "text"
                    }
                }
            }
        }
    }
    # Ignore 400 means to ignore "Index Already Exist" error.
    es.indices.create(index='artontology', ignore=400, body=settings)

def store_all_persons():
    print('Storing all persons in Elasticsearch index ...')
    all_persons = get_all_persons()
    for person in all_persons:
        uri, name = person
        doc = {'uri': uri, 'name': name}
        es.index(index='artontology', doc_type='persons', body=doc)
    print("Finished Elasticsearch storing")

def search_persons(name):
    regexp = {'_source': ['uri', 'name'], 'query': { 'regexp': { 'name': '*?('+name+').*' }}}
    fuzzy = {'_source': ['uri', 'name'], 'query': { 'fuzzy': { 'name': { "value": name }}}}
    res = es.search(index='artontology', body=fuzzy)

    responseJson = []
    print(res)
    for p in res:
        print(p)
    return responseJson


es = connect_elasticsearch()
create_person_index()
store_all_persons()