# Day 1 — Retail Demand Forecasting & Inventory Optimization

## 1. Project Overview

The goal of this project is to build a Retail Demand Forecasting and Inventory Optimization System that analyzes historical sales data, identifies demand patterns, predicts future sales, and helps businesses make better inventory decisions.

The project uses the Walmart M5 Forecasting dataset.

## 2. Project Objectives

- Analyze historical retail sales data.
- Identify sales trends and demand patterns.
- Explore relationships between sales and calendar events.
- Build machine learning models to forecast future demand.
- Optimize inventory decisions using demand forecasts.
- Develop a dashboard to communicate forecasts and business insights.

## 3. Dataset Overview

The project uses three primary datasets.

### A. Sales Training Data

File: `sales_train_validation.csv`

- Contains historical daily sales for individual products across Walmart stores.
- Each row represents a product-store combination.
- Columns beginning with `d_` represent sales on individual days.
- Contains product, department, category, store, and state identifiers.

Shape: `30,490 rows × 1,919 columns`

### B. Calendar Data

File: `calendar.csv`

- Maps day identifiers to actual dates.
- Contains weekday and calendar event information.
- Helps identify weekly patterns, holidays, and special events.

Shape: `1,969 rows × 14 columns`

### C. Sell Prices Data

File: `sell_prices.csv`

- Contains product selling prices for individual stores and weeks.
- Can help investigate relationships between prices and demand.

Shape: `6,841,121 rows × 4 columns`

## 4. Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook
- Git and GitHub

Additional tools and libraries will be introduced as the project progresses.

## 5. Work Completed

### Task 1: Environment Setup

- Verified the Python installation.
- Set up the project directory.
- Opened Jupyter Notebook.
- Loaded the required datasets using Pandas.

### Task 2: Dataset Inspection

Inspected the shapes and structures of the datasets.

```python
print(sales.shape)
print(calendar.shape)
print(prices.shape)
