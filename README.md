# Personalized Product Search & Ranking System

## Overview

This project builds an end-to-end product search and ranking system that converts natural language queries into personalized product recommendations.

The system understands user intent, retrieves relevant products from a product catalog, ranks them using multiple relevance signals, and provides recommendation explanations to improve transparency and user trust.

A key focus of the project is not only building the search pipeline, but also measuring and improving it through dedicated evaluation frameworks for query understanding, retrieval quality, and ranking quality.

---

## Problem Statement

Traditional product search systems often rely on keyword matching, popularity, or simple filtering. As a result, users may receive recommendations that do not fully match their intent.

Examples:

* A user searching for "cheap sneakers under 3000" may receive expensive products with high ratings.
* A user searching for "premium running shoes" may receive budget products because they are popular.
* Different users may receive similar recommendations despite having different preferences.

The goal of this project is to improve recommendation relevance by combining query understanding, candidate retrieval, personalized ranking, and systematic evaluation.

---

## Project Highlights

* Built an end-to-end product search and ranking pipeline
* Developed query understanding and taxonomy matching layers
* Implemented candidate retrieval and personalized ranking
* Built parser, retrieval, and ranking evaluation frameworks
* Achieved Category Match Rate ≈ 0.93
* Achieved Quality Lift ≈ +0.26
* Improved average recommendation quality from 0.43 to 0.69
* Developed a Streamlit application with recommendation explanations

---

## System Architecture

```text
User Query
   ↓
Query Understanding
   ↓
Taxonomy Matching
   ↓
Candidate Retrieval
   ↓
Ranking Engine
   ↓
Recommendation Explanations
   ↓
Streamlit UI
```

### Evaluation Pipeline

```text
Evaluation Queries
   ↓
Parser Evaluation
   ↓
Retrieval Evaluation
   ↓
Ranking Evaluation
   ↓
Failure Analysis
   ↓
System Improvements
```

---

## Core Components

### Product Catalog

A synthetic e-commerce catalog was created containing product information such as:

* Category
* Subcategory
* Price
* Rating
* Review Count
* Number of Purchases
* Intrinsic Quality (hidden evaluation signal)

The catalog serves as the foundation for retrieval and ranking.

### Query Understanding

Natural language queries are converted into structured signals including:

* Category
* Subcategory
* Persona
* Budget Constraints
* Use Case

These signals guide downstream retrieval and ranking.

### Taxonomy Matching

Users often use different vocabulary than the catalog.

Examples:

```text
Sneakers → Sports Shoes
Kicks → Sports Shoes
Trainers → Sports Shoes
```

Taxonomy matching helps bridge the gap between user language and catalog labels.

### Candidate Retrieval

The retrieval layer selects a relevant candidate set from the catalog using structured query signals.

The goal of retrieval is to reduce the search space before ranking.

### Ranking Engine

The ranking layer orders retrieved products based on relevance.

Ranking combines signals such as:

* Budget Fit
* Product Quality
* Rating Confidence
* Popularity
* User Intent

The objective is to place the most relevant products at the top of the recommendation list.

### Recommendation Explanations

The system generates simple explanations describing why products were recommended.

This improves transparency, interpretability, and user trust.

---

## Evaluation Framework

Instead of evaluating only final recommendations, separate evaluation frameworks were developed for each major stage of the pipeline.

### Parser Evaluation

Measures:

* Category Score
* Subcategory Score
* Persona Score
* Use Case Score
* Price Constraint Score

### Retrieval Evaluation

Measures:

* Category Match Rate
* Subcategory Match Rate
* Empty Retrieval Rate

### Ranking Evaluation

Measures:

* Average Candidate Quality
* Average Top-10 Quality
* Quality Lift
* Top-1 Intrinsic Quality

This layer-wise evaluation approach enables targeted debugging and systematic improvement of the overall system.

---

## Results

### Retrieval Results

| Metric                 | Value |
| ---------------------- | ----- |
| Category Match Rate    | ~0.93 |
| Subcategory Match Rate | ~0.61 |
| Empty Retrieval Rate   | ~0.03 |

Retrieval evaluation revealed vocabulary and taxonomy mismatches between user queries and catalog labels, leading to several improvements in taxonomy matching and candidate selection.

### Ranking Results

| Metric                    | Value |
| ------------------------- | ----- |
| Average Candidate Quality | ~0.43 |
| Average Top-10 Quality    | ~0.69 |
| Quality Lift              | ~0.26 |
| Top-1 Intrinsic Quality   | ~0.78 |

The ranking engine successfully promoted higher-quality products from the retrieved candidate set, resulting in a significant improvement in recommendation quality.

---

## Failure Analysis

The evaluation framework helped identify several important system failures during development.

### Query Understanding Failures

The parser initially struggled with taxonomy mismatches between user vocabulary and catalog labels, leading to incorrect intent extraction.

### Retrieval Failures

Some subcategories had limited product coverage because of dataset size and distribution issues. This caused retrieval to return broader category-level results instead of specific subcategory results.

### Ranking Failures

Popularity signals were initially dominating the ranking formula, allowing some lower-quality products to appear in top recommendations. The ranking logic was revised to give stronger importance to trusted quality signals.

---

## Key Improvements

### Query Understanding

* Improved taxonomy matching
* Improved category and subcategory extraction
* Reduced vocabulary mismatch issues

### Retrieval

* Increased catalog size
* Introduced weighted sampling
* Improved subcategory coverage

### Ranking

* Reduced excessive popularity influence
* Strengthened quality signals
* Improved recommendation quality

### Evaluation

* Built parser evaluation framework
* Built retrieval evaluation framework
* Built ranking evaluation framework
* Enabled layer-wise debugging and failure analysis

---

## Key Learning

One of the biggest lessons from this project was that recommendation quality is a pipeline problem rather than a ranking problem.

A failure in query understanding affects retrieval.

A failure in retrieval affects ranking.

A failure in ranking affects final recommendations.

This led to the development of layer-wise evaluation frameworks that made it possible to identify failures, trace root causes, and improve the system systematically.

---

## Future Improvements

* MLflow experiment tracking
* LLM-based query understanding
* Semantic retrieval using vector search
* Learning-to-rank models
* Stronger validation layer
* Docker deployment
* GitHub Actions CI/CD
* Real user feedback integration

---

## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Jupyter Notebook

---

## Author

**Tanvi Ranganekar**

M.Sc. Data Science
