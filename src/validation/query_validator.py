VALID_CATEGORY_SUBCATEGORY_MAP = {
    "Clothing": ["Tshirts", "Shirts", "Jeans", "Kurtis", "Dresses"],
    "Footwear": ["Sneakers", "Sandals", "Boots", "Flats", "Sports Shoes"],
    "Accessories": ["Bags", "Belts", "Caps", "Watches"],
    "Cosmetics": ["Lipstick", "Foundation", "Moisturizer", "Sunscreen"],
}  # dictionary of allowed values 

VALID_PERSONAS = {"Budget", "Balanced", "Quality"}
VALID_USE_CASES = {"Sports", "Daily Use", "Fashion"}


def validate_parsed_query(parsed_query: dict) -> dict:
    cleaned = {}

    # category
    category = parsed_query.get("category") # get category from LLM output
    cleaned["category"] = category if category in VALID_CATEGORY_SUBCATEGORY_MAP else None # If catgroy is valid and exists in the allowed category list, then keep it. Otherwise set it to None.

    # sub_category
    sub_category = parsed_query.get("sub_category") # get subcategory from LLM output
    if cleaned["category"] and sub_category in VALID_CATEGORY_SUBCATEGORY_MAP[cleaned["category"]]: # If category is valid and subcategory is valid for that category, then keep it. Otherwise set it to None.
        cleaned["sub_category"] = sub_category
    else:
        cleaned["sub_category"] = None

    # max_price
    max_price = parsed_query.get("max_price")
    if isinstance(max_price, (int, float)) and max_price > 0: # if max price is positive and greater than 0
        cleaned["max_price"] = int(max_price)
    else:
        cleaned["max_price"] = None

    # persona / persona_type
    persona = parsed_query.get("persona") or parsed_query.get("persona_type") # valid personas are Budgte , Quality and Balanced. check if the LLm output persona is valid
    cleaned["persona_type"] = persona if persona in VALID_PERSONAS else "Budget"

    # weights
    budget_weight = parsed_query.get("budget_weight")
    quality_weight = parsed_query.get("quality_weight")

    # If weights are not valid numbers, set default weights. If they are valid, normalize them so that they sum to 1. 
    if not isinstance(budget_weight, (int, float)) or not isinstance(quality_weight, (int, float)):
        budget_weight = 0.6
        quality_weight = 0.4
    else:
        budget_weight = max(0, min(1, budget_weight))
        quality_weight = max(0, min(1, quality_weight))

        total = budget_weight + quality_weight
        if total == 0:
            budget_weight = 0.6
            quality_weight = 0.4
        else:
            budget_weight = budget_weight / total
            quality_weight = quality_weight / total

    cleaned["budget_weight"] = budget_weight
    cleaned["quality_weight"] = quality_weight

    # use_case validation - only allow known values like sports,daily use and fashion. If the use case is not valid, set it to None.
    use_case = parsed_query.get("use_case")
    cleaned["use_case"] = use_case if use_case in VALID_USE_CASES else None

    return cleaned