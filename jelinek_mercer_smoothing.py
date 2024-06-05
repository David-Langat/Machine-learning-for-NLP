import os
from bow__doc_coll import BowDocColl 
from bow_query_coll import BowQueryColl

# """
# Pseudocode
# 1. Initialize:
#    - Load 'the50Queries.txt' and parse the queries.
#    - Load documents from 'Data_C101' to 'Data_C150'.

# 2. For each query Q in queries:
#    a. Load the corresponding document collection D.
#    b. For each document d in D:
#       i. Calculate the relevance score P(Q|d) using JM_LM.
#       ii. Store the document ID and its relevance score.
   
#    c. Sort the documents by relevance score in descending order.
#    d. Save the sorted list to 'JM_LM_RxRanking.dat'.
# """





# Function to calculate the relevance score of a document using Jelinek-Mercer smoothing
def jelinek_mercer_smoothing(query, collection_of_documents):
    #local variables
    lambda_ = 0.4
    epsilon = 1e-10  # small constant to avoid zero scores

    # a dictionary with document id as key and the score as value
    collection_score = {}

    #total  number  of  word  occurrences  in  data  collection
    total_words = (collection_of_documents.get_total_term_frequency())

    #Calculate the score for the document
    for document in collection_of_documents.get_docs().values():
        score = 1.0
        document_score = 0
        ntqwd = 0.5
        for term in query.get_terms().keys(): 
             #number of times query word qi occurs in the data collection
            try: 
                ntqwc = collection_of_documents.get_collection_term_frequency()[term] 
            except KeyError: 
                ntqwc = 0
            # number  of  times  query  word  qi occurs  in  document  D
            ntqwd = document.get_term_count(term)
            #the number of word occurrences in the document
            doc_len = len(document.terms)
            #calculate the score for the document
            document_score = ((1-lambda_)*(ntqwd/doc_len)) + lambda_*(ntqwc/total_words)
            if document_score != 0:
                score = score * (document_score + epsilon)
        collection_score[document.get_docid()] = score
        #sort the collection_score by value in descending order
        collection_score = dict(sorted(collection_score.items(), key=lambda x: x[1], reverse=True))
    return collection_score




# Main function that saves the rankings to an output file
def jm_lm(collections_of_queries, data_collection):
    #get the jelinek mercer smoothing scores
    query_position = 101
    document_collection_position = 0
    #changing directory to \Ranking_Output\JM_LM_Output
    os.chdir(os.path.join(os.getcwd(), 'Ranking_Output', 'JM_LM_Output'))
    #loop through all queries
    while query_position <=150:
        query = collections_of_queries.get_query(query_position)
        output_file = os.path.join(os.getcwd(), f'JM_LM_R{query_position}Ranking.dat')
        #get the document collection
        collection_of_documents = data_collection.get_collection(document_collection_position)
        rankings = jelinek_mercer_smoothing(query, collection_of_documents)
        #save the rankings to a file
        with open(output_file, 'w', encoding='utf-8') as out_file:
            for i, (doc_id, score) in enumerate(rankings.items()):
                if i >= 15:
                    break
                out_file.write(f'{doc_id} {score}\n')
        document_collection_position += 1
        query_position += 1
    #change directory back to the root directory
    os.chdir(os.path.join(os.getcwd(), '..','..'))
    
  
   
  