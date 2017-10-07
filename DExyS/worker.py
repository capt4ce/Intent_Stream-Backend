from collections import Counter
import math

# Using Cosine Similarity Technique
# to calculate the accuracy of the destination
# to be retrieved and further rank them
# as the result of the searching
# def cosineSimilarity(destinations, keywords, start, limit):
#     # tag_vals = []       #for counting tags
#     # words = []          #for storing the accumulative tag
#     # vects = []          #for storing counter vector
#     # tags_len = []

#     # for dest in destinations:
#     #     # count tag occurrences in each destination
#     #     val = Counter(dest['tags'])
#     #     tag_vals.append(val)

#     #     # convert to word-vectors
#     #     words.append(tag_vals[i].keys())
    
#     # i=0
#     # for dest in destinations:
#     #     tags_len.append(sum(av*av for av in vects[i]) ** 0.5)
    
#     # dot    = sum(av*bv for av,bv in zip(a_vect, b_vect))    # 3
#     # cosine = dot / (len_a * len_b)

#     dest_len = len(destinations)+1              # n = length of data + 1 (query)
#     # words = []
#     words = list(keywords.keys())
#     df = []                                     # Document Frequency of each frequency
#     idf = []                                    # Inverse Document Frequency of each frequency

#     # for word in keywords.keys():
#     #     words.append(word)

#     # for dest in destinations:
#     #     words = list(keywords.keys() | dest.tags | dest.types)
#     #     df.append()
#     #     idf.append(math.log10(dest_len/df))

#     # # for generating the complete words
#     for dest in destinations:
#         words = list(words | list(dest['tags']) | list(dest['types']))
#     #     words = concatenate(words,dest['tags'])
#     #     words = concatenate(words,dest['types'])


#     m, n = len(words), len(destinations)+1;
#     Matrix = [[0 for x in range(m)] for y in range(n)] 
#     print(words)
#     for idx,word in enumerate(words):
#         i = 0
#         for term in keywords.keys():
#             if (word == term): i+=1
#         Matrix[idx][0] = i
#         print(str(idx))

#         for dest_idx,dest in enumerate(destinations):
#             j=0
#             for tag in dest['tags']:
#                 if (word==tag): j+=1
#             Matrix[idx][dest_idx+1] = i

#     for i in m:
#         k=0
#         for j in n:
#            k+=Matrix[i][j] 
#         df.append(k)
#         idf = math.log10(dest_len/df)
#     print(df)
#     print(idf)
#     result = []
#     return result

def execute(destinations, keywords, start, limit):
    # Getting normalised TF of each document
    total_terms={}
    dest_tf=[]
    match_terms_with_keywords = []
    for i in destinations:
        match_terms_with_keywords.append(0)

    for idx,dest in enumerate(destinations):
        terms =  dest['types']
        terms += dest['tags']
        terms.append(dest['country'])
        print(terms)
        dest_tf.append(1/len(terms))
        for term in terms:
            if term in keywords:
                match_terms_with_keywords[idx]+=1
        # for term in terms:
        #     if term in terms:
        #         terms[term] += 1
        #     else:
        #         terms[term] = 1
    
    # print(total_terms)

    # calculating IDF of each terms in total_terms
    for term in total_terms.keys():
        total_terms[term]=1+math.log(len(destinations)/total_terms[term])


    # Getting TF of queries / keywords
    # keywordsTF = Counter(keywords.keys())
    keywords_tf = 1/len(keywords.keys())
    print(keywords)
    print(match_terms_with_keywords)

    cosine_vals = cosineSimilarity(dest_tf, keywords_tf, match_terms_with_keywords)

    if limit<=0:
        limit = 10
    result=[]
    if len(cosine_vals):        
        for i in range(limit-1):
            if max(cosine_vals) == -1:
                break
            # print(str(cosine_vals)+' '+str(max(cosine_vals))+' '+str(start)+' '+str(limit))
            idx_max = cosine_vals.index(max(cosine_vals))
            # del cosine_vals[idx_max]
            cosine_vals[idx_max]=-1
            if start!=0:
                start-=1
                i-=1
            
            else:
                result.append(destinations[idx_max])
        
    return result
    

def cosineSimilarity(dest_tf, keywords_tf, match_terms_with_keywords):
    result = []

    print('keyword_tf '+str(keywords_tf))
    q = math.sqrt((keywords_tf**2)*1/keywords_tf)
    for i,val in enumerate(dest_tf):    
            # dot product
            # dot_keywords = keywords_tf*keywords_tf
        dot_dest = dest_tf[i]*keywords_tf*match_terms_with_keywords[i]
            # if int(1/keywords_tf)>len(dest_tf):
            #     dot_dest=0
            # else:
            #     dot_dest = dest_tf[i]*keywords_tf*1/keywords_tf
            #     # dot_dest = dest_tf[i]**int(1/keywords_tf)

        print(dot_dest)        
        d = math.sqrt((dest_tf[i]**2)*match_terms_with_keywords[i])
        print(str(q)+','+str(d))

            # cosine similarity
        try:
            result.append(dot_dest/(q*d))
        except ZeroDivisionError:
            result.append(0)

    print(result)

    return result

