import rdflib

def load_ontology():
    ONTOLOGY_PATH = "ontologies/ArtOntology.ttl"
    print("Loading ArtOntology..")
    graph = rdflib.Graph()
    graph.parse(location=ONTOLOGY_PATH, format="n3")
    print("Finished loading ArtOntology")
    return graph

ontology = load_ontology()

def get_random_triple():
    res = ontology.query("""
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

    for row in res:
        return row
