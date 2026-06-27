import pandas as pd
from src.recommendation.intelligent_search import intelligent_search


def evaluate_ranking_output(expected_row, retrieved_candidates, recommendations, k=10):
    candidate_count = len(retrieved_candidates)
    top_k = recommendations.head(k)

    if candidate_count == 0 or len(top_k) == 0:
        return {
            "query": expected_row["query"],
            "candidate_count": candidate_count,
            "avg_candidate_quality": 0.0,
            "avg_top10_quality": 0.0,
            "quality_lift": 0.0,
            "top1_intrinsic_quality": 0.0,
            "empty_ranking": 1
        }

    avg_candidate_quality = retrieved_candidates["intrinsic_quality"].mean()
    avg_top10_quality = top_k["intrinsic_quality"].mean()
    quality_lift = avg_top10_quality - avg_candidate_quality
    top1_intrinsic_quality = top_k.iloc[0]["intrinsic_quality"]

    return {
        "query": expected_row["query"],
        "candidate_count": candidate_count,
        "avg_candidate_quality": avg_candidate_quality,
        "avg_top10_quality": avg_top10_quality,
        "quality_lift": quality_lift,
        "top1_intrinsic_quality": top1_intrinsic_quality,
        "empty_ranking": 0
    }


def run_ranking_evaluation_pipeline(eval_queries_path, products_df, k=10):
    eval_df = pd.read_csv(eval_queries_path)

    results = []

    for _, expected_row in eval_df.iterrows():
        query = expected_row["query"]

        search_output = intelligent_search(
            product_df=products_df,
            query=query,
            use_llm=False
        )

        evaluation_row = evaluate_ranking_output(
            expected_row=expected_row,
            retrieved_candidates=search_output["retrieved_candidates"],
            recommendations=search_output["recommendations"],
            k=k
        )

        results.append(evaluation_row)

    ranking_evaluation_results = pd.DataFrame(results)

    return ranking_evaluation_results


if __name__ == "__main__":
    products_df = pd.read_csv("data/raw/products.csv")

    results_df = run_ranking_evaluation_pipeline(
        eval_queries_path="data/evaluation/evaluation_queries.csv",
        products_df=products_df,
        k=10
    )

    results_df.to_csv(
        "results/ranking_evaluation_results.csv",
        index=False
    )

    print(results_df.head())
    print("\nRanking evaluation completed.")