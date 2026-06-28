# Intelligent Product Search & Ranking System

End-to-end product search and ranking system that converts natural language product queries into personalized recommendations.

The system combines rule-based query parsing, LLM-powered query understanding, taxonomy matching, candidate retrieval, dynamic ranking, evaluation pipelines, MLflow tracking, Docker containerization, and GitHub Actions CI.

---

## Overview

This project simulates a production-style e-commerce search and recommendation system.

A user can enter queries such as:

```text
best running shoes under 3000
cheap tshirts below 1000
premium lipstick
daily use bag under 2000
```

The system understands the query, retrieves relevant products, ranks them based on quality, budget fit, popularity, and user intent, and returns explainable recommendations.

---

## Why This Project

Product search is not only a ranking problem.

If query understanding fails, retrieval fails.
If retrieval fails, ranking has poor candidates.
If ranking overuses popularity, lower-quality products may appear at the top.

This project focuses on building and evaluating the full pipeline, not just training a model.

---

## System Architecture

```text
User Query
   ↓
Hybrid Query Parser
   ├── Rule-Based Parser
   └── LLM Parser
        ↓
   Fallback to Rule Parser if LLM fails
   ↓
Validation Layer
   ↓
Catalog / Taxonomy Matching
   ↓
Candidate Retrieval
   ↓
Dynamic Ranking Engine
   ↓
Recommendation Explanations
   ↓
Streamlit UI
```

---

## Key Features

* Natural language product search
* Rule-based query parser
* LLM-based query parser using OpenAI API
* Hybrid fallback parser
* Query validation layer
* Catalog taxonomy matching
* Candidate retrieval
* Persona-aware ranking
* Budget-aware ranking
* Quality-aware ranking
* Recommendation explanations
* Parser, retrieval, and ranking evaluation
* MLflow experiment tracking
* Dockerized Streamlit app
* GitHub Actions CI pipeline

---

## Dataset

A synthetic e-commerce dataset was generated with 5,000 products across:

* Clothing
* Footwear
* Accessories
* Cosmetics

Each product contains:

* Category
* Subcategory
* Brand
* Price
* Rating
* Review count
* Number of purchases
* Intrinsic quality
* Brand strength

User personas were also simulated:

* Budget
* Quality
* Balanced

---

## Query Understanding

The system extracts structured signals from user queries:

* Category
* Subcategory
* Maximum price
* Persona
* Use case
* Budget weight
* Quality weight

Example:

```text
Query:
best running shoes under 3000
```

Parsed output:

```python
{
    "category": "Footwear",
    "sub_category": "Sports Shoes",
    "max_price": 3000,
    "persona_type": "Quality",
    "budget_weight": 0.2,
    "quality_weight": 0.8,
    "use_case": "Sports"
}
```

---

## LLM Parser

The LLM parser improves query understanding for natural language queries.

The system uses a hybrid design:

```text
Try LLM Parser
   ↓
If successful → use LLM output
   ↓
If failed → fallback to rule-based parser
```

This makes the system more robust because the application can still work even if the LLM API fails.

---

## Parser Evaluation Results

The LLM parser was evaluated against the rule-based parser using the same evaluation dataset.

| Metric            | Rule-Based Parser | LLM Parser |
| ----------------- | ----------------: | ---------: |
| Category Score    |            94.68% |    100.00% |
| Subcategory Score |            79.26% |     85.64% |
| Persona Score     |            60.64% |     89.36% |
| Max Price Score   |           100.00% |    100.00% |
| Use Case Score    |            65.96% |     66.49% |
| Overall Average   |            80.11% |     88.30% |

The largest improvement came from persona detection, where the LLM handled intent words such as “best,” “premium,” “cheap,” and “affordable” better than rule-based logic.

---

## Retrieval Layer

The retrieval layer filters products using parsed query signals:

* Category
* Subcategory
* Price constraints
* Use case

A relaxation strategy is used to avoid overly strict filtering. For example, quality-focused searches may allow a slightly wider price range to avoid empty results.

---

## Ranking Layer

The ranking engine combines multiple signals:

* Budget fit
* Trusted rating score
* Review confidence
* Popularity
* Use-case match
* Persona weights

The ranking logic avoids relying only on popularity and gives stronger weight to trusted quality signals.

---

## Ranking Evaluation Results

| Metric                    | Value |
| ------------------------- | ----: |
| Average Candidate Quality | ~0.43 |
| Average Top-10 Quality    | ~0.69 |
| Quality Lift              | ~0.26 |
| Top-1 Intrinsic Quality   | ~0.78 |

The ranking engine improved average product quality by promoting stronger products from the retrieved candidate set.

---

## MLflow Tracking

MLflow is used to track:

* Parser experiments
* Retrieval experiments
* Ranking experiments
* Parameters
* Metrics
* Evaluation artifacts

This makes experiments reproducible and easier to compare.

---

## CI/CD

GitHub Actions is used as the CI pipeline.

On every push, the pipeline automatically:

```text
1. Checks out the repository
2. Sets up Python
3. Installs dependencies
4. Runs parser evaluation
5. Runs retrieval evaluation
6. Runs ranking evaluation
7. Builds the Docker image
```

This helps catch production issues before deployment.

During CI setup, the pipeline caught a real bug where the OpenAI client was initialized during import. The parser was refactored so the OpenAI client is created only when the LLM parser is actually used.

---

## Docker

The Streamlit app is containerized using Docker.

The project uses separate dependency files:

* `requirements.txt` for full project evaluation and MLflow tracking
* `requirements-app.txt` for the lightweight Streamlit Docker app

This keeps the application container smaller and avoids unnecessary runtime dependencies.

---

## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* OpenAI API
* MLflow
* Docker
* GitHub Actions
* Git

---

## Project Structure

```text
.
├── app.py
├── Dockerfile
├── requirements.txt
├── requirements-app.txt
├── data/
│   ├── raw/
│   └── evaluation/
├── mlflow_tracking/
├── src/
│   ├── data_prep/
│   ├── parser/
│   ├── validation/
│   ├── recommendation/
│   ├── ranking/
│   └── evaluation/
└── .github/
    └── workflows/
        └── ci.yml
```

---

## Key Learnings

The biggest learning from this project is that recommendation quality is a full-system problem.

A better ranking formula alone is not enough.

The system needs:

* Strong query understanding
* Reliable retrieval
* Robust ranking
* Layer-wise evaluation
* Experiment tracking
* CI checks
* Reproducible deployment setup

This project helped turn a recommendation notebook into a production-style ML system.

---

## Future Improvements

* Add semantic retrieval using vector embeddings
* Add learning-to-rank model
* Add online A/B testing simulation
* Add FastAPI serving layer
* Add monitoring for drift and degraded search quality
* Connect to a real product catalog or database

---

## Author

**Tanvi Ranganekar**
M.Sc. Data Science
