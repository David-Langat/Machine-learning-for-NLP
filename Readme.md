# Information Retrieval System

This project provides a robust framework for exploring and evaluating various information retrieval (IR) techniques. It features a command-line interface for executing different ranking algorithms, a comprehensive evaluation suite, and a modular architecture for easy extension. The system is designed to serve as both a practical tool for IR experimentation and an educational resource for understanding the underlying concepts.

## Core Features

- **Multiple Ranking Models:** Implements and compares three distinct ranking algorithms:
    - BM25 (Best Match 25)
    - Jelinek-Mercer Smoothing
    - Pseudo-Relevance Feedback (PRF)
- **End-to-End NLP Pipeline:** Includes a complete pipeline for processing raw text data, featuring:
    - Tokenization
    - Stop-word removal
    - Multiple stemming algorithms (Porter, Porter2, Lovins, Paice-Husk)
- **Comprehensive Evaluation:** Provides a rigorous evaluation framework that calculates standard IR metrics:
    - Mean Average Precision (MAP)
    - Precision@10
    - Discounted Cumulative Gain (DCG@10)
- **Statistical Significance Testing:** Uses paired t-tests to determine if the performance differences between models are statistically significant.
- **Modular Design:** Built with Object-Oriented principles and design patterns (e.g., Strategy pattern for file handling) to ensure a maintainable and extensible codebase.

## NLP Pipeline

The NLP pipeline is responsible for transforming raw text from documents and queries into a structured format suitable for the ranking algorithms. This process involves several stages:

1.  **Tokenization:** The raw text is broken down into individual words or tokens. Punctuation and digits are removed during this step.
2.  **Stop-word Removal:** Common words that provide little semantic value (e.g., "the", "a", "is") are removed. The list of stop words is sourced from `common-english-words.txt`.
3.  **Stemming:** Words are reduced to their root form to ensure that different variations of a word are treated as the same term. This project includes several stemming algorithms, with **Porter2** being the default:
    - **Porter2 (Snowball):** An improvement over the original Porter stemmer, offering better performance and accuracy.
    - **Porter:** The original stemming algorithm, widely used in IR.
    - **Lovins:** A single-pass, context-sensitive stemmer.
    - **Paice-Husk:** A rule-based, iterative stemmer.

The final output of the pipeline is a Bag-of-Words (BoW) representation of the documents and queries, which is then used by the ranking algorithms.

## Ranking Algorithms

### BM25

BM25 is a ranking function based on the probabilistic retrieval framework. It ranks documents by estimating the probability that a document is relevant to a given query. The score is calculated based on the query terms present in each document, taking into account term frequency (TF) and inverse document frequency (IDF). The key parameters of the BM25 formula are:

-   `k1`: Controls the term frequency scaling.
-   `b`: Controls the document length normalization.
-   `k2`: Controls the query term frequency scaling.

### Jelinek-Mercer Smoothing

Jelinek-Mercer smoothing is a language modeling approach to information retrieval. It estimates the probability of a query being generated from a document's language model. To avoid issues with zero probabilities for terms that do not appear in a document, it uses a smoothing technique that linearly interpolates between the document's language model and the collection's language model. The `lambda` parameter controls the balance between these two models.

### Pseudo-Relevance Feedback (PRF)

Pseudo-Relevance Feedback is a query expansion technique that aims to improve retrieval performance by automatically reformulating the query. The process is as follows:

1.  The initial query is run against the document collection using a standard ranking algorithm (in this case, BM25).
2.  The top-ranked documents are assumed to be relevant.
3.  The terms from these "pseudo-relevant" documents are used to expand the original query.
4.  The expanded query is then used to re-rank the documents, hopefully leading to a more accurate result set.

## Evaluation

The `evaluate.py` module provides a comprehensive framework for evaluating the performance of the ranking models. It uses the following metrics:

-   **Mean Average Precision (MAP):** The mean of the average precision scores for each query. Average precision rewards models that rank relevant documents higher.
-   **Precision@10:** The proportion of relevant documents in the top 10 results.
-   **Discounted Cumulative Gain (DCG@10):** A measure of ranking quality that gives more weight to relevant documents that appear higher in the results list.

In addition to these metrics, the evaluation module performs paired t-tests to determine if the differences in performance between the models are statistically significant.

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/David-Aires/Machine-learning-for-NLP.git
    ```
2.  **Install dependencies:**
    ```bash
    pip install pandas numpy scipy
    ```
3.  **Run the main script:**
    ```bash
    python main.py <path_to_data_collection>
    ```
    Replace `<path_to_data_collection>` with the relative path to the directory containing the document collections. For example:
    ```bash
    python main.py /Data
    ```

The script will then execute the ranking algorithms, evaluate their performance, and print the results to the console. The evaluation results and t-test results will also be saved to CSV files in the root directory.
