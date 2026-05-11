import numpy as np
from sklearn.preprocessing import minmax_scale
from src.config.parameters import PERSONA_PARAMS


def ranking(product_df, user):
    df = product_df.copy()

    budget = user.avg_budget
    persona = user.persona_type

    # Dynamic weights from search mode
    budget_weight = user.get("budget_weight", None)
    quality_weight = user.get("quality_weight", None)

    # Fallback for old user-based recommendation mode
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

    # Use persona only for price sensitivity parameters
    if persona == "Budget":
        params = PERSONA_PARAMS["Budget"]
    elif persona == "Quality":
        params = PERSONA_PARAMS["Quality"]
    elif persona == "Balanced":
        params = PERSONA_PARAMS["Quality"]
    else:
        raise ValueError(f"Unknown persona type: {persona}")

    # Price score
    df["error"] = (df["price"] - budget) / budget

    df["price_score"] = np.where(
        df["error"] <= 0,
        np.exp(-np.abs(df["error"]) / params["b_low"]),
        np.exp(-np.abs(df["error"]) / params["b_high"])
    )

    # Rating score
    df["rating_score"] = (df["rating"] - 1) / 4

    # Purchase score
    df["purchase_log"] = np.log1p(df["num_purchases"])
    df["purchase_score"] = minmax_scale(df["purchase_log"])

    # Trust score
    k = 20
    df["confidence_score"] = df["review_count"] / (df["review_count"] + k)
    df["trusted_rating_score"] = df["rating_score"] * df["confidence_score"]

    # Trust-adjusted purchase score
    df["trusted_adjusted_purchase_score"] = (
        df["purchase_score"] * (df["trusted_rating_score"] ** 2)
    )

    # Components
    df["budget_component"] = df["price_score"]

    df["quality_component"] = np.where(
        df["rating"].isna(),
        0.2 * df["purchase_score"],   # weak fallback if rating missing
        0.7 * df["trusted_rating_score"] + 0.3 * df["trusted_adjusted_purchase_score"]
    )

    # Final dynamic score
    df["final_score"] = (
        budget_weight * df["budget_component"] +
        quality_weight * df["quality_component"]
    )

    return df.sort_values(by="final_score", ascending=False)