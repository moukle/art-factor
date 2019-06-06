import random
from SPARQLWrapper import SPARQLWrapper, JSON


def query(body):
    fuseki_url = "http://localhost:3030/artontology/sparql"
    sparql = SPARQLWrapper(fuseki_url)
    sparql.setQuery(body)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return result["results"]["bindings"]


def get_fact(trueFact, subjects):
    if subjects:
        subj = random.choice(subjects)
    else:
<<<<<<< HEAD
        while(True):
            true_row = get_data_on_ressource()
            #print(subject)
            while str(true_row) == "":
                true_row = get_data_on_ressource()
            #true_row = get_data_on_ressource(subject)
            alternate_row = get_data_on_ressource()
            while str(alternate_row) == "":
                alternate_row = get_data_on_ressource()
            #dont mix same elements
            if true_row[0] == alternate_row[0]:
                print(true_row)
                print(alternate_row)
                print(1)
                continue
            #lies arent lies if the object doesnt change
            if true_row[-1] == alternate_row[-1]:
                print(2)
                continue
            #kinda basic and not very extendable
            alternate_row = alternate_row[2:4]
            true_row = true_row[0:2]
            #print(true_row)
            #print(alternate_row)
            s = true_row + alternate_row
            #print(s)
            return s


def get_data_on_ressource(ressource=''):
    if ressource == '':
        #no ressource to get data on. Retrieve data from a random person
        ressource = get_person()
        print(ressource)
        for row in ressource:
            random_person = "wd:" + str.format(row[0]).split('/')[-1]
=======
        import elasticSearch.elasticSearch_api as es
        subj = es.random_uri()
    subj = "wd:" + str.format(subj).split('/')[-1]

    if trueFact:
        return get_true_fact(subj)
>>>>>>> QuerysOnFuseki
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