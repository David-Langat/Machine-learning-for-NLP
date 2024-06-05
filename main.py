# Import necessary libraries
import bm25
import pandas as pd
import sys
import os
from parse import parse_query as pq, get_stopwords
from parse import parse_documents as pdoc
from jelinek_mercer_smoothing import jm_lm
from prm import retrieve_bm25, generate_w5_scores, create_prm_benchmark
from evaluate import load_relevance_judgements, load_all_rankings, load_prm_rankings, evaluate_models_with_prm, perform_ttest
from bm25 import perform_bm25
# Main script execution
if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        sys.stderr.write("USAGE: %s <coll-file>\n" % sys.argv[0])
        sys.exit()

    # Set the input path based on the provided argument
    inputpath = (os.getcwd() + sys.argv[1])  # Assuming the data is in a folder in the same directory as this file

    # Define the query file
    query_file = 'the50Queries.txt'

    # Parse queries and documents
    collection_of_queries = pq(get_stopwords(), query_file)
    data_collection = pdoc(get_stopwords(), inputpath)

    #Calculate BM25 scores
    perform_bm25(collection_of_queries, data_collection)

    #Calculate JM scores
    jm_lm(collection_of_queries,data_collection)

    # Retrieve BM25 scores and generate PRM benchmark
    retrieve_bm25(collection_of_queries, data_collection)
    create_prm_benchmark()
    generate_w5_scores(data_collection)

    # Define paths for relevance judgments and model rankings
    script_dir = os.path.dirname(os.path.abspath(__file__))
    relevance_judgements_path = os.path.join(script_dir, 'EvaluationBenchmark')
    prm_rankings_path = os.path.join(script_dir, 'Ranking_Output', 'PRM_Output', 'PRM_Test_Ranks')
    bm25_rankings_path = os.path.join(script_dir, 'Ranking_Output', 'BM25_Output')
    jm_lm_rankings_path = os.path.join(script_dir, 'Ranking_Output', 'JM_LM_Output')

    # Load relevance judgments and model rankings
    relevance_judgements = load_relevance_judgements(relevance_judgements_path)
    prm_rankings = load_prm_rankings(prm_rankings_path)
    bm25_rankings = load_all_rankings(bm25_rankings_path)
    jm_lm_rankings = load_all_rankings(jm_lm_rankings_path)

    # Evaluate the models
    evaluation_results = evaluate_models_with_prm(relevance_judgements, bm25_rankings, jm_lm_rankings, prm_rankings)

    # Create tables for MAP, Precision@10, and DCG@10
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

    # Save tables to CSV files
    map_table.to_csv('map_table.csv', index=False)
    precision_table.to_csv('precision_table.csv', index=False)
    dcg_table.to_csv('dcg_table.csv', index=False)

    # Perform paired t-tests for MAP
    t_statistic_bm25_jm_lm_map, p_value_bm25_jm_lm_map, sig_bm25_jm_lm_map = perform_ttest(
        evaluation_results['BM25_MAP'].iloc[:-1], evaluation_results['JM_LM_MAP'].iloc[:-1], 'BM25', 'JM_LM'
    )
    t_statistic_bm25_my_prm_map, p_value_bm25_my_prm_map, sig_bm25_my_prm_map = perform_ttest(
        evaluation_results['BM25_MAP'].iloc[:-1], evaluation_results['My_PRM_MAP'].iloc[:-1], 'BM25', 'My_PRM'
    )
    t_statistic_jm_lm_my_prm_map, p_value_jm_lm_my_prm_map, sig_jm_lm_my_prm_map = perform_ttest(
        evaluation_results['JM_LM_MAP'].iloc[:-1], evaluation_results['My_PRM_MAP'].iloc[:-1], 'JM_LM', 'My_PRM'
    )

    # Perform paired t-tests for Precision@10
    t_statistic_bm25_jm_lm_prec10, p_value_bm25_jm_lm_prec10, sig_bm25_jm_lm_prec10 = perform_ttest(
        evaluation_results['BM25_Precision@10'].iloc[:-1], evaluation_results['JM_LM_Precision@10'].iloc[:-1], 'BM25', 'JM_LM'
    )
    t_statistic_bm25_my_prm_prec10, p_value_bm25_my_prm_prec10, sig_bm25_my_prm_prec10 = perform_ttest(
        evaluation_results['BM25_Precision@10'].iloc[:-1], evaluation_results['My_PRM_Precision@10'].iloc[:-1], 'BM25', 'My_PRM'
    )
    t_statistic_jm_lm_my_prm_prec10, p_value_jm_lm_my_prm_prec10, sig_jm_lm_my_prm_prec10 = perform_ttest(
        evaluation_results['JM_LM_Precision@10'].iloc[:-1], evaluation_results['My_PRM_Precision@10'].iloc[:-1], 'JM_LM', 'My_PRM'
    )

    # Perform paired t-tests for DCG@10
    t_statistic_bm25_jm_lm_dcg10, p_value_bm25_jm_lm_dcg10, sig_bm25_jm_lm_dcg10 = perform_ttest(
        evaluation_results['BM25_DCG@10'].iloc[:-1], evaluation_results['JM_LM_DCG@10'].iloc[:-1], 'BM25', 'JM_LM'
    )
    t_statistic_bm25_my_prm_dcg10, p_value_bm25_my_prm_dcg10, sig_bm25_my_prm_dcg10 = perform_ttest(
        evaluation_results['BM25_DCG@10'].iloc[:-1], evaluation_results['My_PRM_DCG@10'].iloc[:-1], 'BM25', 'My_PRM'
    )
    t_statistic_jm_lm_my_prm_dcg10, p_value_jm_lm_my_prm_dcg10, sig_jm_lm_my_prm_dcg10 = perform_ttest(
        evaluation_results['JM_LM_DCG@10'].iloc[:-1], evaluation_results['My_PRM_DCG@10'].iloc[:-1], 'JM_LM', 'My_PRM'
    )

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

