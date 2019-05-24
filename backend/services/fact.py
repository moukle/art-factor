from ontologyAPI.api import get_random_triple

def fact(r, s, p, o, factTrue=True):
    fact = { 
        "Fact": {
            "resource": r,
            "subject": s,
            "predicate": p,
            "object": o,
            "factTrue": factTrue
        }
    }
    return fact

def read_random_true():
    r, s, p, o = get_random_triple()
    return fact(r, s, o, p, True)
