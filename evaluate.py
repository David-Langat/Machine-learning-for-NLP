import numpy as np
import pandas as pd
import os
import re
from scipy.stats import ttest_rel

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


# Function to load the PRM Training Benchmark relevance judgments
def load_prm_relevance_judgements(directory_path):
    relevance = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            query_id = re.search(r'\d+', filename).group()
            query_id = f'R{query_id}'
            relevance[query_id] = {}
            with open(os.path.join(directory_path, filename), 'r') as f:
                for line in f:
                    _, doc_id, rel = line.strip().split()
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

# Evaluate models including My_PRM
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
            if not isinstance(my_prm_ranked_list, list):
                my_prm_ranked_list = list(my_prm_ranked_list)
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

# Perform paired t-tests
def perform_paired_t_tests(df_results):
    metrics = ['MAP', 'Precision@10', 'DCG@10']
    t_test_results = {}

    for metric in metrics:
        bm25_scores = df_results[f'BM25_{metric}'].dropna()
        jm_lm_scores = df_results[f'JM_LM_{metric}'].dropna()
        my_prm_scores = df_results[f'My_PRM_{metric}'].dropna()

        # Ensure the scores are aligned by the same topic
        common_indices = bm25_scores.index.intersection(jm_lm_scores.index).intersection(my_prm_scores.index)
        bm25_scores = bm25_scores.loc[common_indices]
        jm_lm_scores = jm_lm_scores.loc[common_indices]
        my_prm_scores = my_prm_scores.loc[common_indices]

        t_stat_bm25_jm_lm, p_value_bm25_jm_lm = ttest_rel(bm25_scores, jm_lm_scores)
        t_stat_bm25_my_prm, p_value_bm25_my_prm = ttest_rel(bm25_scores, my_prm_scores)
        t_stat_jm_lm_my_prm, p_value_jm_lm_my_prm = ttest_rel(jm_lm_scores, my_prm_scores)

        t_test_results[metric] = {
            'BM25_vs_JM_LM': {'t_stat': t_stat_bm25_jm_lm, 'p_value': p_value_bm25_jm_lm},
            'BM25_vs_My_PRM': {'t_stat': t_stat_bm25_my_prm, 'p_value': p_value_bm25_my_prm},
            'JM_LM_vs_My_PRM': {'t_stat': t_stat_jm_lm_my_prm, 'p_value': p_value_jm_lm_my_prm}
        }

    return t_test_results
# Load the evaluation results and perform paired t-tests
relevance_judgements = load_relevance_judgements('C:/Users/s4021/OneDrive/桌面/Machine-learning-for-NLP/EvaluationBenchmark')
# Load PRM relevance judgments
prm_rankings = load_prm_relevance_judgements('C:/Users/s4021/OneDrive/桌面/Machine-learning-for-NLP/Ranking_Output/PRM_Output/PRM_Training_benchmark')

# Load the rankings for BM25, JM_LM, and My_PRM
bm25_rankings = load_all_rankings('C:/Users/s4021/OneDrive/桌面/Machine-learning-for-NLP/Ranking_Output/BM25_Output')
jm_lm_rankings = load_all_rankings('C:/Users/s4021/OneDrive/桌面/Machine-learning-for-NLP/Ranking_Output/JM_LM_Output')


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

# Perform paired t-tests
t_test_results = perform_paired_t_tests(evaluation_results)

# Print t-test results
for metric, comparisons in t_test_results.items():
    print(f"{metric} Paired T-Test Results:")
    for comparison, result in comparisons.items():
        print(f"  {comparison}:")
        print(f"    t-statistic: {result['t_stat']}")
        print(f"    p-value: {result['p_value']}")

# Save the t-test results to a file
with open('t_test_results.txt', 'w') as f:
    for metric, comparisons in t_test_results.items():
        f.write(f"{metric} Paired T-Test Results:\n")
        for comparison, result in comparisons.items():
            f.write(f"  {comparison}:\n")
            f.write(f"    t-statistic: {result['t_stat']}\n")
            f.write(f"    p-value: {result['p_value']}\n")

# Recommendations based on t-test results
recommendations = []
for metric, comparisons in t_test_results.items():
    for comparison, result in comparisons.items():
        if result['p_value'] < 0.05:
            recommendations.append(f"{metric}: {comparison} shows a significant difference (p < 0.05)")

if recommendations:
    print("\nRecommendations based on t-test results:")
    for recommendation in recommendations:
        print(recommendation)
else:
    print("\nNo significant differences found in the paired t-tests.")
