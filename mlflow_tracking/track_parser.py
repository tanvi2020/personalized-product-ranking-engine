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

from src.evaluation.parser_evaluation import run_parser_evaluation_pipeline


# -----------------------------------
# Paths
# -----------------------------------
PRODUCTS_PATH = "data/raw/products.csv"
EVAL_QUERIES_PATH = "data/evaluation/evaluation_queries.csv"
OUTPUT_PATH = "results/parser_evaluation_results.csv"


# -----------------------------------
# Load data
# -----------------------------------
products_df = pd.read_csv(PRODUCTS_PATH)


# -----------------------------------
# Run parser evaluation
# -----------------------------------
results_df = run_parser_evaluation_pipeline(
    eval_queries_path=EVAL_QUERIES_PATH,
    products_df=products_df
)

os.makedirs("results", exist_ok=True)
results_df.to_csv(OUTPUT_PATH, index=False)


# -----------------------------------
# Calculate metrics
# -----------------------------------
avg_category_score = results_df["category_score"].mean()
avg_subcategory_score = results_df["subcategory_score"].mean()
avg_persona_score = results_df["persona_score"].mean()
avg_use_case_score = results_df["use_case_score"].mean()
avg_max_price_score = results_df["max_price_score"].mean()


# -----------------------------------
# MLflow tracking
# -----------------------------------
mlflow.set_experiment("parser_experiments")

with mlflow.start_run(run_name="baseline_v1_current_system"):

    # Parameters = design choices
    mlflow.log_param("parser_type", "hybrid_parser")
    mlflow.log_param("rule_parser_enabled", True)
    mlflow.log_param("llm_enabled", False)
    mlflow.log_param("taxonomy_matching_enabled", True)
    mlflow.log_param("validation_layer_enabled", True)
    mlflow.log_param("catalog_size", len(products_df))

    # Metrics = measured results
    mlflow.log_metric("avg_category_score", avg_category_score)
    mlflow.log_metric("avg_subcategory_score", avg_subcategory_score)
    mlflow.log_metric("avg_persona_score", avg_persona_score)
    mlflow.log_metric("avg_use_case_score", avg_use_case_score)
    mlflow.log_metric("avg_max_price_score", avg_max_price_score)

    # Artifact = proof/output file
    mlflow.log_artifact(OUTPUT_PATH)

print("Parser baseline tracked successfully in MLflow.")