from ontologyAPI.api import get_random_triple

def fact(s, o, factTrue=True):
    fact = { 
        "Fact": {
            "fact": str(s+o),
            "factTrue": factTrue
        }
    }
    return fact

def read_random_true():
    s, o = get_random_triple()
    return fact(s, o, True)