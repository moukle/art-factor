import random
import requests
from SPARQLWrapper import SPARQLWrapper, JSON


def query(body):
    fuseki_url = "http://localhost:3030/artontology/sparql"
    sparql = SPARQLWrapper(fuseki_url)
    sparql.setQuery(body)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return result["results"]["bindings"]


def insert_artontology():
    print("FUSEKI :: Inserting ArtOntology in Fuseki ...")
    fuseki_url = "http://localhost:3030/"
    file = open('ontologies/ArtOntology_main.ttl', encoding='iso-8859-1')
    requests.delete(fuseki_url+'$/datasets/artontology') # delete existing dataset
    requests.post(fuseki_url+'$/datasets', data={'dbName': 'artontology', 'dbType': 'tdb'}) # create new dataset
    requests.post(fuseki_url+'artontology/data', headers={'Content-type': 'text/turtle'}, data=file ) # insert data
    print("FUSEKI :: Inserting ArtOntology finished")


def get_fact(trueFact, subjects):
    if subjects:
        subj = random.choice(subjects)
    else:
        import elasticSearch.elasticSearch_api as es
        subj = es.random_uri()
    subj = "wd:" + str.format(subj).split('/')[-1]

    if trueFact:
        return get_true_fact(subj)
    else:
        return get_false_fact(subj)


def get_false_fact(subj_1):
    filter_list = """ (rdf:type, rdfs:label, :gender, :image) """
    bind = "BIND(" + subj_1 + " AS ?subj)."

    res_random = query("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX : <http://h-da.de/fbi/artontology/>

        SELECT ?subj ?label ?predicate ?obj
        WHERE {
            {
                SELECT ?subj ?label ?subj2 WHERE { 
                    """ + bind + """
                    ?subj a ?class;
                        rdfs:label ?label.
                    ?subj2 a ?class.
                    FILTER(?subj != ?subj2).
                } ORDER BY RAND() LIMIT 1
            }
            ?subj ?predicate ?o1.
            ?subj2 ?predicate ?obj.
            FILTER(?o1 != ?obj).
            FILTER(?predicate NOT IN""" + filter_list + """).
        } ORDER BY RAND() LIMIT 1
    """)

    if res_random:
        return res_random[0]
    else:
        get_false_fact(subj_1)


def get_true_fact(subj):
    filter_list = """(rdf:type, rdfs:label, :gender, :image)"""
    bind = "BIND(" + subj + " AS ?subj)."

    res_random = query("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX : <http://h-da.de/fbi/artontology/>

        SELECT ?subj ?label ?predicate ?obj
        WHERE { 
            """ + bind + """
            ?subj a ?class;
                rdfs:label ?label;
                ?predicate ?obj.
            FILTER(?predicate NOT IN """ + filter_list + """)
        }
        ORDER BY RAND()
        LIMIT 1 
    """)

    if res_random:
        return res_random[0]
    else:
        get_true_fact(subj)


def get_all_persons():
    res_all_persons = query("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX : <http://h-da.de/fbi/artontology/>

        SELECT ?person ?name
        WHERE {
            ?person a :person;
                rdfs:label ?name.
        }
    """)
    return res_all_persons