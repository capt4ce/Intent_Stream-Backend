import rdflib
import rdfextras
import re

import config

filename = config.ROOT_DIR+config.ontology['path']
uri = config.ontology['URI']
ONTO = rdflib.Namespace(uri+'#')

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

# def searchWithQuery(queryStr):
#     # tokenizing search query
#     words=queryStr.split(' ')

#     query=queryBuilder()
#     result=queryProcess(query)
#     return result

# def searchWithKeyword(keywords):
#     query=queryBuilder()
#     result=queryProcess(query)
#     return result
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

def searchMatchingDestination(queries):
    keywords = list()
    for key in queries:
        key = key.replace(' ','_')
        keykey = re.sub(r'[^\w]', '', key)
        keywords.append('myOnto:'+keykey)
    keywords = str(keywords)
    keywords = keywords.replace('\'','')
    keywords = keywords.replace('[','(')
    keywords = keywords.replace(']',')')

    keywordsLiteral = list()
    for key in queries:
        keywordsLiteral.append(key)
    keywordsLiteral = str(keywordsLiteral)
    keywordsLiteral = keywordsLiteral.replace('[','(')
    keywordsLiteral = keywordsLiteral.replace(']',')')



    query="""
        SELECT DISTINCT ?subject
        WHERE {
        ?subject rdf:type myOnto:Destination.
        {?subject   rdf:type ?queries}

        UNION {?subject   myOnto:hasCountry       ?queries}
        UNION {?subject   myOnto:hasCity          ?queries}
        UNION {?subject   myOnto:hasArea          ?queries}
        UNION {?subject   myOnto:hasName          ?queriesLiteral}
        UNION {?subject   myOnto:hasAlias         ?queriesLiteral}
                    
        FILTER (?queries IN %(keywords)s || ?queriesLiteral IN %(keywordsLiteral)s)
        }
        """ %{'keywords':keywords,'keywordsLiteral':keywordsLiteral}
    destinations=[]
    # for i in list(queryProcess(query)):
    #     print(i)
    
    for row in queryProcess(query):
        print("%s" %row)
        url=str('%s' %row)
        destinations.append(g.resource(url))

    # print()
    # for dest in destinations:
    #     print(dest.value(ONTO.hasName))
    # print(list(destinations[0].__iter__()))

    result = []
    for dest in destinations:
        result.append({
            'name': '%s' %dest.value(ONTO.hasName),
            'description': dest.value(ONTO.hasDescription)
        })

    print()
    print(str(result))

    return result


def getAttributes(destinations):
    result = []
    return result


searchMatchingDestination(['Sunset','Arambol Beach, North Goa'])







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
#IF (?property = myOnto:hasCountry, SELECT ?val where{?value myOnto:hasName ?val, ?value})

# SELECT DISTINCT ?subject ?property ?value ?type
#         WHERE {
#         ?subject rdf:type myOnto:Beach.
#         ?subject rdf:type myOnto:Destination.
#         ?subject ?property ?value
        
#             {
#                 SELECT ?type 
#                 where{
#                     ?subject rdf:type ?type
#                 }
#             }
#         }
#         """


# SELECT DISTINCT ?subject (group_concat(?type) as ?types) ?value
#         WHERE {
#         ?subject rdf:type myOnto:Beach.
#         ?subject rdf:type myOnto:Destination.
#         ?subject rdf:type ?type
#         }


# FILTER (?queries in """+str(queries)+""")