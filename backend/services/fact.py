import ontologyAPI.ontology_api as ontologyAPI
import json

def statement(t1, f1, f2):
    statement = [ t1, f1, f2 ]
    return statement

def fact(triple, factTrue=True):
    u = triple["subj"]["value"]
    s = triple["label"]["value"]
    p = triple["predicate"]["value"]
    o = triple["obj"]["value"]
    fact = { 
        "Fact": {
            "resource": u,
            "subject": s,
            "predicate": p,
            "object": o,
            "factTrue": factTrue
        }
    }
    return fact

def read_true_false_false(subjects=[]):
    truth = fact(ontologyAPI.get_fact(True, subjects), True)
    lie_1 = fact(ontologyAPI.get_fact(False, subjects), False)
    lie_2 = fact(ontologyAPI.get_fact(False, subjects), False)

    return statement(truth, lie_1, lie_2)