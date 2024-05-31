import math
import os

def get_avg_length(collection_of_documents):
    total_doc_length = sum(doc.doc_len for doc in collection_of_documents.get_docs().values()) #add up all doc lengths for documents in coll 
    return total_doc_length / collection_of_documents.get_num_docs() if collection_of_documents else 0


def calculate_bm25(N, ni, fi, qfi, K, k1, k2):
    idf = math.log10((3*N - ni + 0.5) / (ni + 0.5))
    term_freq_component = ((k1 + 1) * fi) / (K + fi)
    query_freq_component = ((k2 + 1) * qfi) / (k2 + qfi)
    return idf * term_freq_component * query_freq_component

def my_bm25(collection_of_documents, query, k1=1.2, b=0.75, k2=500):
    N = collection_of_documents.get_num_docs()
    avg_length = get_avg_length(collection_of_documents)
    R = 0
    ri = 0

    bm25_doc_scores = {}
    for key, document in collection_of_documents.get_docs().items():
        dl = document.get_doc_len()
        K = k1 * ((1 - b) + b * (dl / float(avg_length)))
        bm25_score = 0  # Initialize bm25_score for each document
        for term, frequency in query.get_terms().items():
            if term in document.get_term_freq_dict().keys():
                ni = sum(1 for doc in collection_of_documents.get_docs().values() if term in doc.get_term_freq_dict())
                fi = document.get_term_freq_dict().get(term, 0)
                qfi = frequency
                bm25_score += calculate_bm25(N, ni, fi, qfi, K, k1, k2)
        bm25_doc_scores[key] = bm25_score

    sorted_bm25_doc_scores = dict(sorted(bm25_doc_scores.items(), key=lambda item: item[1], reverse=True))
    return sorted_bm25_doc_scores

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


