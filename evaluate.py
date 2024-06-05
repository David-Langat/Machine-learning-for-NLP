import numpy as np
import pandas as pd
import os
import re
from scipy.stats import ttest_rel

# Function to load relevance judgments from files
# 1. Initialize an empty dictionary called 'relevance'.
# 2. For each file in the given directory_path:
#    a. Check if the file ends with ".txt".
#    b. Extract the query ID from the filename.
#    c. Initialize a dictionary for the query ID in 'relevance'.
#    d. Open the file and read it line by line:
#       i. Split each line into parts.
#       ii. If there are three parts, assign the document ID and relevance score to the dictionary.
# 3. Return the 'relevance' dictionary.
def load_relevance_judgements(directory_path):
    relevance = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            query_id = re.search(r'\d+', filename).group()
            query_id = f'R{query_id}'
            relevance[query_id] = {}
            with open(os.path.join(directory_path, filename), 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 3:
                        _, doc_id, rel = parts
                        relevance[query_id][doc_id] = int(rel)
    return relevance

# Function to load the PRM rankings with flexible format handling
# 1. Initialize an empty dictionary called 'model_rankings'.
# 2. Define a pattern to match filenames.
# 3. For each file in the given filepath:
#    a. Check if the file ends with ".txt".
#    b. Match the pattern with the filename.
#    c. If the pattern matches, extract the query ID and initialize a list.
#    d. Open the file and read it line by line:
#       i. Split each line into document ID and score.
#       ii. Append the document ID to the list.
#    e. Assign the list to 'model_rankings' for the query ID.
# 4. Return the 'model_rankings' dictionary.
def load_prm_rankings(filepath):
    model_rankings = {}
    pattern = re.compile(r'_(R\d+)Rank\.txt$')

    for filename in os.listdir(filepath):
        if filename.endswith(".txt"):
            match = pattern.search(filename)
            if match:
                query_id = match.group(1)
                ranked_list = []
                with open(os.path.join(filepath, filename), 'r') as f:
                    for line in f:
                        doc_id, score = line.strip().split()
                        ranked_list.append(doc_id)
                model_rankings[query_id] = ranked_list
            else:
                print(f"Filename '{filename}' does not match the expected pattern")
    return model_rankings

# Function to load all model rankings from files
# 1. Initialize an empty dictionary called 'model_rankings'.
# 2. Define a pattern to match filenames.
# 3. For each file in the given directory_path:
#    a. Check if the file ends with ".dat".
#    b. Match the pattern with the filename.
#    c. If the pattern matches, extract the query ID and initialize a list.
#    d. Open the file and read it line by line:
#       i. Split each line into document ID and score.
#       ii. Append the document ID to the list.
#    e. Assign the list to 'model_rankings' for the query ID.
# 4. Return the 'model_rankings' dictionary.
def load_all_rankings(directory_path):
    model_rankings = {}
    pattern = re.compile(r'_(R\d+)Ranking\.dat$')

    for filename in os.listdir(directory_path):
        if filename.endswith(".dat"):
            match = pattern.search(filename)
            if match:
                query_id = match.group(1)
                ranked_list = []
                with open(os.path.join(directory_path, filename), 'r') as f:
                    for line in f:
                        doc_id, score = line.strip().split()
                        ranked_list.append(doc_id)
                model_rankings[query_id] = ranked_list
            else:
                print(f"Filename '{filename}' does not match the expected pattern")
    return model_rankings

# Function to calculate Average Precision (AP)
# 1. Initialize relevant_count to 0 and precision_at_k to an empty list.
# 2. For each document ID in the ranked list:
#    a. If the document is relevant, increment relevant_count and append precision to precision_at_k.
# 3. Return the mean of precision_at_k or 0 if precision_at_k is empty.
def calculate_ap(ranked_list, relevance):
    relevant_count = 0
    precision_at_k = []
    for i, doc_id in enumerate(ranked_list, 1):
        if relevance.get(doc_id, 0) == 1:
            relevant_count += 1
            precision_at_k.append(relevant_count / i)
    return np.mean(precision_at_k) if precision_at_k else 0

# Function to calculate Precision@10
# 1. Count the number of relevant documents in the top 10 of the ranked list.
# 2. Return the count divided by 10.
def calculate_precision_at_10(ranked_list, relevance):
    relevant_count = sum(1 for doc_id in ranked_list[:10] if relevance.get(doc_id, 0) == 1)
    return relevant_count / 10

# Function to calculate DCG@10
# 1. Initialize dcg to 0.
# 2. For each document ID in the top 10 of the ranked list:
#    a. Add the relevance score divided by log2(i+2) to dcg.
# 3. Return dcg
def calculate_dcg_at_10(ranked_list, relevance):
    dcg = sum((relevance.get(doc_id, 0) / np.log2(i + 2)) for i, doc_id in enumerate(ranked_list[:10]))
    return dcg

# Function to evaluate models including My_PRM
# 1. Initialize a dictionary to store the results.
# 2. For each query ID in the relevance judgments:
#    a. Retrieve the relevance scores for the query.
#    b. Evaluate BM25, JM_LM, and My_PRM models:
#       i. Calculate AP, Precision@10, and DCG@10 for each model.
#       ii. Store the results in the dictionary.
# 3. Create a DataFrame from the results dictionary.
# 4. Calculate the average values for each metric and add to the DataFrame.
# 5. Return the DataFrame.
def evaluate_models_with_prm(relevance_judgements, bm25_rankings, jm_lm_rankings, prm_relevance_judgements):
    results = {
        'Topic': [],
        'BM25_MAP': [], 'BM25_Precision@10': [], 'BM25_DCG@10': [],
        'JM_LM_MAP': [], 'JM_LM_Precision@10': [], 'JM_LM_DCG@10': [],
        'My_PRM_MAP': [], 'My_PRM_Precision@10': [], 'My_PRM_DCG@10': []
    }

    for query_id in relevance_judgements:
        relevance = relevance_judgements[query_id]
        results['Topic'].append(query_id)

        # BM25 evaluation
        if query_id in bm25_rankings:
            bm25_ranked_list = bm25_rankings[query_id]
            ap_bm25 = calculate_ap(bm25_ranked_list, relevance)
            precision_at_10_bm25 = calculate_precision_at_10(bm25_ranked_list, relevance)
            dcg_at_10_bm25 = calculate_dcg_at_10(bm25_ranked_list, relevance)
            results['BM25_MAP'].append(ap_bm25)
            results['BM25_Precision@10'].append(precision_at_10_bm25)
            results['BM25_DCG@10'].append(dcg_at_10_bm25)
        else:
            results['BM25_MAP'].append(np.nan)
            results['BM25_Precision@10'].append(np.nan)
            results['BM25_DCG@10'].append(np.nan)

        # JM_LM evaluation
        if query_id in jm_lm_rankings:
            jm_lm_ranked_list = jm_lm_rankings[query_id]
            ap_jm_lm = calculate_ap(jm_lm_ranked_list, relevance)
            precision_at_10_jm_lm = calculate_precision_at_10(jm_lm_ranked_list, relevance)
            dcg_at_10_jm_lm = calculate_dcg_at_10(jm_lm_ranked_list, relevance)
            results['JM_LM_MAP'].append(ap_jm_lm)
            results['JM_LM_Precision@10'].append(precision_at_10_jm_lm)
            results['JM_LM_DCG@10'].append(dcg_at_10_jm_lm)
        else:
            results['JM_LM_MAP'].append(np.nan)
            results['JM_LM_Precision@10'].append(np.nan)
            results['JM_LM_DCG@10'].append(np.nan)

        # My_PRM evaluation
        if query_id in prm_relevance_judgements:
            my_prm_ranked_list = prm_relevance_judgements[query_id]
            ap_my_prm = calculate_ap(my_prm_ranked_list, relevance)
            precision_at_10_my_prm = calculate_precision_at_10(my_prm_ranked_list, relevance)
            dcg_at_10_my_prm = calculate_dcg_at_10(my_prm_ranked_list, relevance)
            results['My_PRM_MAP'].append(ap_my_prm)
            results['My_PRM_Precision@10'].append(precision_at_10_my_prm)
            results['My_PRM_DCG@10'].append(dcg_at_10_my_prm)
        else:
            results['My_PRM_MAP'].append(np.nan)
            results['My_PRM_Precision@10'].append(np.nan)
            results['My_PRM_DCG@10'].append(np.nan)

    df_results = pd.DataFrame(results)
    df_results.loc['Average'] = df_results.mean(numeric_only=True)
    df_results.at['Average', 'Topic'] = 'Average'
    return df_results


# Function to perform paired t-tests for MAP, Precision@10, and DCG@10
# 1. Perform a paired t-test between two sets of data.
# 2. Check if the p-value is less than 0.05 to determine significance.
# 3. Return the t-statistic, p-value, and whether the result is significant.
def perform_ttest(data1, data2, label1, label2):
    t_statistic, p_value = ttest_rel(data1, data2, nan_policy='omit')
    significant = p_value < 0.05
    return t_statistic, p_value, significant
