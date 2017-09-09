from . import ontology
from . import sparql
from . import worker

# search function accept a tuple that contains (keyword,weight)
# it will return:
#   destination search result
#   additional few highest keywords
# have an option to return all other keywords
def querySearch(queryStr):
    result = sparql.searchWithQuery(queryStr)
    return result

def keywordSearch(keywords):
    result = sparql.searchWithKeyword(keywords)
    return result