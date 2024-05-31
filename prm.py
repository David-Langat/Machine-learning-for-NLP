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

    doc_ids_dict = {i: {'all_ids': [], 'ids_score_1': [], 'ids_score_0': []} for i in range(50)}
    counter = 0

    for filename in sorted(os.listdir(input_dir)):
        input_file = os.path.join(input_dir, filename)

        with open(input_file, 'r') as in_file:
            for line in in_file:
                _, doc_id, relevance_score = line.strip().split()
                relevance_score = int(relevance_score)

                doc_ids_dict[counter]['all_ids'].append(doc_id)
                if relevance_score == 1:
                    doc_ids_dict[counter]['ids_score_1'].append(doc_id)
                elif relevance_score == 0:
                    doc_ids_dict[counter]['ids_score_0'].append(doc_id)

        counter += 1

    return doc_ids_dict

def w5(collection_of_documents,theta, i):
    #get the relevance scores in the structure of a dictionary:: collection id as keys and values are list of relvant documents and non relevant documents
    relevance_scores = get_relevance_scores()

    #initialize T to store term and frequency from relevant documents
    T= {}
    relevant_docs = relevance_scores[i]['ids_score_1']
    for doc_id in relevant_docs:
        document = collection_of_documents.get_doc(int(doc_id))
        for term in document.get_term_freq_dict().keys():
            try:
                T[term] += 1
            except KeyError:
                T[term] = 1

    #calculate document frequency of all terms in the collection of documents
    ntk ={} 
    for doc in collection_of_documents.get_docs().values():
        for term in doc.get_term_freq_dict().keys():
            try:
                ntk[term] += 1
            except KeyError:
                ntk[term] = 1
    
    #get number of documents in the collection
    No_docs = collection_of_documents.get_num_docs()
    #get number of relevanat documents
    R = len(relevant_docs)
    
    for id, rtk in T.items():
        T[id] = ((rtk+0.5) / (R-rtk + 0.5)) / ((ntk[id]-rtk+0.5)/(No_docs-ntk[id]-R+rtk +0.5)) 
    
    #calculate the mean of w5 weights.
    meanW5= 0
    if T:  # Check if T is not empty
        for id, rtk in T.items():
            meanW5 += rtk
        meanW5 = meanW5/len(T)
    else:
        meanW5 = 0  # Or any default value

    #Features selection
    Features = {t:r for t,r in T.items() if r > meanW5 + theta }
    return Features

def use_w5 (collection_of_documents):
    theta = 0.5
    for i in range(50):
        # Call the function with the collection, theta, and i
        features = w5(collection_of_documents.get_collection(i), theta, i)

        # Get the current working directory
        cwd = os.getcwd()

        # Define the directory path relative to the current working directory
        dir_path = os.path.join(cwd, 'Ranking_Output', 'PRM_Output', 'PRM_W5')

        # Create the directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)

        # Define the file path
        file_path = os.path.join(dir_path, f'PRM_R{i+101}.dat')

        # Open the file in write mode
        with open(file_path, 'w') as f:
            # Write the features to the file in the format "term: score"
            for term, score in features.items():
                f.write(f'{term}: {score}\n')
   

    







