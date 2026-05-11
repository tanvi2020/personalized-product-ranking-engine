def parse_query(query):
    """
    Convert user query into structured signals.
    """

    query = query.lower()

    category = None
    sub_category = None
    max_price = None
    persona = "Budget"  # default
    use_case= None
    budget_weight = 0.6
    quality_weight = 0.4


    # --------------------------
    # CATEGORY / SUBCATEGORY
    # --------------------------
    footwear_words = ["footwear", "shoes", "sneakers", "trainers", "kicks"]
    clothing_words = ["clothing", "clothes", "dress", "shirt", "jeans", "tshirt","kurtis"]
    accessory_words = ["accessories", "bags", "watches", "belts", "caps"]
    cosmetic_words = ["cosmetics", "makeup", "lipstick", "moisturizer"]

    # Specific first
    if any(word in query for word in footwear_words):
        category = "Footwear"
        if "sneakers" in query or "trainers" in query or "kicks" in query:
            sub_category = "Sneakers"

    elif any(word in query for word in cosmetic_words):
        category = "Cosmetics"
        sub_category = "Lipstick"

    elif any(word in query for word in cosmetic_words):
        category = "Cosmetics"
        sub_category = "Moisturizer"

    elif any(word in query for word in clothing_words):
        category = "Clothing"
        if "dress" in query:
            sub_category = "Dress"
        elif "shirt" in query:
            sub_category = "Shirt"
        elif "jeans" in query:
            sub_category = "Jeans"
        elif "tshirt" in query:
            sub_category = "T-Shirt"    
        elif "kurtis" in query:
            sub_category = "Kurti"
    elif any(word in query for word in accessory_words):
        category = "Accessories"
        if "bags" in query:
            sub_category = "Bags"
        elif "watches" in query:
            sub_category = "Watches"
        elif "belts" in query:
            sub_category = "Belts"
        elif "caps" in query:
            sub_category = "Caps"

    # --------------------------
    # PRICE
    # --------------------------
    import re # regular expression module

    price_match = re.search(r"\d+", query) # find the first number in the query, which we will treat as max price
    if price_match:
        max_price = int(price_match.group())

    # --------------------------
    # PERSONA (intent)
    # --------------------------
    quality_words = ["best","quality", "durable", "long-lasting", "premium","top"]
    budget_words = ["cheap", "affordable", "budget", "inexpensive"]

    quality_flag = any(word in query for word in quality_words)
    budget_flag = any(word in query for word in budget_words)


    if quality_flag and budget_flag:
        persona = "Balanced"
        budget_weight = 0.5
        quality_weight = 0.5
    elif quality_flag:
        persona = "Quality"
        budget_weight = 0.2
        quality_weight = 0.8
    elif budget_flag:
        persona = "Budget"
        budget_weight = 0.8
        quality_weight = 0.2
    else:
        persona = "Budget"
        budget_weight = 0.6
        quality_weight = 0.4


    # --------------------------
    # USE CASE 
    #---------------------------
    
    sports_words = ["sports", "running", "gym", "training", "athletic"]
    daily_words = ["daily", "everyday", "regular use"]
    fashion_words = ["party", "fashion", "stylish"]

    if any(word in query for word in sports_words):
        use_case = "Sports"
    elif any(word in query for word in daily_words):
        use_case = "Daily Use"
    elif any(word in query for word in fashion_words):
        use_case = "Fashion"


    return {
        "category": category,
        "sub_category": sub_category,
        "max_price": max_price,
        "persona": persona,
        "use_case": use_case,
        "budget_weight" : budget_weight,
        "quality_weight" : quality_weight
    }