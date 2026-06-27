from src.agent.query_parser import parse_query
from src.parser.llm_parser import parse_query_with_llm
from src.validation.query_validator import validate_parsed_query
from src.parser.catalog_query_matcher import apply_catalog_matching

def hybrid_parse_query(query: str, use_llm: bool = True) -> dict:
    """
    LLM first.
    If LLM fails, fallback to rule-based parser.
    Always validate final output.
    """

    if use_llm:
        try:
            raw_parsed = parse_query_with_llm(query)
            print("Used LLM parser")
        except Exception as e:
            print("LLM parser failed. Falling back to rule-based parser.")
            print("Error:", e)
            raw_parsed = parse_query(query)
    else:
        raw_parsed = parse_query(query)
        print("Used rule-based parser")

    cleaned_query = validate_parsed_query(raw_parsed)
    cleaned_query = apply_catalog_matching(query, cleaned_query)

    return cleaned_query