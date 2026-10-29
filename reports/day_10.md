# Day 10 — Full Dataset Preparation & Feature Engineering

## 🎯 Objective

Prepare the original M5 retail sales dataset and extend the existing feature engineering workflow to the full dataset while processing data in manageable chunks.

---

## Part 1: Full Dataset Preparation

### 1. Original Dataset Overview

Worked with the original M5 Forecasting dataset rather than the smaller sample used during initial development.

**Dataset statistics:**

* Total product-store combinations: 30,490
* Unique products: 3,049
* Stores: 10
* Daily sales observations: 59,181,090
* Daily sales columns: 1,941
* Total units sold: 66,927,173
* Zero-sales observations: 40,241,819
* Positive-sales observations: 18,939,271
* Sales date range: January 29, 2011 – May 22, 2016

### 2. Data Processing in Chunks

Processed the original sales data in batches of 1,000 product-store combinations to manage memory usage.

Generated 31 Parquet files and organized the processed data into separate directories.

**Why chunking?**

The original dataset contains approximately 59 million observations. Processing it in smaller batches reduces memory pressure and makes the workflow more manageable.

### 3. Calendar Integration

Joined the original sales data with calendar information to add:

* Date
* Weekday
* Month
* Year
* Event name
* Event type
* SNAP indicators for California, Texas and Wisconsin
* Retail week identifier (`wm_yr_wk`)

Saved the calendar-enriched data in the processed dataset directory.

### 4. Selling Price Integration

Joined weekly selling prices using:

* `store_id`
* `item_id`
* `wm_yr_wk`

**Price integration results:**

* Total observations: 59,181,090
* Observations with matched prices: 46,881,677
* Observations with missing prices: 12,299,413
* Missing-price percentage: 20.78%

The missing-price observations corresponded to zero-sales records. All positive-sales records had a matched selling price.

### 5. Revenue Calculation

Created a revenue column using:

`revenue = sales × sell_price`

Revenue was calculated where selling-price information was available.

**Total revenue with known prices:** 191,577,552.00 in the dataset's price units.

Saved the revenue-enriched data in:

`Data/processed/full_dataset/revenue/`

### 6. Data Quality Report

Generated a data quality report containing key dataset statistics, sales totals, price coverage and missing-price information.

**Report location:**

`reports/full_dataset_quality_report.csv`

---

## Part 2: Feature Engineering

### 1. Lag Features

Created historical sales features for each product-store combination.

| Feature  | Description                   |
| -------- | ----------------------------- |
| `lag_1`  | Sales from the previous day   |
| `lag_7`  | Sales from seven days earlier |
| `lag_28` | Sales from 28 days earlier    |

These features help forecasting models learn from historical demand patterns.

### 2. Rolling Features

Created rolling averages using historical sales only.

| Feature           | Description                                |
| ----------------- | ------------------------------------------ |
| `rolling_mean_7`  | Average sales over the previous seven days |
| `rolling_mean_28` | Average sales over the previous 28 days    |

The sales series is shifted by one day before calculating rolling averages to prevent the current day's sales from leaking into its own features.

### 3. Numerical Calendar Feature

Added `day_of_week` by converting weekday names into numerical values:

* Monday = 0
* Tuesday = 1
* Wednesday = 2
* Thursday = 3
* Friday = 4
* Saturday = 5
* Sunday = 6

Existing calendar columns, including date, weekday, month and year, were retained.

### 4. Event Indicator

Created the `is_event` feature using the available `event_name_1` column.

* `1` — An event is recorded.
* `0` — No event is recorded.

The original processed dataset does not contain `event_name_2`, so the indicator currently uses `event_name_1` only.

### 5. Existing Features Retained

Preserved the existing:

* SNAP indicators
* Selling-price information
* Revenue
* Calendar features
* Product and store identifiers

---

## Part 3: Validation and Output

### Validation Results

* Processed all 31 original dataset chunks.
* Created five lag and rolling features.
* Added `day_of_week` and `is_event`.
* Confirmed that all 31 output chunks contain the required feature columns.
* Verified that `day_of_week` and `is_event` have no missing values.
* Confirmed that missing lag and rolling values occur at the beginning of each product-store series, where sufficient historical observations are unavailable.

### Output Directories

**Revenue-enriched dataset:**

`Data/processed/full_dataset/revenue/`

**Feature-engineered dataset:**

`Data/processed/full_dataset/featured/`

**Data quality report:**

`reports/full_dataset_quality_report.csv`

---

## 📚 Key Learnings

* Processing large datasets in chunks to manage memory usage.
* Joining calendar and weekly selling-price information.
* Calculating revenue while accounting for missing prices.
* Creating lag and rolling features for time-series forecasting.
* Preventing target leakage by using historical sales only.
* Validating feature columns and expected missing values.
* Organizing processed datasets and quality reports for reproducibility.

## 🚀 Next Steps

1. Review feature values and chronological ordering across the complete dataset.
2. Prepare the training dataset and define the forecasting target.
3. Establish a baseline forecasting model.
4. Evaluate forecasting performance using appropriate metrics.
5. Compare the full-dataset model against the existing sample-data baseline.
