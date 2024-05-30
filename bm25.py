import math
import os

def get_avg_length(collection_of_documents):
    total_doc_length = sum(doc.doc_len for doc in collection_of_documents.get_docs().values()) #add up all doc lengths for documents in coll 
    return total_doc_length / collection_of_documents.get_num_docs() if collection_of_documents else 0


def my_bm25(collection_of_documents, query):
    # Following lecture slides
    k1 = 1.2
    b = 0.75
    k2 = 100

    # As per assignment sheet
    R = 0
    ri = 0
    N = collection_of_documents.get_num_docs()

    bm25_doc_sores = {}
    for key, document in collection_of_documents.get_docs().items():
        # Iterate through each term in the query
        K = k1 * ((1 - b) + b * (document.get_doc_len() / get_avg_length(collection_of_documents)))
        bm25_intermediate_sum = 0
        for term, frequency in query.get_terms().items():
            bm25_intermediate_sum = 0
            if term in document.get_term_freq_dict().keys():
                ni = document.get_term_freq_dict()[term]
            else:
                ni = 0.1 # non zero otherwise log would be undefined
            if term in document.get_term_freq_dict():
                fi = document.get_term_freq_dict()[term]
            else:
                fi = 0.1 # non zero otherwise log would be undefined
            qfi = frequency
            # BM25 equation broken up into separate terms for better readability
            coefficient1 = ((ri + 0.5) / (R - ri + 0.5)) / ((ni - ri + 0.5) / (N - ni - R + ri + 0.5))
            coefficient2 = ((k1 + 1) * fi) / K + fi
            coefficient3 = ((k2 + 1) * qfi) / k2 + qfi
            bm25_intermediate_sum += math.log10(coefficient1 * coefficient2 * coefficient3) # Sum up for all terms in query
        bm25_doc_sores[key] = bm25_intermediate_sum
    sorted_bm25_doc_sores = dict(sorted(bm25_doc_sores.items(), key=lambda item: item[1], reverse=True))
    # print(sorted_bm25_doc_sores)
    return sorted_bm25_doc_sores

def perform_bm25(collection_of_queries, data_collection):

    #get the bm25 scores
    query_position = 101
    document_collection_position = 0
    #changing directory to \Ranking_Output\JM_LM_Output
    os.chdir(os.path.join(os.getcwd(), 'Ranking_Output', 'BM25_Output'))
    #loop through all queries
    while query_position <=150:
        query = collection_of_queries.get_query(query_position)
        output_file = os.path.join(os.getcwd(), f'BM25_R{query_position}Ranking.dat')
        #get the document collection
        collection_of_documents = data_collection.get_collection(document_collection_position)
        #get the document frequency which is a dictionary with term as key and term frequency as value
        rankings =my_bm25(collection_of_documents, query)
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
    print("BM25 ranking complete!")


