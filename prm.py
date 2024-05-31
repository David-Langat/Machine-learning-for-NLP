import os
from bm25 import my_bm25




def retrieve_bm25(collection_of_queries, data_collection):
    '''calculate bm25 scores for all queries and save the scores to a file'''
    #get the bm25 scores
    query_position = 101
    document_collection_position = 0
    #changing directory to \Ranking_Output\PRM_Output\PRM_Input
    os.chdir(os.path.join(os.getcwd(), 'Ranking_Output', 'PRM_Output', 'PRM_Input'))
    #loop through all queries
    while query_position <=150:
        query = collection_of_queries.get_query(query_position)
        output_file = os.path.join(os.getcwd(), f'PRM_R{query_position}.dat')
        #get the document collection
        collection_of_documents = data_collection.get_collection(document_collection_position)
        #get the document frequency which is a dictionary with term as key and term frequency as value
        rankings =my_bm25(collection_of_documents, query)
        #save the rankings to a file
        with open(output_file, 'w', encoding='utf-8') as out_file:
            for doc_id, score in rankings.items():
                out_file.write(f'{doc_id} {score}\n')
        document_collection_position += 1
        query_position += 1
    #change directory back to the root directory
    os.chdir(os.path.join(os.getcwd(), '..','..','..'))
    print("BM25 ranking complete!")

def create_prm_benchmark():
    """Create PRM benchmark based on BM25 scores using PRM hypothesis."""
    input_dir = os.path.join(os.getcwd(), 'Ranking_Output', 'PRM_Output', 'PRM_Input')
    output_dir = os.path.join(os.getcwd(), 'Ranking_Output', 'PRM_Output', 'PRM_Training_benchmark')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        input_file = os.path.join(input_dir, filename)
        base, ext = os.path.splitext(filename)
        new_base = base.replace('PRM_', 'PRM_Training_Benchmark_')
        new_filename = new_base + '.txt'
        output_file = os.path.join(output_dir, new_filename)

        with open(input_file, 'r') as in_file:
            with open(output_file, 'w') as out_file:
                for line in in_file:
                    doc_id, score = line.strip().split()
                    score = float(score)
                    relevance_score = 1 if score > 1 else 0
                    out_file.write(f'{base.split("_")[-1]} {doc_id} {relevance_score}\n')

    

def get_relevance_scores():
    """Get lists of all document IDs, IDs with relevance score 1, and IDs with relevance score 0."""
    input_dir = os.path.join(os.getcwd(), 'Ranking_Output', 'PRM_Output', 'PRM_Training_benchmark')

    doc_ids_dict = {}

    for filename in os.listdir(input_dir):
        input_file = os.path.join(input_dir, filename)
        query_id = int(filename.split('_')[-1].replace('.txt', '').replace('R', ''))

        if query_id not in doc_ids_dict:
            doc_ids_dict[query_id] = {'all_ids': [], 'ids_score_1': [], 'ids_score_0': []}

        with open(input_file, 'r') as in_file:
            for line in in_file:
                _, doc_id, relevance_score = line.strip().split()
                relevance_score = int(relevance_score)

                doc_ids_dict[query_id]['all_ids'].append(doc_id)
                if relevance_score == 1:
                    doc_ids_dict[query_id]['ids_score_1'].append(doc_id)
                elif relevance_score == 0:
                    doc_ids_dict[query_id]['ids_score_0'].append(doc_id)

    return doc_ids_dict

def w5(data_collection,theta):
    relevance_scores = get_relevance_scores()
    #looping through all collections
    for i in range(50):
        collection = data_collection.get_collection(i)







