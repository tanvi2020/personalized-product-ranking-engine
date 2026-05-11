from src.ranking.ranker import ranking
import pandas as pd

def recommender(product_df, user_df, user_id, top_k=10, category=None, max_price=None):
    user_match = user_df[user_df["user_id"] == user_id]

    if user_match.empty:
        raise ValueError(f"User_id not found: {user_id}")

    user = user_match.iloc[0]

    candidates = filter_candidates(
        product_df,
        category=category,
        max_price=max_price
    )

    if candidates.empty:
        return user, candidates

    ranked_products = ranking(candidates, user)

    return user, ranked_products.head(top_k)


def summarize_recommendations(user, recs):
    return {
        "user_id": int(user["user_id"]),
        "persona_type": str(user["persona_type"]),
        "avg_budget": int(user["avg_budget"]),
        "avg_recommended_price": float(recs["price"].mean()),
        "avg_intrinsic_quality": float(recs["intrinsic_quality"].mean()),
        "missing_rating_count": int(recs["trusted_rating_score"].isna().sum()),
        "total_recommendations": int(len(recs))
    }

def get_recommendation_result(product_df, user_df, user_id, top_k=10, category=None, max_price=None):
    user, recs = recommender(
        product_df,
        user_df,
        user_id,
        top_k,
        category=category,
        max_price=max_price
    )

    summary = summarize_recommendations(user, recs)

    return {
        "user": user,
        "recommendations": recs,
        "summary": summary
    }


def filter_candidates(product_df, category=None, sub_category=None, min_price=None, max_price=None, use_case=None):
    candidates = product_df.copy()

    # 1. Filter by category
    if category is not None and category != "All":
        candidates = candidates[candidates["category"] == category]

    # 2. Use-case aware filtering
    if category == "Footwear" and use_case == "Sports":
        candidates = candidates[
            candidates["sub_category"].isin(["Sneakers", "Sports Shoes"])
        ]

    # 3. Normal sub-category filtering
    elif sub_category is not None:
        candidates = candidates[candidates["sub_category"] == sub_category]

    # 4. Filter by max price
    if max_price is not None:
        candidates = candidates[candidates["price"] <= max_price]

    # 5 Filter by min price
    if min_price is not None:
        candidates=candidates[candidates["price"] >= min_price]

    return candidates

def get_relaxation_multiplier(parsed_query):
    base_multiplier = 1.0
    if parsed_query["max_price"] is not None:
    
        if parsed_query["category"] in ["Footwear", "Clothing"]:
            base_multiplier += 0.1

        if parsed_query['budget_weight'] > parsed_query['quality_weight']:
            base_multiplier += 0.1
        if parsed_query['quality_weight'] > parsed_query['budget_weight']:
            base_multiplier += 0.3
    
    # The multiplier value should not be below 1.0 and above 1.5
    base_multiplier=max(1.0,min(base_multiplier,1.5))
    return base_multiplier # if max_price does not exist

def recommend_from_query(product_df, category=None, sub_category=None, min_price=None, max_price=None, persona_type="Budget", use_case=None,budget_weight=0.5,quality_weight=0.5, top_k=10):
     parsed_query = {
        "category": category,
        "sub_category": sub_category,
        "min_price": min_price,
        "max_price": max_price,
        "persona_type": persona_type,
        "use_case": use_case,
        "budget_weight": budget_weight,
        "quality_weight": quality_weight
    }

     relaxation_multiplier = get_relaxation_multiplier(parsed_query)

     relaxed_max_price = None
     if max_price is not None:
        relaxed_max_price = max_price * relaxation_multiplier

        if min_price is None:
            if budget_weight > quality_weight:
                min_price = None
            elif quality_weight > budget_weight:
                min_price = 0.4 * max_price
            else:
                min_price = 0.25 * max_price

     candidates = filter_candidates(
        product_df,
        category=category,
        sub_category=sub_category,
        min_price=min_price,
        max_price=relaxed_max_price,
        use_case=use_case
     )

     if candidates.empty:
        return candidates

     temporary_user = pd.Series({
        "user_id": -1,
        "persona_type": persona_type,
        "avg_budget": max_price if max_price is not None else product_df["price"].median(),
        "budget_weight": budget_weight,
        "quality_weight": quality_weight,
        "relaxation_multiplier": relaxation_multiplier,
        "relaxed_max_price": relaxed_max_price
    })

     ranked_products = ranking(candidates, temporary_user)
     print(f'max_price: {max_price}, Relaxation Multiplier: {relaxation_multiplier}, Relaxed Max Price: {relaxed_max_price}, Candidate Count: {len(candidates)}')
     print("query settings:")
     print("budget_weight:", budget_weight)
     print("quality_weight:", quality_weight)
     print("relaxation_multiplier:", relaxation_multiplier)
     print("min_price:", min_price)
     print("relaxed_max_price:", relaxed_max_price)
     print("candidate_count:", len(candidates))
     print(candidates[["product_id", "category", "sub_category", "price", "rating", "review_count", "num_purchases"]].sort_values("price").head(10))
     return ranked_products.head(top_k)
