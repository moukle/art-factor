import rdflib

def load_ontology():
    ONTOLOGY_PATH = "ontologies/ArtOntology.ttl"
    print("Loading ArtOntology ...")
    graph = rdflib.Graph()
    graph.parse(location=ONTOLOGY_PATH, format="n3")
    print("Finished loading ArtOntology")
    return graph


#returns true or false statement
def get_random_triple(isTrue=True, subject=''):
    if isTrue:
        true_row = get_data_on_ressource(subject)
        return true_row
    else:
        while(True):
            true_row = get_data_on_ressource(subject)
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
    print(ressource)
    if ressource == '':
        #no ressource to get data on. Retrieve data from a random person
        ressource = get_person()
        for row in ressource:
            random_person = "wd:" + str.format(row[0]).split('/')[-1]
    else:
        random_person = "wd:" + str.format(ressource).split('/')[-1]
    print(random_person)
    filter_list = """(rdf:type, rdfs:label, :gender, :image)"""
    res = ontology.query("""
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX : <http://h-da.de/fbi/artontology/>

                SELECT *
                WHERE { 
                """ + random_person + """ ?p ?o.
                FILTER(?p NOT IN """ + filter_list + """)
                }
                ORDER BY RAND()
                LIMIT 1 

                """)
    for row in res:
        return random_person+str(row)


def get_person():
    res_random = ontology.query("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX : <http://h-da.de/fbi/artontology/>

    SELECT ?p ?n
    WHERE {
        ?p a :person;
            rdfs:label ?n.
    }
    ORDER BY RAND()
    LIMIT 1
     """)
    return res_random


def get_all_persons():
    res_all_persons = ontology.query("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX : <http://h-da.de/fbi/artontology/>

        SELECT ?p ?n
        WHERE {
            ?p a :person;
                rdfs:label ?n.
        }
    """)
    return res_all_persons


ontology = load_ontology()