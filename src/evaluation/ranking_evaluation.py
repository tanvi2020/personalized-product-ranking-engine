# Are the top ranked product actually of good quality? Check for both - Quality and Budget user. 
# We can use the intrinsic quality as a proxy for the actual quality of the product.
# If the average intrinsic_quality of the top ranked products is higher than the overall average 
# intrinsic_quality, then the ranking is good. 

from src.data_prep.generate_synthetic_data import generate_products, generate_users
from src.ranking.ranker import ranking
import pandas as pd

if __name__ =="__main__":
    products_df=generate_products(500)
    users_df=generate_users(100)

    user1=users_df[users_df['persona_type']=='Budget'].iloc[0]
    user2=users_df[users_df['persona_type']=='Quality'].iloc[0]

    budget_user_ranking=ranking(products_df,user1)
    quality_user_ranking=ranking(products_df,user2)

    # Calculate average intrinsic quality for top 10 ranked products for both users
    avg_intrinsic_quality_budget = budget_user_ranking.head(10)['intrinsic_quality'].mean()
    avg_intrinsic_quality_quality = quality_user_ranking.head(10)['intrinsic_quality'].mean()
    # calculate overall average intrinsic quality for all products
    overall_avg_intrinsic_quality = products_df['intrinsic_quality'].mean()
    
    print(f"Average Intrinsic Quality of top 10 ranked products for Budget user: {avg_intrinsic_quality_budget}")

    print(f"Average Intrinsic Quality of top 10 ranked products for Quality user: {avg_intrinsic_quality_quality}")
    print(f"Overall Average Intrinsic Quality: {overall_avg_intrinsic_quality}")
    if avg_intrinsic_quality_budget > overall_avg_intrinsic_quality:
        print("The ranking for Budget user is good.")
    else:
        print("The ranking for Budget user is not good.")  

    if avg_intrinsic_quality_quality > overall_avg_intrinsic_quality:
        print("The ranking for Quality user is good.")
    else:
        print("The ranking for Quality user is not good.")    

    # observation : The ranking system is working well because the average intrinsic quality of the top 10 ranked
    # products is much higher than the overall dataset average for both Budget and Quality users. This shows that 
    # ranking function is successfully surfacing better products near the top instead of ranking products randomly.