from src.recommendation.intelligent_search import intelligent_search
import pandas as pd


def normalize_value(value):
    if value is None:
        return None

    value = str(value).strip()

    if value.lower() in ["none", "nan", "default", ""]:
        return None

    return value.lower()


def score_category(expected, predicted):
    expected = normalize_value(expected)
    predicted = normalize_value(predicted)

    if expected is None and predicted is None:
        return 1.0

    if expected == predicted:
        return 1.0

    return 0.0


def score_persona(expected, predicted):
    expected = normalize_value(expected)
    predicted = normalize_value(predicted)

    if expected == predicted:
        return 1.0

    if expected is None or predicted is None:
        return 0.0

    if "balanced" in [expected, predicted]:
        return 0.5

    return 0.0


def score_max_price(expected, predicted):
    expected = normalize_value(expected)
    predicted = normalize_value(predicted)

    if expected is None and predicted is None:
        return 1.0

    if expected is None or predicted is None:
        return 0.0

    expected = float(expected)
    predicted = float(predicted)

    relative_error = abs(predicted - expected) / expected

    if relative_error <= 0.10:
        return 1.0
    elif relative_error <= 0.25:
        return 0.5
    else:
        return 0.0


SIMILAR_SUBCATEGORIES = [
    {"sneakers", "sports shoes"},
    {"heels", "sandals"},
    {"lipsticks", "lip color"},
    {"moisturizer", "skin cream", "face lotion"},
]


def score_subcategory(expected, predicted):
    expected = normalize_value(expected)
    predicted = normalize_value(predicted)

    if expected is None and predicted is None:
        return 1.0

    if expected is None or predicted is None:
        return 0.0

    if expected == predicted:
        return 1.0

    for group in SIMILAR_SUBCATEGORIES:
        if expected in group and predicted in group:
            return 0.5

    return 0.0


SIMILAR_USE_CASES = [
    {"running", "sports", "gym"},
    {"party wear", "fashion", "prom night"},
    {"daily wear", "daily use", "casual"},
    {"office", "formal"},
    {"winter", "cold weather"},
]


def score_use_case(expected, predicted):
    expected = normalize_value(expected)
    predicted = normalize_value(predicted)

    if expected is None and predicted is None:
        return 1.0

    if expected is None and predicted is not None:
        return 0.5

    if expected is not None and predicted is None:
        return 0.0

    if expected == predicted:
        return 1.0

    if expected in predicted or predicted in expected:
        return 0.5

    for group in SIMILAR_USE_CASES:
        if expected in group and predicted in group:
            return 0.5

    return 0.0


def evaluate_parser_output(expected_row, parsed_query):
    predicted_subcategory = (
        parsed_query.get("sub_category")
        or parsed_query.get("subcategory")
    )

    predicted_persona = (
        parsed_query.get("persona_type")
        or parsed_query.get("persona")
    )

    return {
        "query": expected_row["query"],

        "expected_category": expected_row["expected_category"],
        "predicted_category": parsed_query.get("category"),
        "category_score": score_category(
            expected_row["expected_category"],
            parsed_query.get("category")
        ),

        "expected_subcategory": expected_row["expected_subcategory"],
        "predicted_subcategory": predicted_subcategory,
        "subcategory_score": score_subcategory(
            expected_row["expected_subcategory"],
            predicted_subcategory
        ),

        "expected_persona": expected_row["expected_persona"],
        "predicted_persona": predicted_persona,
        "persona_score": score_persona(
            expected_row["expected_persona"],
            predicted_persona
        ),

        "expected_max_price": expected_row["expected_max_price"],
        "predicted_max_price": parsed_query.get("max_price"),
        "max_price_score": score_max_price(
            expected_row["expected_max_price"],
            parsed_query.get("max_price")
        ),

        "expected_use_case": expected_row["expected_use_case"],
        "predicted_use_case": parsed_query.get("use_case"),
        "use_case_score": score_use_case(
            expected_row["expected_use_case"],
            parsed_query.get("use_case")
        )
    }


def run_parser_evaluation_pipeline(
    eval_queries_path,
    products_df,
    use_llm=False
):
    eval_df = pd.read_csv(eval_queries_path)

    results = []

    for _, expected_row in eval_df.iterrows():
        query = expected_row["query"]

        search_output = intelligent_search(
            query=query,
            product_df=products_df,
            use_llm=use_llm
        )

        parsed_query = search_output["parsed_query"]

        evaluation_row = evaluate_parser_output(
            expected_row=expected_row,
            parsed_query=parsed_query
        )

        results.append(evaluation_row)

    parser_evaluation_results = pd.DataFrame(results)
    return parser_evaluation_results


if __name__ == "__main__":
    products_df = pd.read_csv("data/raw/products.csv")

    # Change this to False for rule-based parser evaluation.
    # Change this to True for hybrid LLM parser evaluation.
    USE_LLM = True

    results_df = run_parser_evaluation_pipeline(
        eval_queries_path="data/evaluation/evaluation_queries.csv",
        products_df=products_df,
        use_llm=USE_LLM
    )

    output_path = (
        "results/parser_evaluation_results_llm.csv"
        if USE_LLM
        else "results/parser_evaluation_results_rule_based.csv"
    )

    results_df.to_csv(output_path, index=False)

    print(results_df.head())
    print(f"\nParser evaluation completed. Saved to: {output_path}")