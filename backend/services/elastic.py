from elasticSearch.elasticSearch_api import search_persons

def search(fuzzy):
    print(fuzzy)
    return search_persons(fuzzy)