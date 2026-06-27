import re


CATALOG_MATCHING_RULES = {
    "Footwear": {
        "Sports Shoes": ["sports shoes", "running shoes", "gym shoes", "training shoes", "track shoes", "gym shooes"],
        "Sneakers": ["sneakers", "sneaker", "snkers", "kicks", "trainers"],
        "Sandals": ["sandals", "sandls"],
        "Boots": ["boots"],
        "Heels": ["heels"],
        "Flats": ["flats"],
    },

    "Clothing": {
        "Tshirts": ["tshirt", "tshirts", "t-shirt", "t-shirts", "thsirts", "tshirtts"],
        "Shirts": ["shirt", "shirts", "formal shirts", "formals"],
        "Jeans": ["jeans", "denim", "denims", "denm"],
        "Hoodies": ["hoodie", "hoodies"],
        "Trousers": ["trouser", "trousers"],
        "Jackets": ["jacket", "jackets"],
        "Dresses": ["dress", "dresses"],
        "Kurtis": ["kurti", "kurtis"],
    },

    "Accessories": {
        "Bags": ["bag", "bags", "handbag", "handbags", "travel bags"],
        "Belts": ["belt", "belts"],
        "Caps": ["cap", "caps"],
        "Watches": ["watch", "watches"],
        "Sunglasses": ["sunglasses", "shades"],
    },

    "Cosmetics": {
        "Lipstick": ["lipstick", "lipsticks", "lipstik", "lip color"],
        "Foundation": ["foundation"],
        "Moisturizer": ["moisturizer", "moisturiser", "skin cream", "face lotion"],
        "Sunscreens": ["sunscreen", "sunscreens", "sun screen"],
        "Perfumes": ["perfume", "perfumes", "perfumee"],
        "Eye Makeup": ["eye makeup", "eye products"],
        "Skincare": ["skincare", "skin care"],
    }
}


def keyword_matches_query(keyword: str, query: str) -> bool:
    """
    Match full words / full phrases only.
    Avoids bad substring matches.
    Example:
    'tee' should not match inside some random word.
    """
    keyword = keyword.lower().strip()
    query = query.lower().strip()

    pattern = r"\b" + re.escape(keyword) + r"\b"

    return re.search(pattern, query) is not None


def apply_catalog_matching(query: str, parsed_query: dict) -> dict:
    query_lower = query.lower()
    cleaned = parsed_query.copy()

    matched_category = None
    matched_subcategory = None

    for category, subcategory_rules in CATALOG_MATCHING_RULES.items():
        for subcategory, keywords in subcategory_rules.items():
            for keyword in keywords:
                if keyword_matches_query(keyword, query_lower):
                    matched_category = category
                    matched_subcategory = subcategory
                    break

            if matched_subcategory is not None:
                break

        if matched_subcategory is not None:
            break

    cleaned["category"] = matched_category or cleaned.get("category") # First try to infer from actual query words. If matcher finds nothing, then keep parser output.
    cleaned["sub_category"] = matched_subcategory or cleaned.get("sub_category")

    return cleaned