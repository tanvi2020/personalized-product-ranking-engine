import json

try:
    from openai import OpenAI
    from dotenv import load_dotenv
except ImportError:
    OpenAI = None

    def load_dotenv():
        pass


load_dotenv()


QUERY_PARSE_SCHEMA = {
    "name": "product_query_parse",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "category": {
                "type": ["string", "null"],
                "enum": ["Clothing", "Footwear", "Accessories", "Cosmetics", None],
            },
            "sub_category": {
                "type": ["string", "null"],
                "enum": [
                    "Tshirts", "Shirts", "Jeans", "Kurtis", "Dresses",
                    "Sneakers", "Sandals", "Boots", "Flats", "Sports Shoes",
                    "Bags", "Belts", "Caps", "Watches",
                    "Lipstick", "Foundation", "Moisturizer", "Sunscreen",
                    None,
                ],
            },
            "max_price": {"type": ["integer", "null"]},
            "persona": {
                "type": "string",
                "enum": ["Budget", "Balanced", "Quality"],
            },
            "use_case": {
                "type": ["string", "null"],
                "enum": ["Sports", "Daily Use", "Fashion", None],
            },
            "budget_weight": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
            },
            "quality_weight": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
            },
        },
        "required": [
            "category",
            "sub_category",
            "max_price",
            "persona",
            "use_case",
            "budget_weight",
            "quality_weight",
        ],
    },
    "strict": True,
}


def parse_query_with_llm(query: str, model: str = "gpt-4.1-mini") -> dict:
    """
    Convert a product search query into structured fields using an LLM.

    The OpenAI client is created inside this function, not at import time.
    This prevents CI from failing when LLM parsing is disabled.
    """

    if OpenAI is None:
        raise ImportError("OpenAI package is not installed.")

    client = OpenAI()

    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": """
You are a query parser for a product search and ranking system.

Extract only structured intent.

Rules:
- category must be one of: Clothing, Footwear, Accessories, Cosmetics, or null.
- sub_category must match the user's intent if clear, else null.
- max_price should be extracted from phrases like under 3000, below 5000, within 2000.
- persona:
  - Budget = cheap, affordable, budget, low price
  - Quality = best, premium, durable, top quality
  - Balanced = both cheap and best/quality are mentioned
- budget_weight and quality_weight must sum close to 1.
- use_case can be Sports, Daily Use, Fashion, or null.
- Do not invent fields.
""",
            },
            {
                "role": "user",
                "content": query,
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": QUERY_PARSE_SCHEMA["name"],
                "schema": QUERY_PARSE_SCHEMA["schema"],
                "strict": True,
            }
        },
    )

    return json.loads(response.output_text)