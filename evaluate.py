import numpy as np
import pandas as pd
import os
import re
from scipy.stats import ttest_rel

# Function to load relevance judgments from files
def load_relevance_judgements(directory_path):
    relevance = {}
    for filename in os.listdir(directory_path):  # Iterate over files in the directory
        if filename.endswith(".txt"):  # Check if the file is a text file
            query_id = re.search(r'\d+', filename).group()  # Extract query ID from filename
            query_id = f'R{query_id}'  # Format query ID
            relevance[query_id] = {}
            with open(os.path.join(directory_path, filename), 'r') as f:  # Open file
                for line in f:  # Read each line
                    parts = line.strip().split()  # Split line into parts
                    if len(parts) == 3:  # Check if the line has three parts
                        _, doc_id, rel = parts
                        relevance[query_id][doc_id] = int(rel)  # Store relevance judgment
    return relevance

# Function to load the PRM rankings with flexible format handling
def load_prm_rankings(filepath):
    model_rankings = {}
    pattern = re.compile(r'_(R\d+)Rank\.txt$')  # Regex pattern to match PRM ranking files

    for filename in os.listdir(filepath):  # Iterate over files in the directory
        if filename.endswith(".txt"):  # Check if the file is a text file
            match = pattern.search(filename)  # Match filename to pattern
            if match:
                query_id = match.group(1)  # Extract query ID
                ranked_list = []
                with open(os.path.join(filepath, filename), 'r') as f:  # Open file
                    for line in f:  # Read each line
                        doc_id, score = line.strip().split()  # Split line into document ID and score
                        ranked_list.append(doc_id)  # Append document ID to the ranked list
                model_rankings[query_id] = ranked_list  # Store ranked list for the query
            else:
                print(f"Filename '{filename}' does not match the expected pattern")
    return model_rankings

# Function to load all model rankings from files
def load_all_rankings(directory_path):
    model_rankings = {}
    pattern = re.compile(r'_(R\d+)Ranking\.dat$')  # Regex pattern to match ranking files

    for filename in os.listdir(directory_path):  # Iterate over files in the directory
        if filename.endswith(".dat"):  # Check if the file is a .dat file
            match = pattern.search(filename)  # Match filename to pattern
            if match:
                query_id = match.group(1)  # Extract query ID
                ranked_list = []
                with open(os.path.join(directory_path, filename), 'r') as f:  # Open file
                    for line in f:  # Read each line
                        doc_id, score = line.strip().split()  # Split line into document ID and score
                        ranked_list.append(doc_id)  # Append document ID to the ranked list
                model_rankings[query_id] = ranked_list  # Store ranked list for the query
            else:
                print(f"Filename '{filename}' does not match the expected pattern")
    return model_rankings

# Function to calculate Average Precision (AP)
def calculate_ap(ranked_list, relevance):
    relevant_count = 0
    precision_at_k = []
    for i, doc_id in enumerate(ranked_list, 1):  # Iterate over the ranked list
        if relevance.get(doc_id, 0) == 1:  # Check if the document is relevant
            relevant_count += 1
            precision_at_k.append(relevant_count / i)  # Calculate precision at k
    return np.mean(precision_at_k) if precision_at_k else 0  # Return mean average precision

# Function to calculate Precision@10
def calculate_precision_at_10(ranked_list, relevance):
    relevant_count = sum(1 for doc_id in ranked_list[:10] if relevance.get(doc_id, 0) == 1)  # Count relevant documents in top 10
    return relevant_count / 10  # Return precision at 10

# Function to calculate DCG@10
def calculate_dcg_at_10(ranked_list, relevance):
    dcg = sum((relevance.get(doc_id, 0) / np.log2(i + 2)) for i, doc_id in enumerate(ranked_list[:10]))  # Calculate DCG at 10
    return dcg

# Function to evaluate models including My_PRM
def evaluate_models_with_prm(relevance_judgements, bm25_rankings, jm_lm_rankings, prm_relevance_judgements):
    results = {
        'Topic': [],
        'BM25_MAP': [], 'BM25_Precision@10': [], 'BM25_DCG@10': [],
        'JM_LM_MAP': [], 'JM_LM_Precision@10': [], 'JM_LM_DCG@10': [],
        'My_PRM_MAP': [], 'My_PRM_Precision@10': [], 'My_PRM_DCG@10': []
    }

    for query_id in relevance_judgements:  # Iterate over relevance judgments
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

    df_results = pd.DataFrame(results)  # Create a DataFrame from the results
    df_results.loc['Average'] = df_results.mean(numeric_only=True)  # Calculate average for each metric
    df_results.at['Average', 'Topic'] = 'Average'  # Label the average row
    return df_results

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current script directory
relevance_judgements_path = os.path.join(script_dir, 'EvaluationBenchmark')
prm_rankings_path = os.path.join(script_dir, 'Ranking_Output', 'PRM_Output', 'PRM_Test_Ranks')
bm25_rankings_path = os.path.join(script_dir, 'Ranking_Output', 'BM25_Output')
jm_lm_rankings_path = os.path.join(script_dir, 'Ranking_Output', 'JM_LM_Output')

# Load data
relevance_judgements = load_relevance_judgements(relevance_judgements_path)
prm_rankings = load_prm_rankings(prm_rankings_path)
bm25_rankings = load_all_rankings(bm25_rankings_path)
jm_lm_rankings = load_all_rankings(jm_lm_rankings_path)

# Evaluate the models
evaluation_results = evaluate_models_with_prm(relevance_judgements, bm25_rankings, jm_lm_rankings, prm_rankings)

# Create individual tables
map_table = evaluation_results[['Topic', 'BM25_MAP', 'JM_LM_MAP', 'My_PRM_MAP']]
precision_table = evaluation_results[['Topic', 'BM25_Precision@10', 'JM_LM_Precision@10', 'My_PRM_Precision@10']]
dcg_table = evaluation_results[['Topic', 'BM25_DCG@10', 'JM_LM_DCG@10', 'My_PRM_DCG@10']]

# Display tables
print("Table 1. The performance of 3 models on average precision (MAP)")
print(map_table.to_string(index=False))

print("\nTable 2. The performance of 3 models on precision@10")
print(precision_table.to_string(index=False))

print("\nTable 3. The performance of 3 models on DCG@10")
print(dcg_table.to_string(index=False))

# Save to CSV
map_table.to_csv('map_table.csv', index=False)
precision_table.to_csv('precision_table.csv', index=False)
dcg_table.to_csv('dcg_table.csv', index=False)


# Perform paired t-tests for MAP, Precision@10, and DCG@10 and save results
def perform_ttest(data1, data2, label1, label2):
    t_statistic, p_value = ttest_rel(data1, data2, nan_policy='omit')
    significant = p_value < 0.05
    return t_statistic, p_value, significant

# Perform t-tests for MAP
t_statistic_bm25_jm_lm_map, p_value_bm25_jm_lm_map, sig_bm25_jm_lm_map = perform_ttest(evaluation_results['BM25_MAP'].iloc[:-1], evaluation_results['JM_LM_MAP'].iloc[:-1], 'BM25', 'JM_LM')
t_statistic_bm25_my_prm_map, p_value_bm25_my_prm_map, sig_bm25_my_prm_map = perform_ttest(evaluation_results['BM25_MAP'].iloc[:-1], evaluation_results['My_PRM_MAP'].iloc[:-1], 'BM25', 'My_PRM')
t_statistic_jm_lm_my_prm_map, p_value_jm_lm_my_prm_map, sig_jm_lm_my_prm_map = perform_ttest(evaluation_results['JM_LM_MAP'].iloc[:-1], evaluation_results['My_PRM_MAP'].iloc[:-1], 'JM_LM', 'My_PRM')

# Perform t-tests for Precision@10
t_statistic_bm25_jm_lm_prec10, p_value_bm25_jm_lm_prec10, sig_bm25_jm_lm_prec10 = perform_ttest(evaluation_results['BM25_Precision@10'].iloc[:-1], evaluation_results['JM_LM_Precision@10'].iloc[:-1], 'BM25', 'JM_LM')
t_statistic_bm25_my_prm_prec10, p_value_bm25_my_prm_prec10, sig_bm25_my_prm_prec10 = perform_ttest(evaluation_results['BM25_Precision@10'].iloc[:-1], evaluation_results['My_PRM_Precision@10'].iloc[:-1], 'BM25', 'My_PRM')
t_statistic_jm_lm_my_prm_prec10, p_value_jm_lm_my_prm_prec10, sig_jm_lm_my_prm_prec10 = perform_ttest(evaluation_results['JM_LM_Precision@10'].iloc[:-1], evaluation_results['My_PRM_Precision@10'].iloc[:-1], 'JM_LM', 'My_PRM')

# Perform t-tests for DCG@10
t_statistic_bm25_jm_lm_dcg10, p_value_bm25_jm_lm_dcg10, sig_bm25_jm_lm_dcg10 = perform_ttest(evaluation_results['BM25_DCG@10'].iloc[:-1], evaluation_results['JM_LM_DCG@10'].iloc[:-1], 'BM25', 'JM_LM')
t_statistic_bm25_my_prm_dcg10, p_value_bm25_my_prm_dcg10, sig_bm25_my_prm_dcg10 = perform_ttest(evaluation_results['BM25_DCG@10'].iloc[:-1], evaluation_results['My_PRM_DCG@10'].iloc[:-1], 'BM25', 'My_PRM')
t_statistic_jm_lm_my_prm_dcg10, p_value_jm_lm_my_prm_dcg10, sig_jm_lm_my_prm_dcg10 = perform_ttest(evaluation_results['JM_LM_DCG@10'].iloc[:-1], evaluation_results['My_PRM_DCG@10'].iloc[:-1], 'JM_LM', 'My_PRM')

# Save t-test results to a DataFrame
ttest_results = pd.DataFrame({
    'Comparison': ['BM25_vs_JM_LM', 'BM25_vs_My_PRM', 'JM_LM_vs_My_PRM'],
    'MAP_t-statistic': [t_statistic_bm25_jm_lm_map, t_statistic_bm25_my_prm_map, t_statistic_jm_lm_my_prm_map],
    'MAP_p-value': [p_value_bm25_jm_lm_map, p_value_bm25_my_prm_map, p_value_jm_lm_my_prm_map],
    'MAP_Significant': [sig_bm25_jm_lm_map, sig_bm25_my_prm_map, sig_jm_lm_my_prm_map],
    'Precision@10_t-statistic': [t_statistic_bm25_jm_lm_prec10, t_statistic_bm25_my_prm_prec10, t_statistic_jm_lm_my_prm_prec10],
    'Precision@10_p-value': [p_value_bm25_jm_lm_prec10, p_value_bm25_my_prm_prec10, p_value_jm_lm_my_prm_prec10],
    'Precision@10_Significant': [sig_bm25_jm_lm_prec10, sig_bm25_my_prm_prec10, sig_jm_lm_my_prm_prec10],
    'DCG@10_t-statistic': [t_statistic_bm25_jm_lm_dcg10, t_statistic_bm25_my_prm_dcg10, t_statistic_jm_lm_my_prm_dcg10],
    'DCG@10_p-value': [p_value_bm25_jm_lm_dcg10, p_value_bm25_my_prm_dcg10, p_value_jm_lm_my_prm_dcg10],
    'DCG@10_Significant': [sig_bm25_jm_lm_dcg10, sig_bm25_my_prm_dcg10, sig_jm_lm_my_prm_dcg10]
})

# Save t-test results to CSV
ttest_results.to_csv('ttest_results.csv', index=False)

# Display t-test results
print("\nT-Test Results:")
print(ttest_results.to_string(index=False))

