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

from src.evaluation.ranking_evaluation import run_ranking_evaluation_pipeline


# -----------------------------------
# Paths
# -----------------------------------
PRODUCTS_PATH = "data/raw/products.csv"
EVAL_QUERIES_PATH = "data/evaluation/evaluation_queries.csv"
OUTPUT_PATH = "results/ranking_evaluation_results.csv"


# -----------------------------------
# Load data
# -----------------------------------
products_df = pd.read_csv(PRODUCTS_PATH)


# -----------------------------------
# Run ranking evaluation
# -----------------------------------
results_df = run_ranking_evaluation_pipeline(
    eval_queries_path=EVAL_QUERIES_PATH,
    products_df=products_df,
    k=10
)

os.makedirs("results", exist_ok=True)
results_df.to_csv(OUTPUT_PATH, index=False)


# -----------------------------------
# Calculate metrics
# -----------------------------------
avg_candidate_quality = results_df["avg_candidate_quality"].mean()
avg_top10_quality = results_df["avg_top10_quality"].mean()
avg_quality_lift = results_df["quality_lift"].mean()
avg_top1_intrinsic_quality = results_df["top1_intrinsic_quality"].mean()
empty_ranking_rate = results_df["empty_ranking"].mean()


# -----------------------------------
# MLflow tracking
# -----------------------------------
mlflow.set_experiment("ranking_experiments")

with mlflow.start_run(run_name="baseline_v1_current_system"):

    # Parameters = ranking design choices
    mlflow.log_param("ranking_type", "rule_based_scoring")
    mlflow.log_param("catalog_size", len(products_df))
    mlflow.log_param("top_k", 10)
    mlflow.log_param("confidence_k", 20)
    mlflow.log_param("quality_component_weight", 0.7)
    mlflow.log_param("purchase_score_weight", 0.3)
    mlflow.log_param("budget_soft_gate_enabled", True)
    mlflow.log_param("use_case_boost_enabled", True)
    mlflow.log_param("use_case_boost_weight", 0.15)
    mlflow.log_param("llm_enabled", False)

    # Metrics = ranking performance
    mlflow.log_metric("avg_candidate_quality", avg_candidate_quality)
    mlflow.log_metric("avg_top10_quality", avg_top10_quality)
    mlflow.log_metric("avg_quality_lift", avg_quality_lift)
    mlflow.log_metric("avg_top1_intrinsic_quality", avg_top1_intrinsic_quality)
    mlflow.log_metric("empty_ranking_rate", empty_ranking_rate)

    # Artifact = proof/output file
    mlflow.log_artifact(OUTPUT_PATH)

print("Ranking baseline tracked successfully in MLflow.")