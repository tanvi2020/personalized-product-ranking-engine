import streamlit as st
import pandas as pd
import os
import sys

# --------------------------------------------------
# FIX PATH
# --------------------------------------------------
project_root = os.path.abspath(os.path.dirname(__file__))

if project_root not in sys.path:
    sys.path.append(project_root)

# --------------------------------------------------
# IMPORT BACKEND LOGIC
# --------------------------------------------------
from src.recommendation.recommender import get_recommendation_result
from src.recommendation.intelligent_search import intelligent_search

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Product Search & Ranking System",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
products_df = pd.read_csv("data/raw/products.csv")
users_df = pd.read_csv("data/raw/users.csv")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("🧠 System Overview")
st.sidebar.write(
    """
    This project simulates an intelligent product search and ranking system.

    Core layers:
    - Query understanding
    - Catalog taxonomy matching
    - Candidate retrieval
    - Personalized ranking
    - Explainable recommendations
    """
)

st.sidebar.markdown("---")
st.sidebar.write("Example queries:")
st.sidebar.code("premium sports shoes under 6000")
st.sidebar.code("cheap tshirts under 1000")
st.sidebar.code("premium lipstick under 3000")
st.sidebar.code("budget watches under 2000")

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("🛍️ Personalized Product Search & Ranking System")
st.write(
    "Search products using natural language and get ranked recommendations with simple explanations."
)

# --------------------------------------------------
# MODE SELECTION
# --------------------------------------------------
mode = st.radio(
    "Choose Mode",
    ["Search-Based", "User-Based"],
    horizontal=True
)

top_k = st.slider("Number of Recommendations", 3, 20, 10)

# ==================================================
# SEARCH-BASED MODE
# ==================================================
if mode == "Search-Based":

    st.subheader("🔎 Intelligent Product Search")

    query = st.text_input(
        "Enter your search query",
        placeholder="e.g. premium sports shoes under 6000 for running"
    )

    use_llm = st.checkbox(
        "Use LLM Parser",
        value=False,
        help="Keep unchecked unless OpenAI billing/API access is active."
    )

    if st.button("Search Products"):

        if query.strip() == "":
            st.warning("Please enter a query.")
            st.stop()

        result = intelligent_search(
            product_df=products_df,
            query=query,
            top_k=top_k,
            use_llm=use_llm
        )

        parsed_query = result["parsed_query"]
        metadata = result["metadata"]
        recs = result["recommendations"]

        # --------------------------
        # PARSED QUERY
        # --------------------------
        st.subheader("🧠 Query Understanding")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Category", parsed_query.get("category") or "N/A")
        col2.metric("Subcategory", parsed_query.get("sub_category") or "N/A")
        col3.metric("Persona", parsed_query.get("persona_type") or "N/A")
        col4.metric("Max Price", parsed_query.get("max_price") or "N/A")

        with st.expander("View full parsed query"):
            st.json(parsed_query)

        # --------------------------
        # RETRIEVAL METADATA
        # --------------------------
        st.subheader("📊 Retrieval Summary")

        m1, m2, m3 = st.columns(3)

        m1.metric("Candidate Count", metadata.get("candidate_count", 0))
        m2.metric(
            "Relaxation Multiplier",
            round(metadata.get("relaxation_multiplier", 1.0), 2)
        )

        relaxed_price = metadata.get("relaxed_max_price")
        m3.metric(
            "Relaxed Max Price",
            int(relaxed_price) if relaxed_price is not None else "N/A"
        )

        st.caption(
            f"Budget Weight: {metadata.get('budget_weight')} | "
            f"Quality Weight: {metadata.get('quality_weight')} | "
            f"Use Case: {metadata.get('use_case')}"
        )

        # --------------------------
        # RECOMMENDATIONS
        # --------------------------
        st.subheader("🏆 Recommended Products")

        if recs.empty:
            st.warning("No products found.")
        else:
            display_cols = [
                "product_id",
                "brand",
                "category",
                "sub_category",
                "price",
                "rating",
                "review_count",
                "final_score",
                "recommendation_reason"
            ]

            available_cols = [col for col in display_cols if col in recs.columns]
            st.dataframe(recs[available_cols])

            with st.expander("View technical ranking signals"):
                technical_cols = [
                    "product_id",
                    "price_score",
                    "trusted_rating_score",
                    "purchase_score",
                    "use_case_match_score",
                    "final_score"
                ]

                available_tech_cols = [col for col in technical_cols if col in recs.columns]
                st.dataframe(recs[available_tech_cols])

        if len(recs) < top_k:
            st.info(
                f"Only {len(recs)} products matched your filters, so showing fewer than requested."
            )

# ==================================================
# USER-BASED MODE
# ==================================================
else:

    st.subheader("👤 User-Based Recommendation")

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

        # --------------------------
        # USER SUMMARY
        # --------------------------
        st.subheader("📊 User Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Persona", summary["persona_type"])
        col2.metric("Budget", summary["avg_budget"])
        col3.metric("Total Recommendations", summary["total_recommendations"])

        col4, col5, col6 = st.columns(3)

        col4.metric("Avg Recommended Price", round(summary["avg_recommended_price"], 2))
        col5.metric("Avg Intrinsic Quality", round(summary["avg_intrinsic_quality"], 3))
        col6.metric(
            "Missing Ratings",
            f"{summary['missing_rating_count']} / {summary['total_recommendations']}"
        )

        # --------------------------
        # RECOMMENDATIONS
        # --------------------------
        st.subheader("🏆 Recommended Products")

        if recs.empty:
            st.warning("No products found.")
        else:
            display_cols = [
                "product_id",
                "brand",
                "category",
                "sub_category",
                "price",
                "rating",
                "review_count",
                "final_score",
                "recommendation_reason"
            ]

            available_cols = [col for col in display_cols if col in recs.columns]
            st.dataframe(recs[available_cols])

            with st.expander("View technical ranking signals"):
                technical_cols = [
                    "product_id",
                    "price_score",
                    "trusted_rating_score",
                    "purchase_score",
                    "final_score"
                ]

                available_tech_cols = [col for col in technical_cols if col in recs.columns]
                st.dataframe(recs[available_tech_cols])