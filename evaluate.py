import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
import os
import re

# Load relevance judgments from files
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

# Load all model rankings
def load_all_rankings(directory_path):
    model_rankings = {}
    pattern = re.compile(r'_(R\d+)Ranking\.dat$')  # Matches _R<query_id>Ranking.dat

    for filename in os.listdir(directory_path):
        if filename.endswith(".dat"):
            match = pattern.search(filename)
            if match:
                query_id = match.group(1)  # Extracts the R<query_id> part
                ranked_list = []
                with open(os.path.join(directory_path, filename), 'r') as f:
                    for line in f:
                        doc_id, score = line.strip().split()
                        ranked_list.append(doc_id)
                model_rankings[query_id] = ranked_list
            else:
                print(f"Filename '{filename}' does not match the expected pattern")
    return model_rankings

# Calculate Average Precision (AP)
def calculate_ap(ranked_list, relevance):
    relevant_count = 0
    precision_at_k = []
    for i, doc_id in enumerate(ranked_list, 1):
        if relevance.get(doc_id, 0) == 1:
            relevant_count += 1
            precision_at_k.append(relevant_count / i)
    return np.mean(precision_at_k) if precision_at_k else 0

# Calculate Precision@10
def calculate_precision_at_10(ranked_list, relevance):
    relevant_count = sum(1 for doc_id in ranked_list[:10] if relevance.get(doc_id, 0) == 1)
    return relevant_count / 10

# Calculate DCG@10
def calculate_dcg_at_10(ranked_list, relevance):
    dcg = sum((relevance.get(doc_id, 0) / np.log2(i + 2)) for i, doc_id in enumerate(ranked_list[:10]))
    return dcg

# Evaluate models
def evaluate_models(relevance_judgements, bm25_rankings, jm_lm_rankings):
    results = {
        'Topic': [],
        'BM25_MAP': [], 'BM25_Precision@10': [], 'BM25_DCG@10': [],
        'JM_LM_MAP': [], 'JM_LM_Precision@10': [], 'JM_LM_DCG@10': []
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

    df_results = pd.DataFrame(results)
    df_results.loc['Average'] = df_results.mean(numeric_only=True)
    df_results.at['Average', 'Topic'] = 'Average'
    return df_results

# Perform t-tests
def perform_t_tests(df_results):
    metrics = ['MAP', 'Precision@10', 'DCG@10']
    t_test_results = {}

    for metric in metrics:
        bm25_scores = df_results[f'BM25_{metric}'].dropna()
        jm_lm_scores = df_results[f'JM_LM_{metric}'].dropna()
        t_stat, p_value = ttest_ind(bm25_scores, jm_lm_scores)
        t_test_results[metric] = {'t_stat': t_stat, 'p_value': p_value}

    return t_test_results

# Example usage
relevance_judgements = load_relevance_judgements('C:/Users/s4021/OneDrive/桌面/Machine-learning-for-NLP-1/EvaluationBenchmark')

# Ensure you have already saved the rankings for BM25 and JM_LM
bm25_rankings = load_all_rankings('C:/Users/s4021/OneDrive/桌面/Machine-learning-for-NLP-1/Ranking_Output/BM25_Output')
jm_lm_rankings = load_all_rankings('C:/Users/s4021/OneDrive/桌面/Machine-learning-for-NLP-1/Ranking_Output/JM_LM_Output')

evaluation_results = evaluate_models(relevance_judgements, bm25_rankings, jm_lm_rankings)

# Perform t-tests
t_test_results = perform_t_tests(evaluation_results)

# Print t-test results
for metric, result in t_test_results.items():
    print(f"{metric} T-Test:")
    print(f"  t-statistic: {result['t_stat']}")
    print(f"  p-value: {result['p_value']}")

# Create individual tables
map_table = evaluation_results[['Topic', 'BM25_MAP', 'JM_LM_MAP']]
precision_table = evaluation_results[['Topic', 'BM25_Precision@10', 'JM_LM_Precision@10']]
dcg_table = evaluation_results[['Topic', 'BM25_DCG@10', 'JM_LM_DCG@10']]

# Display tables
print("Table 1. The performance of 2 models on average precision (MAP)")
print(map_table.to_string(index=False))

print("\nTable 2. The performance of 2 models on precision@10")
print(precision_table.to_string(index=False))

print("\nTable 3. The performance of 2 models on DCG@10")
print(dcg_table.to_string(index=False))

# Save to CSV
map_table.to_csv('map_table.csv', index=False)
precision_table.to_csv('precision_table.csv', index=False)
dcg_table.to_csv('dcg_table.csv', index=False)
