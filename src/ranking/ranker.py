import numpy as np
from sklearn.preprocessing import minmax_scale
from src.config.parameters import PERSONA_PARAMS


def ranking(product_df,user):
    df=product_df.copy()
    budget=user.avg_budget
    persona=user.persona_type

    if persona=='Budget':
       params=PERSONA_PARAMS['Budget']

    elif persona=="Quality":
        params=PERSONA_PARAMS['Quality']
    else:
        raise ValueError(f"Unknown persona type: {persona}")

    df['error']=(df['price']-budget)/budget # error is deviation from user's budget. negative error means under budget, positive error means over budget

    df['price_score']=np.where(
        df['error']<=0,
            np.exp(-np.abs(df['error'])/params['b_low']),
            np.exp(-np.abs(df['error'])/params['b_high'])
    )
    
    df['rating_score']=(df['rating']-1)/4 # Rating is between 1 and 5, we want to give higher score to higher rating,
    # so we subtract 1
    df['purchase_log']=np.log1p(df['num_purchases']) # using lop1p instead of log to handle zero purchases and 
    #also to reduce the impact of outliers in num_purchases. This way, the difference between 0 and 1 purchase is more significant than the 
    # difference between 1000 and 1001 purchases, which makes sense in our context.
    df['purchase_score']=minmax_scale(df['purchase_log']) # we use minmax scaling to convert purchase score to
    #range [0,1] so that it is comparable to rating score which is also in range [0,1]
    
    # define k, where k is the minimum number of review_count after which a user can start trusting the rating
    k=20

    # calculte confidence 
    df['confidence_score']=df['review_count']/(df['review_count']+k) 
    # this will give us a confidence score between 0 and 1, where 0 means no confidence (0 reviews) and 1 means
    #  full confidence (infinite reviews). This way, products with few reviews will have a lower confidence score,
    #  which will reduce the impact of their rating on the final score. 

    # calculate trusted rating score by multiplying rating score with confidence
    df['trusted_rating_score']=df['rating_score']*df['confidence_score']

    # purchases should only be rewarded when rating is good. We are doing this so that the ranking should not blindly assume
    # a product with good purchases as a good quality product ... and later purchase_score should not dominate the final score when rating is bad
    # So we will multiply purchase_score with trusted_rating_score to get a more balanced score. 
    # df['validated_purchase_score']=df['purchase_score']*df['trusted_rating_score']
    # But this rule killed products with mediocre purchases,Products with good rating but medium purchases are 
    # getting unfairly penalized because purchase_score is being multiplied with trusted_rating_score, which 
    # reduces their contribution too much. This makes the ranking overly strict and biases it toward rating, 
    # causing even good products to drop
    df['trusted_adjusted_purchase_score']=df['purchase_score']*0.5 + 0.5*df['trusted_rating_score'] # creates a gate between 0.5 and 1
    # if trusted_rating_score = 0 → purchase keeps 50%
    #if trusted_rating_score = 1 → purchase keeps 100%
    #if trusted_rating_score = 0.6 → purchase keeps 80%
    #So now the system says:
    #"I will reduce popularity a bit if trust is weak, but I will not destroy it."
    
    # calculate final score as a product of price_score,purchase_score and trusted_rating score if rating exists
    # else final score is just a product of price_score and purchase_score
    df['final_score']=np.where(
        df['rating'].isna(),
        df['price_score']*df['purchase_score'],
        (params['w1'] * df['trusted_rating_score'] + params['w2'] * df['trusted_adjusted_purchase_score'])*df['price_score']
    )
    return df.sort_values(by='final_score', ascending=False)




