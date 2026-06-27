PERSONA_PARAMS= {
    'Budget':{
        'b_low':0.72,# Anchors to calculate b_low -->score -50% → 0.5 (soft decay until 50% below budget)
        'b_high':0.217,# Anchors to calculate b_high ---> score +50% → 0.1 (aggresive decay after 50% above budget)
        'w1':0.6,
        'w2':0.4
    },
    'Quality':{
        'b_low':0.546, # Anchors to calculate b_high ---> score(−50%) = 0.4 (They distrust too-cheap items slightly more than Budget users)
        'b_high':0.415,# Anchors to calculate b_low --> score(+50%) = 0.3 (they tolerate overspend more than Budget users)
        'w1':0.7,
        'w2':0.3
    }
}
USE_CASE_SUBCATEGORY_MAP = {
    "Sports": {
        "Footwear": ["Sneakers", "Sports Shoes"],
        "Clothing": ["Tshirts"],
        "Accessories": ["Caps", "Watches"]
    },
    "Fashion": {
        "Footwear": ["Flats", "Boots", "Sandals"],
        "Clothing": ["Dresses", "Kurtis", "Shirts"],
        "Accessories": ["Bags", "Belts", "Watches"],
        "Cosmetics": ["Lipstick", "Foundation"]
    },
    "Daily Use": {
        "Footwear": ["Sneakers", "Flats", "Sandals"],
        "Clothing": ["Tshirts", "Jeans", "Shirts", "Kurtis"],
        "Accessories": ["Bags", "Watches"],
        "Cosmetics": ["Moisturizer", "Sunscreen"]
    }
}