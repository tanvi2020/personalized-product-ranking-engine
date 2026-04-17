# Personalized Product Ranking Engine with Synthetic Marketplace Simulation

## Overview

This project explores how real-world product ranking systems work by building a simplified version from scratch.

Instead of relying on existing datasets, I designed a synthetic e-commerce marketplace that tries to mimic real user behavior. The goal was not just to rank products, but to understand how different signals like popularity, ratings, and user preferences interact in a realistic system.

---

## Problem

In many beginner projects, datasets are either too clean or randomly generated, which leads to unrealistic model behavior.

While working on this project, I realized that:
- Too many products had ratings  
- Review counts were very similar  
- Low-quality products still looked competitive  
- Ratings and purchases were overly correlated  

This made the dataset unrealistic and reduced the effectiveness of any ranking logic built on top of it.

---

## Approach

### 1. Synthetic Data Generation

I built a custom data generation pipeline where each product is defined by hidden factors:

- intrinsic quality  
- brand strength  
- product age  

These factors are not directly visible but influence observable behavior.

A causal flow was implemented:
quality / brand / age → purchases → reviews → rating

This ensures that ratings are a result of user interactions, not randomly assigned values.

---

### 2. Improving Data Realism

EDA was used as a debugging tool to identify unrealistic patterns.

Key improvements included:

- Introducing demand segmentation (high / medium / low demand products)  
- Adding controlled randomness instead of pure noise  
- Adjusting rating visibility thresholds (to allow missing ratings)  
- Reducing strong correlation between rating and purchases  

These changes made the dataset more diverse and closer to real-world behavior.

---

### 3. Personalized Ranking

A ranking system was built using multiple signals:

- price  
- rating  
- popularity (purchases)  

Instead of a static score, ranking is personalized:

- Budget-focused users prioritize price  
- Quality-focused users prioritize rating  

This allows the same product set to be ranked differently depending on user preferences.

---

### 4. Evaluation

The system is evaluated by checking whether top-ranked products align with intrinsic product quality.

Work is ongoing to incorporate formal ranking metrics such as NDCG.

---

## Current Status

- Synthetic data generation pipeline: complete  
- Data realism improvements: ongoing  
- Personalized ranking logic: implemented  
- Evaluation metrics: in progress  
- Agent-based interface: planned  

---

## Project Structure
data/
raw/ # synthetic datasets

notebooks/
eda_validation.ipynb # data validation and realism checks

src/
config/
data_prep/
evaluation/
ranking/


---

## Key Learnings

- Data quality matters more than model complexity  
- Realistic data requires modeling user behavior, not just generating numbers  
- Strong correlations between features can mislead ranking systems  
- EDA is not just analysis—it is a debugging tool for data generation  

---

## Future Work

- Improve low-demand product representation  
- Implement NDCG-based evaluation  
- Add an agent layer for natural language queries  
- Build an end-to-end pipeline for easier execution  

---

## Tech Stack

Python, Pandas, NumPy, Scikit-learn