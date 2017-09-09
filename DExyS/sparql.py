import rdflib
import rdfextras

import config

filename = config.ROOT_DIR+config.ontology['path']
uri = config.ontology['URI']

rdfextras.registerplugins() # so we can Graph.query()

g=rdflib.Graph()
g.parse(filename)
print('loading RDF graph...')

# ===================================================
# FUNCTIONS
# ===================================================
# base function to execute queries
def queryProcess(query):
    prefix="""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX myOnto: <""" + config.ontology['URI'] +'#>'
    
    print(prefix+query)

    return g.query(prefix+query)

def queryBuilder():
    # building sparql query based on type of each token in the search query (and weight of each if any)
    query=''
    return query

def searchWithQuery(queryStr):
    # tokenizing search query
    words=queryStr.split(' ')

    query=queryBuilder()
    result=queryProcess(query)
    return result

def searchWithKeyword(keywords):
    query=queryBuilder()
    result=queryProcess(query)
    return result
# ===================================================

def getDestinations():
    pass

# ===================================================

def example_countries():
    results = g.query("""
    SELECT ?p ?o
    WHERE {
    ?p <%s#hasCountry> ?o.
    }
    ORDER BY (?p)
    """ %uri) #get every hasCountry relation

    print(list(results))

def example_destinations():
    query="""
        SELECT *
        WHERE {
        ?subject rdf:type myOnto:Beach.
        ?subject rdf:type myOnto:Destination.
        }
        """

    print(list(queryProcess(query)))

example_destinations()






# EXAMPLE WITH SPARQLWrapper
# from SPARQLWrapper import SPARQLWrapper, JSON

# sparql = SPARQLWrapper("http://dbpedia.org/sparql")
# sparql.setQuery("""
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     SELECT ?label
#     WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
# """)
# sparql.setReturnFormat(JSON)
# results = sparql.query().convert()

# print(results)

# for result in results["results"]["bindings"]:
#     print(result["label"]["value"])

#FILTER (regex(str(?a),"myOnto:Beach","i"))