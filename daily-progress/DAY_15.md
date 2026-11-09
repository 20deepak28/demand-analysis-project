# Day 15 — RetailIQ Dashboard & Deployment

## Objective

Complete the client-facing dashboard for the Retail Demand Forecasting & Inventory Optimization project, prepare its deployment package, and publish the application online.

## 1. Final Streamlit Dashboard

Created the final dashboard application in:

`Retail-Demand-Forecasting/dashboard/app.py`

Built using **Streamlit** and **Plotly**, with seven business-focused sections:

1. **Executive Overview** — portfolio KPIs, category demand, and inventory risk distribution.
2. **Demand Forecasting** — daily predicted demand, category trends, and product-level forecast summaries.
3. **Historical vs Forecast** — comparison of the last 28 days of actual sales with the following 28-day forecast for a selected product-store combination.
4. **Model Performance** — LightGBM and LSTM validation comparison using MAE, RMSE, and WAPE.
5. **Store & Category Analysis** — forecast demand and validation performance by store and category.
6. **Inventory Optimization** — safety-stock and reorder-point recommendations.
7. **High-Risk Products** — risk prioritization table and CSV export.

### Dashboard capabilities

- Global product-category and store filters.
- Product ID search.
- Interactive Plotly charts.
- Sortable data tables.
- CSV downloads for relevant analyses.
- Business-friendly navigation and labels.
- No backend chunk labels or chunk selectors exposed to dashboard users.

## 2. Dashboard Data

| Dataset | Records / Coverage |
|---|---:|
| Product-store summary | 30,490 combinations |
| Future forecasts | 853,720 rows |
| Forecast horizon | 28 days |
| Historical sales comparison | 28 days |
| Inventory risk analysis | 30,490 combinations |
| Inventory recommendations | 30,490 combinations |
| Store analysis | 10 stores |
| Category analysis | 3 categories |

The future forecast period is **May 23 to June 19, 2016**, based on the historical Walmart M5 benchmark dataset.

## 3. Historical vs Forecast

Prepared the final 28 days of historical sales from the M5 evaluation dataset:

- Historical period: **April 25 – May 22, 2016**
- Forecast period: **May 23 – June 19, 2016**

The dashboard compares actual historical sales and model-generated forecasts for an individual product-store combination. This is a comparison of consecutive periods, not a forecast-accuracy calculation.

## 4. Model Performance

The dashboard presents the saved validation metrics:

| Model | MAE | RMSE | WAPE |
|---|---:|---:|---:|
| LightGBM | 0.930733 | 2.006124 | 71.662936% |
| LSTM — Epoch 2 | 0.889473 | 2.137365 | 68.49% |
| LSTM — Epoch 5 | 0.887903 | 2.149717 | 68.37% |

LSTM Epoch 5 has the lowest MAE and WAPE among these reported results, while LightGBM has the lowest RMSE.

## 5. Inventory Optimization & Risk Analysis

Included inventory recommendations based on illustrative project assumptions:

- Lead time: 7 days.
- Service level: 95%.
- Safety stock and reorder point calculated from historical demand statistics.

The M5 dataset does not contain actual on-hand inventory or supplier lead times. Therefore, the outputs are planning thresholds, not live stock levels, stockout alerts, or purchase orders.

The project-defined inventory risk score combines forecast-error ranking and safety-stock ranking. It is a prioritization measure, not a calibrated probability of stockout.

## 6. Deployment Package

Prepared a standalone deployment folder:

`Retail-Demand-Forecasting/deployment/`

```text
deployment/
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

The deployment package size was approximately **7.69 MB** and was prepared to run independently of Google Drive and Colab.

## 7. Public Deployment

Published the application using **Streamlit Community Cloud**, with code and supporting datasets hosted in GitHub.

Live application:

**https://retailiq-tmqgsgb5rsshhqvgmvqx4b.streamlit.app/**

Deployment work included:
- Preparing the deployment folder and dependencies.
- Uploading the application and datasets to GitHub.
- Resolving corrupted Parquet uploads.
- Fixing a Plotly timestamp error in the historical-vs-forecast chart.
- Correcting HTML rendering in the dashboard header.
- Restarting and verifying the deployed application.

The deployed dashboard successfully displayed the Executive Overview, demand charts, inventory recommendations, and risk analysis during final checks.

## 8. Tools & Technologies

Python · Pandas · NumPy · PyArrow / Parquet · LightGBM · PyTorch · Streamlit · Plotly · GitHub · Streamlit Community Cloud · Google Colab · Google Drive

## 9. Key Learning Outcomes

- Turning modelling notebooks into a usable analytics application.
- Designing a client-facing dashboard around business questions.
- Preparing dashboard-ready datasets from a large-scale project.
- Comparing historical sales with model-generated estimates.
- Presenting model metrics and inventory assumptions transparently.
- Packaging a Streamlit application for deployment.
- Managing datasets on GitHub and resolving binary-file upload issues.
- Debugging Plotly and Streamlit runtime errors.
- Deploying a public application and checking its behaviour.

## 10. Important Limitations

- The forecast period is a historical benchmark period in 2016, not a current operational forecast.
- The corrected-scale future LSTM forecasts remain experimental because the original validation inference mismatch was not fully resolved.
- Saved validation metrics do not prove that recursive future forecasts are production-ready.
- Inventory recommendations rely on assumed lead time and service level and do not use actual inventory-on-hand or supplier data.
- The risk score is a project-defined prioritization metric, not a calibrated stockout probability.

## Day 15 Outcome

**Completed the RetailIQ dashboard, prepared its standalone deployment package, and published the application on Streamlit Community Cloud.**

The project now has a public interactive interface showcasing demand forecasting, model evaluation, store and category analysis, inventory recommendations, and product-risk analysis.

### Live Project

https://retailiq-tmqgsgb5rsshhqvgmvqx4b.streamlit.app/
