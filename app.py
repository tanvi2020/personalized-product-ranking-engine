import streamlit as st
import pandas as pd
import os
import sys

# --------------------------------------------------
# FIX PATH (so Python can find src/)
# --------------------------------------------------
project_root = os.path.abspath(os.path.dirname(__file__))

if project_root not in sys.path:
    sys.path.append(project_root)

# --------------------------------------------------
# IMPORT BACKEND LOGIC
# --------------------------------------------------
from src.recommendation.recommender import (
    get_recommendation_result,
    recommend_from_query
)

from src.agent.query_parser import parse_query

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
products_df = pd.read_csv("data/raw/products.csv")
users_df = pd.read_csv("data/raw/users.csv")

# --------------------------------------------------
# UI TITLE
# --------------------------------------------------
st.title("🛍️ Product Recommendation System")

# --------------------------------------------------
# MODE SELECTION
# --------------------------------------------------
mode = st.radio(
    "Choose Recommendation Mode",
    ["User-Based", "Search-Based"]
)

# --------------------------------------------------
# COMMON INPUT
# --------------------------------------------------
top_k = st.slider("Number of Recommendations", 3, 20, 10)

# ==================================================
# USER-BASED MODE
# ==================================================
if mode == "User-Based":

    st.subheader("User-Based Recommendation")

    user_id = st.selectbox(
        "Select User ID",
        users_df["user_id"].unique()
    )

    category_options = ["All"] + sorted(products_df["category"].unique().tolist())

    category = st.selectbox("Select Category", category_options)

    max_price = st.number_input(
        "Maximum Price",
        min_value=0,
        max_value=int(products_df["price"].max()),
        value=int(products_df["price"].max()),
        step=500
    )

    if st.button("Get Recommendations"):

        result = get_recommendation_result(
            products_df,
            users_df,
            user_id=user_id,
            top_k=top_k,
            category=category,
            max_price=max_price
        )

        summary = result["summary"]
        recs = result["recommendations"]

        st.subheader("User Summary")

        st.write(f"Persona: {summary['persona_type']}")
        st.write(f"Budget: {summary['avg_budget']}")
        st.write(f"Avg Recommended Price: {summary['avg_recommended_price']:.2f}")
        st.write(f"Avg Intrinsic Quality: {summary['avg_intrinsic_quality']:.3f}")
        st.write(f"Missing Ratings: {summary['missing_rating_count']} / {summary['total_recommendations']}")

        st.subheader("Recommended Products")

        if recs.empty:
            st.warning("No products found.")
        else:
            st.dataframe(recs[[
                "product_id",
                "brand",
                "category",
                "sub_category",
                "price",
                "final_score",
                "trusted_rating_score",
                "purchase_score"
            ]])

# ==================================================
# SEARCH-BASED MODE (AGENT)
# ==================================================
else:

    st.subheader("Search-Based Recommendation (Agent Mode)")

    query = st.text_input(
        "Enter your search query",
        placeholder="e.g. cheap sneakers under 3000"
    )

    if st.button("Search Products"):

        if query.strip() == "":
            st.warning("Please enter a query.")

        else:
            # --------------------------
            # STEP 1: PARSE QUERY
            # --------------------------
            parsed_query = parse_query(query)

            st.subheader("Parsed Query")
            st.write(parsed_query)

            # --------------------------
            # HANDLE MISSING INFO
            # --------------------------
            if parsed_query ["max_price"] is None:
                st.warning("Please mention a price limit, e.g. 'under 3000'.")
                st.stop()

            if parsed_query ["category"] is None:
                st.warning("Could not detect category clearly.")

            # --------------------------
            # STEP 2: GET RECOMMENDATIONS
            # --------------------------
            recs =recommend_from_query(
                    products_df,
                    category=parsed_query["category"],
                    sub_category=parsed_query["sub_category"],
                    max_price=parsed_query["max_price"],
                    persona_type=parsed_query["persona"],
                    use_case=parsed_query["use_case"],
                    budget_weight=parsed_query["budget_weight"],
                    quality_weight=parsed_query["quality_weight"],
                    top_k=10
                )

            # --------------------------
            # STEP 3: CREATE SUMMARY
            # --------------------------
            summary = {
                "persona_type": parsed_query["persona"],
                "avg_budget": parsed_query["max_price"],
                "avg_recommended_price": float(recs["price"].mean()) if not recs.empty else 0,
                "avg_intrinsic_quality": float(recs["intrinsic_quality"].mean()) if not recs.empty else 0,
                "missing_rating_count": int(recs["trusted_rating_score"].isna().sum()) if not recs.empty else 0,
                "total_recommendations": int(len(recs))
            }

            st.subheader("Search Summary")

            st.write(f"Detected Persona: {summary['persona_type']}")
            st.write(f"Detected Budget: {summary['avg_budget']}")
            st.write(f"Avg Price: {summary['avg_recommended_price']:.2f}")
            st.write(f"Avg Quality: {summary['avg_intrinsic_quality']:.3f}")
            st.write(f"Missing Ratings: {summary['missing_rating_count']} / {summary['total_recommendations']}")

            # --------------------------
            # STEP 4: SHOW RESULTS
            # --------------------------
            st.subheader("Recommended Products")

            if recs.empty:
                st.warning("No products found.")
            else:
                st.dataframe(recs[[
                    "product_id",
                    "brand",
                    "category",
                    "sub_category",
                    "price",
                    "final_score",
                    "trusted_rating_score",
                    "purchase_score"
                ]])

            if len(recs) < top_k:
                st.info(
                f"Only {len(recs)} products matched your filters, so showing fewer than requested."
                )