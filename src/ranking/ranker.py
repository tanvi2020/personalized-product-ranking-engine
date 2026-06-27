import numpy as np
from sklearn.preprocessing import minmax_scale
from src.config.parameters import PERSONA_PARAMS, USE_CASE_SUBCATEGORY_MAP


def ranking(product_df, user):
    df = product_df.copy()

    budget = user.avg_budget
    persona = user.persona_type

    budget_weight = user.get("budget_weight", None)
    quality_weight = user.get("quality_weight", None)

    if budget_weight is None or quality_weight is None:
        if persona == "Budget":
            budget_weight = 0.8
            quality_weight = 0.2
        elif persona == "Quality":
            budget_weight = 0.2
            quality_weight = 0.8
        elif persona == "Balanced":
            budget_weight = 0.5
            quality_weight = 0.5
        else:
            raise ValueError(f"Unknown persona type: {persona}")

    if persona == "Budget":
        params = PERSONA_PARAMS["Budget"]
    elif persona == "Quality":
        params = PERSONA_PARAMS["Quality"]
    elif persona == "Balanced":
        params = PERSONA_PARAMS["Quality"]
    else:
        raise ValueError(f"Unknown persona type: {persona}")

    df["error"] = (df["price"] - budget) / budget

    df["price_score"] = np.where(
        df["error"] <= 0,
        np.exp(-np.abs(df["error"]) / params["b_low"]),
        np.exp(-np.abs(df["error"]) / params["b_high"])
    )

    df["rating_score"] = (df["rating"] - 1) / 4

    df["purchase_log"] = np.log1p(df["num_purchases"])

    if df["purchase_log"].nunique() <= 1:
        df["purchase_score"] = 0.0
    else:
        df["purchase_score"] = minmax_scale(df["purchase_log"])

    k = 20
    df["confidence_score"] = df["review_count"] / (df["review_count"] + k)

    df["trusted_rating_score"] = df["rating_score"] * df["confidence_score"]

    df["popularity_confidence"] = 0.5 + 0.5 * df["purchase_score"]

    df["quality_component"] = np.where(
        df["rating"].isna(),
        0.0,
        df["trusted_rating_score"] * df["popularity_confidence"]
    )

    df["budget_component"] = df["price_score"]

    use_case = user.get("use_case", None)
    category = user.get("category", None)

    df["use_case_match_score"] = 0.0

    preferred_subcategories = (
        USE_CASE_SUBCATEGORY_MAP
        .get(use_case, {})
        .get(category, [])
    )

    if preferred_subcategories:
        df["use_case_match_score"] = np.where(
            df["sub_category"].isin(preferred_subcategories),
            1.0,
            0.0
        )

    # NEW LOGIC:
    # Quality/popularity form the main relevance score.
    # Budget now acts as a soft gate instead of dominating directly.
    df["base_relevance_score"] = (
        0.7 * df["quality_component"] +
        0.3 * df["purchase_score"]
    )

    df["final_score"] = (
        df["base_relevance_score"] *
        (0.5 + 0.5 * df["budget_component"])
    )

    if use_case is not None:
        df["final_score"] = df["final_score"] + (
            0.15 * df["use_case_match_score"]
        )

    def build_recommendation_reason(row):
        reasons = []

        if row.get("use_case_match_score", 0) == 1:
            reasons.append("matches your search intent")

        if row.get("price_score", 0) >= 0.75:
            reasons.append("fits your budget well")

        if row.get("trusted_rating_score", 0) >= 0.50:
            reasons.append("has strong trusted ratings")

        if row.get("purchase_score", 0) >= 0.70:
            reasons.append("is popular among users")

        if not reasons:
            reasons.append("ranked best based on overall score")

        return "Recommended because it " + ", ".join(reasons) + "."

    df["recommendation_reason"] = df.apply(build_recommendation_reason, axis=1)

    return df.sort_values(by="final_score", ascending=False)