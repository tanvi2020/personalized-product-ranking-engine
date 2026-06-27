import os
import sys
import pandas as pd
import mlflow

# -----------------------------------
# Fix project import path
# -----------------------------------
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if project_root not in sys.path:
    sys.path.append(project_root)

from src.evaluation.retrieval_evaluation import run_retrieval_evaluation_pipeline


# -----------------------------------
# Paths
# -----------------------------------
PRODUCTS_PATH = "data/raw/products.csv"
EVAL_QUERIES_PATH = "data/evaluation/evaluation_queries.csv"
OUTPUT_PATH = "results/retrieval_evaluation_results.csv"


# -----------------------------------
# Load data
# -----------------------------------
products_df = pd.read_csv(PRODUCTS_PATH)


# -----------------------------------
# Run retrieval evaluation
# -----------------------------------
results_df = run_retrieval_evaluation_pipeline(
    eval_queries_path=EVAL_QUERIES_PATH,
    products_df=products_df
)

os.makedirs("results", exist_ok=True)
results_df.to_csv(OUTPUT_PATH, index=False)


# -----------------------------------
# Calculate metrics
# -----------------------------------
avg_candidate_count = results_df["candidate_count"].mean()

avg_category_match_rate = results_df["category_match_rate"].dropna().mean()
avg_subcategory_match_rate = results_df["subcategory_match_rate"].dropna().mean()

empty_retrieval_rate = results_df["empty_retrieval"].mean()


# -----------------------------------
# MLflow tracking
# -----------------------------------
mlflow.set_experiment("retrieval_experiments")

with mlflow.start_run(run_name="baseline_v1_current_system"):

    # Parameters = retrieval design choices
    mlflow.log_param("retrieval_type", "rule_based_filtering")
    mlflow.log_param("catalog_size", len(products_df))
    mlflow.log_param("category_filter_enabled", True)
    mlflow.log_param("subcategory_filter_enabled", True)
    mlflow.log_param("subcategory_filter_min_candidates", 10)
    mlflow.log_param("price_relaxation_enabled", True)
    mlflow.log_param("taxonomy_matching_enabled", True)
    mlflow.log_param("llm_enabled", False)

    # Metrics = retrieval performance
    mlflow.log_metric("avg_candidate_count", avg_candidate_count)
    mlflow.log_metric("avg_category_match_rate", avg_category_match_rate)
    mlflow.log_metric("avg_subcategory_match_rate", avg_subcategory_match_rate)
    mlflow.log_metric("empty_retrieval_rate", empty_retrieval_rate)

    # Artifact = proof/output file
    mlflow.log_artifact(OUTPUT_PATH)

print("Retrieval baseline tracked successfully in MLflow.")