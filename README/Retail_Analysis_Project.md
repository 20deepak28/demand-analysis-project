# Retail Demand Forecasting & Inventory Optimization

An end-to-end data science project using the **Walmart M5 Forecasting dataset** to study retail demand patterns, build demand-forecasting models, estimate inventory planning thresholds, and present results through an interactive dashboard.

> **Live dashboard:** [RetailIQ](https://retailiq-tmqgsgb5rsshhqvgmvqx4b.streamlit.app/)  
> **Dashboard application repository:** [RetailIQ on GitHub](https://github.com/20deepak28/RetailIQ)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Business Problem](#business-problem)
- [Project Objectives](#project-objectives)
- [Dataset](#dataset)
- [Project Workflow](#project-workflow)
- [Data Processing and Feature Engineering](#data-processing-and-feature-engineering)
- [Forecasting Models](#forecasting-models)
- [Model Evaluation](#model-evaluation)
- [Future Demand Forecasting](#future-demand-forecasting)
- [Inventory Optimization](#inventory-optimization)
- [Inventory Risk Analysis](#inventory-risk-analysis)
- [RetailIQ Dashboard](#retailiq-dashboard)
- [Technology Stack](#technology-stack)
- [Repository Structure](#repository-structure)
- [How to Explore the Project](#how-to-explore-the-project)
- [Key Learnings](#key-learnings)
- [Limitations and Assumptions](#limitations-and-assumptions)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Project Overview

Retail demand is not constant. It changes with seasonality, calendar events, promotions, store location, product category, and other factors. Understanding these patterns can help retailers plan replenishment and reduce the risk of holding too much or too little inventory.

This project explores that problem using the Walmart M5 sales dataset. It covers the data science workflow from large-scale data preparation and feature engineering to model evaluation, demand estimates, inventory analysis, and dashboard deployment.

The final application, **RetailIQ**, provides an interactive interface for exploring the project outputs.

## Business Problem

Retailers need to estimate how much of each product customers may purchase and use that information to support inventory planning.

This project investigates questions such as:

- How does demand vary across products, categories, stores, and time?
- Can historical sales and calendar information help estimate future demand?
- How do different forecasting models compare?
- How can demand variability be translated into illustrative safety-stock and reorder-point thresholds?
- Which product-store combinations should be prioritised for further inventory-risk investigation?

## Project Objectives

1. Explore historical retail sales patterns.
2. Process a large, multi-store, multi-product dataset.
3. Build leakage-conscious time-series features.
4. Train and evaluate LightGBM and LSTM forecasting models.
5. Generate a 28-day experimental forecast for each product-store series.
6. Calculate illustrative safety-stock and reorder-point thresholds.
7. Create a product-level inventory-risk prioritisation analysis.
8. Present the results in a public, interactive Streamlit dashboard.

## Dataset

**Source:** [M5 Forecasting — Accuracy competition on Kaggle](https://www.kaggle.com/competitions/m5-forecasting-accuracy)

The project uses Walmart historical daily sales data, with product, department, category, store, calendar, event, SNAP, and price information.

Project data scale:

| Measure | Coverage |
|---|---:|
| Product-store time series | 30,490 |
| Individual products | 3,049 |
| Stores | 10 |
| Historical daily observations per series | 1,941 |
| Long-format feature records | 59,181,090 |
| Feature columns in the prepared dataset | 27 |

The historical sales period used in the project runs from **January 29, 2011 to May 22, 2016**.

The prepared long-format feature data was stored in Parquet chunks to make large-scale processing more manageable.

## Project Workflow

```text
Walmart M5 Dataset
        |
        v
Data Exploration and Understanding
        |
        v
Data Preparation and Reshaping
        |
        v
Feature Engineering
        |
        v
Baseline and Model Development
        |
        +----------------------+
        |                      |
        v                      v
     LightGBM                 LSTM
        |                      |
        +----------+-----------+
                   |
                   v
             Model Evaluation
                   |
                   v
       Experimental Future Forecast
                   |
          +--------+--------+
          |                 |
          v                 v
 Inventory Thresholds   Forecast Error
          |                 |
          +--------+--------+
                   |
                   v
          Inventory Risk Analysis
                   |
                   v
          RetailIQ Dashboard
                   |
                   v
          Public Deployment
```

## Data Processing and Feature Engineering

The raw sales data was reshaped into a product-store-date structure and processed in manageable Parquet chunks.

The feature engineering workflow included:

### Historical demand features

- `lag_1`
- `lag_7`
- `lag_28`
- `rolling_mean_7`
- `rolling_mean_28`

Rolling features were shifted so that the current day's sales were not included in their own predictors.

### Calendar and business features

- Date and calendar attributes
- Event information
- SNAP indicators
- Product pricing information

The prepared feature dataset contained **59,181,090 records and 27 columns** across 30,490 product-store series.

## Forecasting Models

Two model approaches were developed and evaluated.

### 1. LightGBM

LightGBM was used as a tree-based gradient boosting approach for demand estimation using engineered historical, calendar, event, SNAP, and price features.

Reported validation metrics:

- MAE: **0.930733**
- RMSE: **2.006124**
- WAPE: **71.662936%**

The best iteration recorded for the full LightGBM model was 286.

### 2. LSTM

A Long Short-Term Memory network was developed using PyTorch to model sequential demand patterns.

The model used:

- 28 time steps of historical input
- 14 historical features
- 8 future-known features
- A historical sequence encoder and a future-feature branch
- Huber loss and AdamW optimisation
- Learning-rate scheduling and gradient clipping

The model was trained using streaming batches to work with the scale of the prepared dataset.

Two checkpoints were compared: Epoch 2 and Epoch 5.

## Model Evaluation

The saved validation metrics are:

| Model | MAE | RMSE | WAPE |
|---|---:|---:|---:|
| LightGBM | 0.930733 | 2.006124 | 71.662936% |
| LSTM — Epoch 2 | 0.889473 | 2.137365 | 68.49% |
| LSTM — Epoch 5 | 0.887903 | 2.149717 | 68.37% |

### Interpretation

- LSTM Epoch 5 recorded the lowest MAE and WAPE among the reported results.
- LightGBM recorded the lowest RMSE.
- No single model performed best on every metric.

These are the project's saved validation results. They should be interpreted alongside the limitations described below, particularly the unresolved difference between saved validation predictions and a reconstructed inference check.

## Future Demand Forecasting

A recursive 28-day forecast was generated for all **30,490 product-store combinations** using the selected LSTM checkpoint.

| Forecast detail | Value |
|---|---|
| Product-store combinations | 30,490 |
| Forecast records | 853,720 |
| Forecast horizon | 28 days |
| Start date | May 23, 2016 |
| End date | June 19, 2016 |

The forecast process used the most recent 28 days of historical features as the initial sequence. Each generated prediction was then added to the rolling history for subsequent forecast steps.

**Important:** These dates are part of the historical M5 benchmark period. This is an experimental historical forecast, not a live forecast for current retail operations.

## Inventory Optimization

An illustrative inventory-planning analysis was created for each product-store combination.

The calculations used these project assumptions:

- Replenishment lead time: **7 days**
- Target service level: **95%**
- Z-score: **1.645**

The main calculations were:

```text
Safety Stock = Z-score × Demand Standard Deviation × √Lead Time

Reorder Point = Average Daily Demand × Lead Time + Safety Stock
```

The output includes:

- Average daily demand
- Demand standard deviation
- Safety stock
- Reorder point

These values are planning thresholds derived from historical demand statistics and stated assumptions. They are not live inventory quantities or purchase-order recommendations.

## Inventory Risk Analysis

A product-level risk prioritisation analysis was developed by combining two ranked components:

- Forecast-error ranking
- Safety-stock ranking

The project-defined score was:

```text
Inventory Risk Score =
(0.5 × Error Rank + 0.5 × Safety Stock Rank) × 100
```

Risk bands used in the project:

| Risk band | Score |
|---|---:|
| Low | 0–50 |
| Medium | Above 50–75 |
| High | Above 75–90 |
| Critical | Above 90–100 |

Risk distribution across the 30,490 product-store combinations:

| Risk band | Combinations |
|---|---:|
| Low | 15,681 |
| Medium | 7,801 |
| High | 4,282 |
| Critical | 2,726 |
| **Total** | **30,490** |

This score is a project-defined prioritisation measure. It is **not** a statistically calibrated probability of stockout.

## RetailIQ Dashboard

**Explore the live application: [Open RetailIQ](https://retailiq-tmqgsgb5rsshhqvgmvqx4b.streamlit.app/)**

RetailIQ is the Streamlit application built to make the project's results easier to explore.

### Dashboard sections

| Section | What it shows |
|---|---|
| Executive Overview | Key demand and inventory-risk summaries |
| Demand Forecasting | Daily predicted demand and category-level trends |
| Historical vs Forecast | Historical sales followed by the 28-day forecast for a selected product-store series |
| Model Performance | Saved LightGBM and LSTM validation metrics |
| Store & Category Analysis | Comparisons across stores and product categories |
| Inventory Optimization | Safety-stock and reorder-point recommendations |
| High-Risk Products | Product-store combinations prioritised by the project's risk score |

### Dashboard features

- Product-category filters
- Store filters
- Product ID search
- Interactive Plotly charts
- Data tables
- CSV downloads

The dashboard is deployed separately in the [RetailIQ GitHub repository](https://github.com/20deepak28/RetailIQ).

## Technology Stack

| Area | Tools |
|---|---|
| Programming | Python |
| Data manipulation | Pandas, NumPy |
| Data storage | Parquet, PyArrow |
| Visualisation | Matplotlib, Seaborn, Plotly |
| Machine learning | LightGBM, Scikit-learn |
| Deep learning | PyTorch |
| Dashboard | Streamlit |
| Development environment | Google Colab |
| Version control and hosting | GitHub |
| Application deployment | Streamlit Community Cloud |

## Repository Structure

The complete project documentation and development work are maintained separately from the lightweight dashboard deployment repository.

### Main project repository

```text
retail-analysis-project/
├── README.md
├── notebooks/
├── docs/
│   └── daily-logs/
├── reports/
└── requirements.txt
```

### Dashboard repository

```text
RetailIQ/
├── app.py
├── requirements.txt
├── README.md
└── data/
    ├── product_summary.parquet
    ├── future_forecasts.parquet
    ├── historical_last_28_days.parquet
    ├── category_error_summary.csv
    └── store_error_summary.csv
```

The exact files available in each repository may evolve as the project is updated.

## How to Explore the Project

1. Start with the notebooks to follow the workflow from data exploration through modelling and analysis.
2. Review the model evaluation section to understand the reported validation results.
3. Review the inventory methodology and limitations before interpreting the recommendations.
4. Open the [live RetailIQ dashboard](https://retailiq-tmqgsgb5rsshhqvgmvqx4b.streamlit.app/) to interact with the prepared project outputs.
5. Visit the [RetailIQ dashboard repository](https://github.com/20deepak28/RetailIQ) for the Streamlit application and deployment files.

## Key Learnings

This project provided practical experience in:

- Working with a large retail time-series dataset.
- Processing tens of millions of records using Pandas and Parquet.
- Creating lag and rolling-window features while avoiding direct target leakage.
- Training and comparing tree-based and recurrent neural-network models.
- Evaluating forecasts with MAE, RMSE, and WAPE.
- Building recursive multi-step forecasts.
- Translating demand variability into illustrative inventory thresholds.
- Designing a business-facing dashboard.
- Packaging and deploying a Streamlit application.
- Debugging data, charting, and deployment issues.

## Limitations and Assumptions

The outputs should be interpreted with the following limitations in mind:

1. **Historical benchmark period:** The future forecast dates are May 23 to June 19, 2016. They are not current forecasts.
2. **Inference consistency:** A reconstructed one-step inference check did not match a saved validation prediction for one inspected series. The original validation inference sequence was not fully recovered, so the discrepancy remains unresolved.
3. **Experimental future forecasts:** The corrected-scale recursive forecasts are candidate experimental outputs and have not been established as production-ready forecasts.
4. **Inventory data:** The M5 dataset does not provide actual on-hand inventory or supplier lead times.
5. **Assumed replenishment settings:** The seven-day lead time and 95% service level are project assumptions, not values supplied by Walmart.
6. **Risk-score interpretation:** The risk score is a relative, project-defined prioritisation measure, not a calibrated stockout probability.
7. **Historical comparison:** The dashboard's historical-versus-forecast view shows consecutive time periods. It should not be mistaken for a same-period forecast-accuracy comparison.

## Future Improvements

Potential next steps include:

- Reconcile the LSTM training and inference pipelines and validate recursive forecast generation.
- Evaluate forecasts across multiple time windows and product segments.
- Add prediction intervals and uncertainty analysis.
- Incorporate real inventory-on-hand, supplier lead-time, and replenishment data.
- Back-test inventory policies against historical demand.
- Add automated data refresh and model monitoring.
- Improve deployment testing and application observability.

## Author

**Deepak Kumar Shukla**

Aspiring Data Scientist interested in Python, machine learning, deep learning, and practical data-driven business applications.

- **GitHub:** [20deepak28](https://github.com/20deepak28)
- **LinkedIn:** [Deepak Kumar Shukla](https://www.linkedin.com/in/deepak-kumar-shukla-474ab922a/)

---

If you explore the project or dashboard, feedback and suggestions are welcome.
