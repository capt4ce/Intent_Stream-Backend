from . import ontology
from . import sparql
from . import worker

# search function accept a tuple that contains (keyword,weight)
# it will return:
#   destination search result
#   additional few highest keywords
# have an option to return all other keywords


# the query string is matched with the dictionary first to get a proper word
def querySearch(queryStr, start, limit):
    words=queryStr.split(' ')

    # matching with dictionary
    queries = []

    destinations = sparql.searchMatchingDestination(queries)
    result = processDestinations(destinations, start, limit)
    # result = sparql.searchWithQuery(queryStr)
    
    return result

# the keywords are collected and directly used in the further processing
def keywordSearch(keywords, start, limit):
    queries = []
    for key in queries:
        queries.append(key)
    destinations = sparql.searchMatchingDestination(queries)
    result = processDestinations(destinations, start, limit)
    # result = sparql.searchWithKeyword(keywords)
    return result


# ranking the destinations, n getting the attributes of the ranked destinations
def processDestinations(destinations, start, limit):
    ranked = worker.cosineSimilarity(destinations, start, limit)
    result = sparql.getAttributes(ranked)
    return result