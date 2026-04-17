# import libraries
import numpy as np
import pandas as pd
import random

from src.ranking.ranker import ranking
# Helper functions to generate Numerical and Categorical variables
# Function to generate Products

brands=['Nike','Puma','Adidas','Libas','Levis','H&M','Zara','MAC','Maybelline','SwissBeauty']
categories=['Clothing','Footwear','Accessories','Cosmetics']
brand_category_map={
    "Nike": ["Clothing", "Footwear", "Accessories"],
    "Puma": ["Clothing", "Footwear", "Accessories"],
    "Adidas": ["Clothing", "Footwear", "Accessories"],
    "Libas": ["Clothing"],
    "Levis": ["Clothing"],
    "H&M": ["Clothing", "Footwear", "Accessories"],
    "Zara": ["Clothing", "Footwear", "Accessories"],
    "MAC": ["Cosmetics"],
    "Maybelline": ["Cosmetics"],
    "SwissBeauty": ["Cosmetics"]
}
sub_category_map={
    "Clothing": ["Tshirts", "Shirts", "Jeans", "Kurtis", "Dresses"],
    "Footwear": ["Sneakers", "Sandals", "Boots", "Flats", "Sports Shoes"],
    "Accessories": ["Bags", "Belts", "Caps", "Watches"],
    "Cosmetics": ["Lipstick", "Foundation", "Moisturizer", "Sunscreen"]
    }  
ratings=[1,2,3,4,5]
rating_prob=[0.05,0.10,0.25,0.35,0.25]
colors=['Red','Blue','Green','Yellow','Pink','Purple']
sizes=['S','M','L','XL','XXL','UK4','UK6','UK8','UK10','UK12','Small','Medium','Large']

category_size_map={'Clothing':['S','M','L','XL','XXL'],
                   'Footwear':['UK4','UK6','UK8','UK10','UK12'],
                   'Accessories':['Small','Medium','Large'],
                   'Cosmetics':['Small','Medium','Large']}

delivery_days_range=(1,7)
price_low=(100,800)
price_mid=(800,3000)
price_high=(3000,15000)

def generate_products(n=500):
    products=[] # Create an empty list called products
    for i in range(1,n+1):
        prod_list=generate_single_product(i) # For each productid i call generate_single_product function
        products.append(prod_list) # store the output in the products list
    df=pd.DataFrame(products) # convert the list to a dataframe
    return df # return 
    
# Function to generate Users
# Main block to Run everything and save CSV

def generate_single_product(product_id):
    intrinsic_quality=random.uniform(0,1) # this hidden feature influences rating. It is not directly observable but it affects the rating given by users. We can use this to create a more realistic relationship between product features and ratings.
    brand_strength=random.uniform(0,1) # Why 0–1 instead of 1–10? Because normalized hidden variables are much easier to combine later. Almost every ML system internally operates on scaled signals.
    product_age=random.uniform(1,365)# in days
    # intrinsic quality, brand strength and product_age influence pruchases .

    quality_component=intrinsic_quality * 2000
    brand_component=brand_strength * 1500
    age_component=(product_age/365) * 1500

    noise=np.random.randint(-300,301)# to make the data more realistic,add uncertainity to the data 

    base_purchase_signal=(quality_component + brand_component + age_component)  
    # define types of demands and their probabilities
    demands=['low','medium','high']
    probabilities=[0.3,0.5,0.2] # 20% low demand, 60% medium demand, 20% high demand
    demand_type=np.random.choice(demands,p=probabilities)
    if demand_type=='low':
        exposure=np.random.uniform(0.001,0.002) # Exposure is a multiplicative feature we add. Exposure tells how many people have seen the product, we can use this to create realistic product pattern ranges like low esposure products, medium exposure and high/ viral products. 
    elif demand_type=='medium':
        exposure=np.random.uniform(0.8,1.2)
    else: # if demand_type=='high'
        exposure=np.random.uniform(1.3,1.8)
    
    final_purchase_signal=base_purchase_signal * exposure + noise  
    num_purchases=int(max(0,min(5000,final_purchase_signal)))# max will ensure that we dont have negative purchases and is purchase is >5000 it returns 5000. 
    brand=random.choice(brands)
    category=random.choice(brand_category_map[brand])
    review_noise=np.random.uniform(-5,6) # to add some randomness to review count . review count will be like 10, 20, 50 .. so noise should be very small like +-5.   
    review_rate=np.random.uniform(0.01,0.03) # generate review rate between 1% to 3%  
    review_count = int(num_purchases * review_rate+ review_noise)
    review_count=max(0,review_count) # avoid negative invalid review counts

    rating=np.nan
    threshold=5 # we will only assign ratings to products which have atleast 5 reviews. This is because with very few reviews, the rating can be very unreliable and can be heavily influenced by outliers. By setting a threshold, we ensure that the ratings are based on a more substantial amount of feedback, making them more representative of the product's true quality and customer satisfaction.
    
    if review_count>=threshold:
        base_rating = 1 + 4 * intrinsic_quality # we add 1 so that rating always is in a scale of 1 to 5. Say if intrinsic_qualit=0, then adding +1 will make the rating as 1 not 0.
        rating_noise_scale= 0.2/np.sqrt(review_count)# find how much noise allowed using noise_scale. 0.2 is the maximum allowed change in the rating 
        rating_noise=np.random.uniform(-rating_noise_scale,+rating_noise_scale) # we want to add noise in both direction so we use uniform distribution between -noise_scale and +noise_scale. This way we can have some products with slightly higher ratings than their intrinsic quality and some with slightly lower ratings, which is more realistic.
        rating = base_rating + rating_noise
        rating=np.clip(rating,1,5) # Ensure that ratings are between 1 and 5. If rating is less than 1, it will be set to 1. If rating is greater than 5, it will be set to 5. This is important because ratings outside this range would not make sense in the context of a typical product review system.

    if category in sub_category_map:
        sub_category=random.choice(sub_category_map.get(category,['unknown']))

    price_bucket=random.choices(['price_low','price_mid','price_high'],weights=[0.5,0.4,0.1],k=1)[0]

    if price_bucket=='price_low':
        price=random.randint(price_low[0],price_low[1])
    elif price_bucket=='price_mid':
        price=random.randint(price_mid[0],price_mid[1])
    else: # if price_bucket=='price_high'
        price=random.randint(price_high[0],price_high[1])
    color=random.choice(colors)
    
    if category in category_size_map:
        size=random.choice(category_size_map[category])
    delivery_days=random.randint(delivery_days_range[0],delivery_days_range[1])

    return {
        'product_id': product_id,
        'brand': brand,
        'category': category,
        'sub_category': sub_category,
        'review_count': review_count,
        'intrinsic_quality': intrinsic_quality,
        'brand_strength': brand_strength,
        'rating': rating,
        'price': price,
        'num_purchases': num_purchases,
        'color': color,
        'size': size,
        'delivery_days': delivery_days
    }

def generate_users(n):
    users=[]
    for i in range(1,n+1):
        if i<=n//2:
            persona_type='Budget'
            avg_budget=random.randint(300,3000)
        else:
            persona_type='Quality'
            avg_budget=random.randint(3000,15000)

        users.append({'user_id':i,
                      'persona_type':persona_type,
                      'avg_budget':avg_budget
                      })
        
    user_df=pd.DataFrame(users)
    return user_df



if __name__=='__main__':  
    generate_products(500).to_csv('data/raw/products.csv',index=False) 
    print('Product csv saved succesfully')
    #print(generate_single_product(1))
    generate_users(100).to_csv('data/raw/users.csv',index=False)
    print('Users csv saved succesfully')

    users_df = pd.read_csv("data/raw/users.csv")
    products_df = pd.read_csv("data/raw/products.csv")

    print(users_df.head(10))
    user1 = users_df[users_df['persona_type']=='Budget'].iloc[0]  # first user
    print("User 1 details :")
    print(user1)
    Budget_ranked = ranking(products_df, user1)

    print(Budget_ranked[['product_id', 'price', 'rating', 'num_purchases', 'error',
                  'price_score', 'rating_score','confidence_score','trusted_rating_score', 'purchase_score', 'final_score']].head(10))

    user2=users_df[users_df['persona_type']=='Quality'].iloc[0]
    print('User 2 details:')
    print(user2)
    Quality_ranked=ranking(products_df,user2)
    print(Quality_ranked[['product_id', 'price', 'rating', 'num_purchases', 'error',
                  'price_score', 'rating_score','confidence_score','trusted_rating_score', 'purchase_score', 'final_score']].head(10))
    
   
    
   