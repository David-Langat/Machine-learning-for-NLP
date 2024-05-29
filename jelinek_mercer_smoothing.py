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
def jelinek_mercer_smoothing(query, document, collection, lambda_=0.4):
    doc_length = document.get_doc_len()
    score = 1.0
    # Calculate the score for each term in the query
    for word in query.terms:
        # Probability of the term in the document
        p_doc = document.get_term_count(word) / doc_length if doc_length > 0 else 0
        # Probability of the term in the collection
        p_col = collection.get_collection_freq[word]/ collection.get_total_words(len(collection.get_collection_freq()))
        # Jelinek-Mercer smoothing formula
        score *= (lambda_ * p_doc) + ((1 - lambda_) * p_col)
    return score

# Function to rank documents based on their relevance to a query
def rank_documents(query, collection, lambda_=0.4):
    rankings = []
    # Calculate the score for each document in the collection
    for document in collection.get_docs().values():
        score = jelinek_mercer_smoothing(query, document, collection, lambda_)
        rankings.append((document.get_docid(), score))
    # Sort the documents by score in descending order
    rankings.sort(key=lambda x: x[1], reverse=True)
    return rankings

# Function to save the rankings to an output file
def save_rankings(rankings, output_path, query_id):
    # Define the output file path
    output_file = os.path.join(output_path, f'JM_LM_{query_id}Ranking.dat')
    # Write the rankings to the output file
    with open(output_file, 'w') as out_file:
        for doc_id, score in rankings:
            out_file.write(f'{doc_id} {score}\n')