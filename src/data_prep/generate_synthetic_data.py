import numpy as np
import pandas as pd
import random


# --------------------------
# RANDOM SEED
# --------------------------
random.seed(42)
np.random.seed(42)


# --------------------------
# CONFIG
# --------------------------
brands = ["Nike", "Puma", "Adidas", "Libas", "Levis", "H&M", "Zara", "MAC", "Maybelline", "SwissBeauty"]

category_weights = {
    "Clothing": 0.35,
    "Footwear": 0.30,
    "Cosmetics": 0.20,
    "Accessories": 0.15
}

brand_category_weights = {
    "Clothing": {
        "Nike": 0.12, "Puma": 0.10, "Adidas": 0.12,
        "Libas": 0.18, "Levis": 0.18, "H&M": 0.15, "Zara": 0.15
    },
    "Footwear": {
        "Nike": 0.28, "Puma": 0.22, "Adidas": 0.28,
        "H&M": 0.10, "Zara": 0.12
    },
    "Accessories": {
        "Nike": 0.15, "Puma": 0.12, "Adidas": 0.12,
        "H&M": 0.20, "Zara": 0.25, "Levis": 0.16
    },
    "Cosmetics": {
        "MAC": 0.35, "Maybelline": 0.35, "SwissBeauty": 0.30
    }
}

sub_category_weights = {
    "Clothing": {
        "Tshirts": 0.24,
        "Shirts": 0.22,
        "Jeans": 0.20,
        "Kurtis": 0.18,
        "Dresses": 0.16
    },
    "Footwear": {
        "Sneakers": 0.25,
        "Sports Shoes": 0.30,
        "Sandals": 0.20,
        "Flats": 0.15,
        "Boots": 0.10
    },
    "Accessories": {
        "Bags": 0.32,
        "Watches": 0.28,
        "Caps": 0.22,
        "Belts": 0.18
    },
    "Cosmetics": {
        "Lipstick": 0.28,
        "Foundation": 0.24,
        "Moisturizer": 0.26,
        "Sunscreen": 0.22
    }
}

category_size_map = {
    "Clothing": ["S", "M", "L", "XL", "XXL"],
    "Footwear": ["UK4", "UK6", "UK8", "UK10", "UK12"],
    "Accessories": ["Small", "Medium", "Large"],
    "Cosmetics": ["Small", "Medium", "Large"],
}

colors = ["Red", "Blue", "Green", "Yellow", "Pink", "Purple", "Black", "White", "Brown"]

price_bucket_weights = {
    "price_low": 0.40,
    "price_mid": 0.45,
    "price_high": 0.15
}

price_ranges = {
    "Clothing": {
        "price_low": (200, 800),
        "price_mid": (800, 2500),
        "price_high": (2500, 8000)
    },
    "Footwear": {
        "price_low": (500, 1500),
        "price_mid": (1500, 5000),
        "price_high": (5000, 15000)
    },
    "Accessories": {
        "price_low": (150, 700),
        "price_mid": (700, 3000),
        "price_high": (3000, 12000)
    },
    "Cosmetics": {
        "price_low": (100, 500),
        "price_mid": (500, 2000),
        "price_high": (2000, 7000)
    }
}

brand_price_multiplier = {
    "Nike": 1.20,
    "Adidas": 1.20,
    "Puma": 1.10,
    "Zara": 1.15,
    "Levis": 1.10,
    "H&M": 0.95,
    "Libas": 0.90,
    "MAC": 1.25,
    "Maybelline": 0.85,
    "SwissBeauty": 0.75
}


# --------------------------
# HELPERS
# --------------------------
def weighted_choice(weight_dict):
    items = list(weight_dict.keys())
    weights = list(weight_dict.values())
    return random.choices(items, weights=weights, k=1)[0]


def generate_realistic_price(category, price_bucket, brand):
    low, high = price_ranges[category][price_bucket]

    # Triangular distribution creates more prices near the middle,
    # unlike randint which spreads everything equally.
    mode = (low + high) / 2
    price = random.triangular(low, high, mode)

    price *= brand_price_multiplier.get(brand, 1.0)

    price = int(round(price / 10) * 10)
    price = max(low, min(price, high))

    return price


def generate_quality(price_bucket):
    if price_bucket == "price_low":
        quality = np.random.beta(2, 4)
    elif price_bucket == "price_mid":
        quality = np.random.beta(3, 3)
    else:
        quality = np.random.beta(5, 2)

    return float(np.clip(quality, 0, 1))


# --------------------------
# PRODUCT GENERATION
# --------------------------
def generate_products(n=5000):
    products = []

    for product_id in range(1, n + 1):
        products.append(generate_single_product(product_id))

    return pd.DataFrame(products)


def generate_single_product(product_id):
    # 1. Category, brand, subcategory
    category = weighted_choice(category_weights)
    brand = weighted_choice(brand_category_weights[category])
    sub_category = weighted_choice(sub_category_weights[category])

    # 2. Price bucket + realistic price
    price_bucket = weighted_choice(price_bucket_weights)
    price = generate_realistic_price(category, price_bucket, brand)

    # 3. Hidden quality
    intrinsic_quality = generate_quality(price_bucket)

    # 4. Brand strength
    brand_strength = random.uniform(0, 1)

    # 5. Product age
    product_age = random.uniform(1, 365)

    # 6. Demand / exposure
    demand_type = np.random.choice(
        ["low", "medium", "high"],
        p=[0.30, 0.50, 0.20]
    )

    if demand_type == "low":
        exposure = np.random.uniform(0.02, 0.25)
    elif demand_type == "medium":
        exposure = np.random.uniform(0.65, 1.20)
    else:
        exposure = np.random.uniform(1.25, 1.90)

    # 7. Purchases
    quality_component = intrinsic_quality * 2000
    brand_component = brand_strength * 1500
    age_component = (product_age / 365) * 1500

    base_purchase_signal = quality_component + brand_component + age_component
    noise = np.random.randint(-300, 301)

    final_purchase_signal = base_purchase_signal * exposure + noise
    num_purchases = int(max(0, min(5000, final_purchase_signal)))

    # 8. Reviews
    review_rate = np.random.uniform(0.01, 0.03)
    review_noise = np.random.uniform(-5, 6)

    review_count = int(num_purchases * review_rate + review_noise)
    review_count = max(0, review_count)

    # 9. Rating
    rating = np.nan
    threshold = 5

    if review_count >= threshold:
        base_rating = 1 + 4 * intrinsic_quality
        rating_noise_scale = 0.2 / np.sqrt(review_count)
        rating_noise = np.random.uniform(-rating_noise_scale, rating_noise_scale)

        rating = base_rating + rating_noise
        rating = float(np.clip(rating, 1, 5))

    # 10. Other attributes
    color = random.choice(colors)
    size = random.choice(category_size_map[category])
    delivery_days = random.randint(1, 7)

    return {
        "product_id": product_id,
        "brand": brand,
        "category": category,
        "sub_category": sub_category,
        "price_bucket": price_bucket,
        "price": price,
        "intrinsic_quality": intrinsic_quality,
        "brand_strength": brand_strength,
        "review_count": review_count,
        "rating": rating,
        "num_purchases": num_purchases,
        "color": color,
        "size": size,
        "delivery_days": delivery_days,
    }


# --------------------------
# USER GENERATION
# --------------------------
def generate_users(n=500):
    users = []

    for user_id in range(1, n + 1):
        persona_type = random.choices(
            ["Budget", "Quality"],
            weights=[0.55, 0.45],
            k=1
        )[0]

        if persona_type == "Budget":
            avg_budget = random.randint(500, 4000)
        else:
            avg_budget = random.randint(4000, 15000)

        users.append({
            "user_id": user_id,
            "persona_type": persona_type,
            "avg_budget": avg_budget,
        })

    return pd.DataFrame(users)


# --------------------------
# MAIN
# --------------------------
if __name__ == "__main__":
    products_df = generate_products(5000)
    users_df = generate_users(500)

    products_df.to_csv("data/raw/products.csv", index=False)
    users_df.to_csv("data/raw/users.csv", index=False)

    print("Product csv saved successfully")
    print("Users csv saved successfully")

    print("\nProduct count:", len(products_df))
    print("User count:", len(users_df))

    print("\nCategory distribution:")
    print(products_df["category"].value_counts(normalize=True).round(3))

    print("\nSub-category distribution:")
    print(products_df["sub_category"].value_counts())

    print("\nQuality by price bucket:")
    print(products_df.groupby("price_bucket")["intrinsic_quality"].mean())

    print("\nPrice by category:")
    print(products_df.groupby("category")["price"].describe())

    print("\nMissing rating percentage:")
    print(products_df["rating"].isna().mean() * 100)

    print("\nProduct sample:")
    print(products_df.head())