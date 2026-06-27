import pandas as pd
from src.recommendation.intelligent_search import intelligent_search


LABEL_NORMALIZATION = {
    "lipstick": "lipsticks",
    "sunscreen": "sunscreens",
    "perfume": "perfumes",
    "handbag": "handbags",
    "hoodie": "hoodies",
    "trouser": "trousers",
    "sunglass": "sunglasses",
    "formal shirts": "shirts"
}


def normalize_value(value):
    if value is None:
        return None

    value = str(value).strip().lower()

    if value in ["none", "nan", "default", ""]:
        return None

    value = LABEL_NORMALIZATION.get(value, value)

    return value


def get_acceptable_subcategories(expected_subcategory):
    expected = normalize_value(expected_subcategory)

    if expected is None:
        return None

    if "/" in expected:
        return [
            normalize_value(item)
            for item in expected.split("/")
        ]

    return [expected]


def evaluate_retrieval_output(expected_row, retrieved_candidates):

    expected_category = normalize_value(
        expected_row["expected_category"]
    )

    acceptable_subcategories = get_acceptable_subcategories(
        expected_row["expected_subcategory"]
    )

    candidate_count = len(retrieved_candidates)

    if candidate_count == 0:
        return {
            "query": expected_row["query"],
            "expected_category": expected_category,
            "expected_subcategory": expected_row["expected_subcategory"],
            "candidate_count": 0,
            "category_match_rate": 0.0,
            "subcategory_match_rate": 0.0,
            "empty_retrieval": 1
        }

    normalized_categories = retrieved_candidates["category"].apply(
        normalize_value
    )

    normalized_subcategories = retrieved_candidates["sub_category"].apply(
        normalize_value
    )

    if expected_category is not None:
        category_match_rate = (
            normalized_categories == expected_category
        ).mean()
    else:
        category_match_rate = None

    if acceptable_subcategories is not None:
        subcategory_match_rate = (
            normalized_subcategories.isin(acceptable_subcategories)
        ).mean()
    else:
        subcategory_match_rate = None

    return {
        "query": expected_row["query"],
        "expected_category": expected_category,
        "expected_subcategory": expected_row["expected_subcategory"],
        "acceptable_subcategories": acceptable_subcategories,
        "candidate_count": candidate_count,
        "category_match_rate": category_match_rate,
        "subcategory_match_rate": subcategory_match_rate,
        "empty_retrieval": 0
    }


def run_retrieval_evaluation_pipeline(eval_queries_path, products_df):
    eval_df = pd.read_csv(eval_queries_path)

    results = []

    for _, expected_row in eval_df.iterrows():
        query = expected_row["query"]

        search_output = intelligent_search(
            product_df=products_df,
            query=query,
            use_llm=False
        )

        retrieved_candidates = search_output["retrieved_candidates"]

        evaluation_row = evaluate_retrieval_output(
            expected_row=expected_row,
            retrieved_candidates=retrieved_candidates
        )

        results.append(evaluation_row)

    retrieval_evaluation_results = pd.DataFrame(results)

    return retrieval_evaluation_results


if __name__ == "__main__":
    products_df = pd.read_csv("data/raw/products.csv")

    results_df = run_retrieval_evaluation_pipeline(
        eval_queries_path="data/evaluation/evaluation_queries.csv",
        products_df=products_df
    )

    results_df.to_csv(
        "results/retrieval_evaluation_results.csv",
        index=False
    )

    print(results_df.head())
    print("\nRetrieval evaluation completed.")