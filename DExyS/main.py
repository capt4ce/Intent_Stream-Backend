from . import ontology
from . import sparql
from . import worker

# search function accept a tuple that contains (keyword,weight)
# it will return:
#   destination search result
#   additional few highest keywords
# have an option to return all other keywords


# the query string is matched with the dictionary first to get a proper word
def querySearch(queryStr, start=0, limit=0):
    queries=queryStr.split(' ')

    # matching with dictionary
    # queries = []
    keywords = {}
    for key in queries:
        keywords[key] = 1

    destinations = sparql.searchMatchingDestination(queries)
    result = processDestinations(destinations, keywords, start, limit)
    # result = sparql.searchWithQuery(queryStr)
    
    return result

# the keywords are collected and directly used in the further processing
def keywordSearch(keywords, start, limit):
    # keywords = []
    # for key in keywords:
    #     keywords.append(key)
    destinations = sparql.searchMatchingDestination(keywords)
    result = processDestinations(destinations, keywords, start, limit)
    # result = sparql.searchWithKeyword(keywords)
    return result


# ranking the destinations, n getting the attributes of the ranked destinations
def processDestinations(destinations, keywords, start, limit):
    ranked = worker.execute(destinations, keywords, start, limit)
    result = sparql.getAttributes(ranked)
    return result