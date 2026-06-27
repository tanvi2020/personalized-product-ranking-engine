from src.parser.hybrid_parser import hybrid_parse_query
from src.recommendation.recommender import recommend_from_query
from src.parser.catalog_query_matcher import apply_catalog_matching

def intelligent_search(product_df, query: str, top_k: int = 10, use_llm: bool = True):
    """
    End-to-end natural language search.

    User query
    -> hybrid parser
    -> validated structured query
    -> candidate retrieval
    -> ranking
    -> top recommendations
    """

    parsed_query = hybrid_parse_query(query, use_llm=use_llm)
    parsed_query = apply_catalog_matching(query, parsed_query)
    
    result = recommend_from_query(
        product_df=product_df,
        category=parsed_query["category"],
        sub_category=parsed_query["sub_category"],
        max_price=parsed_query["max_price"],
        persona_type=parsed_query["persona_type"],
        use_case=parsed_query["use_case"],
        budget_weight=parsed_query["budget_weight"],
        quality_weight=parsed_query["quality_weight"],
        top_k=top_k
    )
    return {
        "parsed_query": parsed_query,
        "metadata": result["metadata"],
        "retrieved_candidates": result["retrieved_candidates"],
        "recommendations": result["recommendations"]
    }