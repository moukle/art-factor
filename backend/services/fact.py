import ontologyAPI.ontology_api as ontologyAPI
import nlp_sentbuilder.sentbuilder as nlp
from services.answer import get_true_ratio_for_user

import json

def statement(truth, lies):
    statement = [truth]
    statement.extend(lies)
    return statement

def fact(triple, factTrue=True):
    u = triple["subj"]["value"]
    s = triple["label"]["value"]
    p = triple["predicate"]["value"]
    o = triple["obj"]["value"]
    sentence = nlp.generate_sentence(s, p, o)

    fact = { 
        "Fact": {
            "resource": u,
            "subject": s,
            "predicate": p,
            "object": o,
            "sentence": sentence,
            "factTrue": factTrue
        }
    }
    return fact

def get_facts_for_user(userID, subjects=[]):
    truth = fact(ontologyAPI.get_fact(True, subjects), True)

    lies = []
    lies.append(fact(ontologyAPI.get_fact(False, subjects), False))

    ratio = get_true_ratio_for_user(userID)
    if ratio >= 0.2:
        lies.append(fact(ontologyAPI.get_fact(False, subjects), False))
    if ratio >= 0.8:
        lies.append(fact(ontologyAPI.get_fact(False, subjects), False))

    return statement(truth, lies)